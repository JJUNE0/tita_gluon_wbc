"""VALIDATION_SIM: bounded residual RLS and guarded, decimated gain updates."""

from collections import deque
import numpy as np
from .model import discrete, dlqr, residual_matrices


class ResidualRLS:
    def __init__(self, cfg):
        self.cfg = cfg
        if not 0 < cfg['forgetting'] <= 1 or cfg['covariance'] <= 0 or cfg['regularization'] <= 0:
            raise ValueError('Invalid RLS configuration')
        self.coefficients = np.zeros((2, 2))
        self.P = np.eye(2) * cfg['covariance']
        self.regressors = deque(maxlen=cfg['window'])
        self.bound_hits = 0

    def update(self, phi, residual):
        phi, residual = np.asarray(phi), np.asarray(residual)
        if phi.shape != (2,) or residual.shape != (2,) or not np.isfinite([phi, residual]).all():
            raise ValueError('Invalid RLS sample')
        self.regressors.append(phi.copy())
        forgetting = self.cfg['forgetting']
        gain = self.P @ phi / (forgetting + phi @ self.P @ phi + self.cfg['regularization'])
        candidate = self.coefficients + np.outer(residual - self.coefficients @ phi, gain)
        bounds = np.asarray(self.cfg['bounds']).reshape(2, 2)
        self.bound_hits += int(np.any(abs(candidate) > bounds))
        self.coefficients = np.clip(candidate, -bounds, bounds)
        self.P = (self.P - np.outer(gain, phi @ self.P)) / forgetting
        self.P = (self.P + self.P.T) / 2
        if not np.isfinite(self.P).all() or np.linalg.eigvalsh(self.P).min() <= 0:
            raise ValueError('Invalid RLS covariance')

    def diagnostics(self):
        singular = np.linalg.svd(np.asarray(self.regressors), compute_uv=False) if self.regressors else np.zeros(2)
        singular = np.pad(singular, (0, max(0, 2-len(singular))))
        condition = float(singular[0]/singular[1]) if singular[1] > 1e-12 else None
        confidence = (len(self.regressors) >= self.cfg['min_samples']
                      and singular[1] >= self.cfg['min_singular']
                      and condition is not None and condition <= self.cfg['max_condition']
                      and self.bound_hits == 0)
        return dict(coefficients=self.coefficients.reshape(4).tolist(), covariance=self.P.tolist(),
                    singular_values=singular.tolist(), rank=int(np.sum(singular > 1e-8)),
                    condition=condition, samples=len(self.regressors), bound_hits=self.bound_hits,
                    confidence=bool(confidence))


class WheelLQR:
    def __init__(self, parameters, dt, dimension, cfg, adaptive=False, shadow=False):
        self.dt, self.dimension, self.cfg = dt, dimension, cfg
        self.A0, self.B0 = discrete(parameters, dt, dimension)
        self.Q = np.diag(cfg['Q4'] if dimension == 4 else cfg['Q4'][1:])
        self.K0, self.eigenvalues = dlqr(self.A0, self.B0, self.Q, cfg['R'])
        self.K = self.K0.copy()
        self.adaptive, self.shadow = adaptive, shadow
        self.rls = ResidualRLS(cfg['rls'])
        self.steps, self.previous_u = 0, 0.
        self.pending = []
        self.accepted, self.rejected = 0, 0
        self.reason = 'cold_start'
        self.frozen, self.disabled = False, False
        self.nominal_error, self.adaptive_error = np.zeros(2), np.zeros(2)
        self.saturated = False

    def state(self, x4):
        return x4 if self.dimension == 4 else x4[1:]

    def command(self, x4, probing=0.):
        x = self.state(x4)
        if not np.isfinite(x).all():
            raise ValueError('Invalid controller state')
        raw = float(-self.K @ x + probing)
        limited = np.clip(raw, -self.cfg['total_torque_limit'], self.cfg['total_torque_limit'])
        self.saturated = bool(abs(raw-limited) > 1e-8)
        delta = self.cfg['slew_nm_s'] * self.dt
        self.previous_u = float(np.clip(limited, self.previous_u-delta, self.previous_u+delta))
        return self.previous_u

    def transition(self, x4, commanded_u, next4):
        x, following = self.state(x4), self.state(next4)
        nominal = self.A0 @ x + self.B0[:, 0]*commanded_u
        velocity_index = 1 if self.dimension == 4 else 0
        indices = [velocity_index, self.dimension-1]
        residual = (following - nominal)[indices]
        phi = np.array([x4[2], commanded_u])
        self.nominal_error = residual
        self.adaptive_error = residual - self.rls.coefficients @ phi
        if not (self.adaptive or self.shadow) or self.frozen or self.disabled:
            return
        self.pending.append((phi, residual))
        self.steps += 1
        if self.steps % self.cfg['update_every']:
            return
        try:
            for regressors, error in self.pending:
                self.rls.update(regressors, error)
            self.pending.clear()
            if not self.rls.diagnostics()['confidence']:
                raise ValueError('insufficient_excitation_or_bounds')
            dA, dB = residual_matrices(self.rls.coefficients, self.dt, self.dimension)
            A, B = self.A0+dA, self.B0+dB
            candidate, eigenvalues = dlqr(A, B, self.Q, self.cfg['R'], self.cfg['stability_margin'])
            if np.linalg.norm(candidate-self.K) > self.cfg['gain_step_fraction']*np.linalg.norm(self.K0):
                raise ValueError('gain_step_limit')
            if np.linalg.norm(candidate-self.K0) > self.cfg['gain_total_fraction']*np.linalg.norm(self.K0):
                raise ValueError('gain_total_limit')
            if abs((candidate-self.K) @ following) > self.cfg['gain_command_step_nm']:
                raise ValueError('command_step_limit')
            # Guard transient growth on BOTH nominal and candidate models.
            for plant_A, plant_B in ((self.A0, self.B0), (A, B)):
                response = following.copy()
                starting_cost = float(response @ self.Q @ response) + 1e-8
                for _ in range(self.cfg['validation_steps']):
                    u = np.clip(-candidate @ response, -self.cfg['total_torque_limit'], self.cfg['total_torque_limit'])
                    response = plant_A @ response + plant_B[:, 0]*u
                    if not np.isfinite(response).all() or response @ self.Q @ response > self.cfg['max_cost_growth']*starting_cost:
                        raise ValueError('validation_transient')
            self.reason = 'shadow_valid' if self.shadow else 'accepted'
            if not self.shadow:
                self.K, self.eigenvalues = candidate, eigenvalues
                self.accepted += 1
        except (ValueError, np.linalg.LinAlgError) as error:
            self.reason = str(error)
            self.rejected += 1
            if 'covariance' in self.reason or 'sample' in self.reason:
                self.disabled = True
                self.pending.clear()

    def diagnostics(self):
        dA, dB = residual_matrices(self.rls.coefficients, self.dt, self.dimension)
        return dict(**self.rls.diagnostics(), K=self.K.tolist(),
                    spectral_radius=float(max(abs(self.eigenvalues))),
                    delta_A_norm=float(np.linalg.norm(dA)), delta_B_norm=float(np.linalg.norm(dB)),
                    accepted=self.accepted, rejected=self.rejected, reason=self.reason,
                    disabled=self.disabled, saturated=self.saturated,
                    nominal_error=self.nominal_error.tolist(), adaptive_error=self.adaptive_error.tolist())
