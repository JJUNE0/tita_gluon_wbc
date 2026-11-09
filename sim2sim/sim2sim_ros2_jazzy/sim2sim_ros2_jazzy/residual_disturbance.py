"""VALIDATION_SIM: payload, push, sensor/plant settings and residual switch."""
import numpy as np


class ResidualDisturbance:
    def __init__(self, env, mass=2., force=20.):
        self.env = env
        self.mass_setting, self.force_setting = float(mass), float(force)
        self.mass = 0.
        self.body = env.model.body('base_link').id
        self.local = np.zeros(3)
        self.push = False
        self.root = None
        self.selection = None
        self.mounts = {}
        for payload in range(env.model.nbody):
            if env.model.body(payload).name.startswith('residual_payload_'):
                self.mounts[int(env.model.body_parentid[payload])] = payload
        self.attachments = self.pushes = 0
        self.force_body = env.model.body('base_link').id
        self.residual_enabled = True
        self.setting_changes = []

    def set_mass(self, mass, body=None, local=None):
        mass = float(mass)
        body = self.body if body is None else body
        local = self.local if local is None else np.asarray(local, dtype=float)
        if not np.isfinite(mass) or not 0 <= mass <= 5:
            raise ValueError('Payload must be between0 and5kg')
        if body not in self.mounts or local.shape != (3,) or not np.isfinite(local).all():
            raise ValueError('Select a robot link and a finite local attachment point')
        model, data, mj = self.env.model, self.env.data, self.env.mujoco
        for payload in self.mounts.values():
            model.body_mass[payload] = 0.
            model.body_inertia[payload] = 0.
            model.geom_rgba[model.body_geomadr[payload], 3] = 0.
        payload = self.mounts[body]
        model.body_mass[payload] = mass
        model.body_inertia[payload] = mass*.4*.03**2
        model.body_pos[payload] = local
        model.geom_rgba[model.body_geomadr[payload], 3] = float(mass > 0)
        saved = data.qpos.copy(), data.qvel.copy(), data.ctrl.copy(), float(data.time)
        mj.mj_setConst(model, data)
        data.qpos[:], data.qvel[:], data.ctrl[:], data.time = saved
        data.qacc_warmstart[:] = 0.
        mj.mj_forward(model, data)
        self.mass, self.body, self.local = mass, body, local.copy()
        self.attachments += 1

    def apply(self):
        self.env.data.xfrc_applied[self.force_body, :] = 0.
        if self.push:
            self.env.data.xfrc_applied[self.force_body, 0] = self.force_setting

    def open_ui(self):
        import tkinter as tk
        from tkinter import ttk
        self.root = tk.Tk()
        self.root.title('TITA | Residual experiment')
        self.root.geometry('+20+60')
        self.root.attributes('-topmost', True)
        self.root.protocol('WM_DELETE_WINDOW', self.close)
        panel = ttk.Frame(self.root, padding=12)
        panel.pack(fill='both', expand=True)
        ttk.Label(panel, text='Double-click a robot link in MuJoCo to attach/move mass.\n'
                  'Terminal: 1 stand up, 0 RL; existing movement/pose keys.').pack(anchor='w')
        self.enabled_var = tk.BooleanVar(value=self.residual_enabled)
        ttk.Checkbutton(panel, text='Enable residual (zero-command conditions still apply)',
                        variable=self.enabled_var, command=self.enable_changed).pack(anchor='w', pady=8)
        tabs = ttk.Notebook(panel)
        tabs.pack(fill='both', expand=True)
        forces = ttk.Frame(tabs, padding=8)
        sensors = ttk.Frame(tabs, padding=8)
        tabs.add(forces, text='Mass / push / friction')
        tabs.add(sensors, text='Noise / delay')
        self.mass_var = tk.DoubleVar(value=self.mass_setting)
        ttk.Label(forces, text='Added mass (kg)').pack(anchor='w', pady=(10, 0))
        tk.Scale(forces, from_=0, to=5, resolution=.1, orient='horizontal', length=350,
                 variable=self.mass_var, command=self.mass_changed).pack(fill='x')
        ttk.Button(forces, text='Remove mass', command=lambda: self.set_mass(0.)).pack(fill='x')
        self.force_var = tk.DoubleVar(value=self.force_setting)
        ttk.Label(forces, text='Torso push (N), world +X').pack(anchor='w', pady=(10, 0))
        tk.Scale(forces, from_=0, to=50, resolution=1, orient='horizontal', length=350,
                 variable=self.force_var, command=self.force_changed).pack(fill='x')
        self.push_button = tk.Button(forces, text='PUSH TORSO — HOLD', height=2, bg='#ed9d3a')
        self.push_button.pack(fill='x', pady=6)
        self.push_button.bind('<ButtonPress-1>', self.press)
        self.push_button.bind('<ButtonRelease-1>', self.release)
        self.push_button.bind('<Leave>', self.release)
        self.root.bind('<FocusOut>', self.release)
        friction = self.env.cfg['model'].get('ground_friction')
        if friction is None:
            friction = float(self.env.model.geom_friction[self.env.ground, 0].mean())
        self.friction_var = tk.DoubleVar(value=friction)
        ttk.Label(forces, text='Ground sliding friction coefficient (mu)').pack(anchor='w', pady=(10, 0))
        tk.Scale(forces, from_=0, to=max(2., friction), resolution=.01, orient='horizontal', length=350,
                 variable=self.friction_var, command=self.friction_changed).pack(fill='x')
        ttk.Label(sensors, text='Gaussian noise: standard deviation per sensor axis.\n'
                  'Teacher, residual and joint PD feedback share each sample.').pack(anchor='w')
        self.noise_vars = {}
        noise_controls = [('joint_position', 'Joint position (rad)', .05, .001),
                          ('joint_velocity', 'Joint velocity (rad/s)', 1., .01),
                          ('gyro', 'Gyro (rad/s)', .2, .001),
                          ('orientation_deg', 'Orientation (deg)', 3., .05)]
        for key, label, maximum, resolution in noise_controls:
            self.noise_vars[key] = tk.DoubleVar(value=self.env.sensor_noise[key])
            ttk.Label(sensors, text=label).pack(anchor='w', pady=(8, 0))
            tk.Scale(sensors, from_=0, to=maximum, resolution=resolution, orient='horizontal', length=350,
                     variable=self.noise_vars[key], command=self.noise_changed).pack(fill='x')
        ttk.Label(sensors, text='Torque lag: uniform min–max, resampled each physics tick.\n'
                  'Both bounds equal gives a fixed delay.').pack(anchor='w', pady=(10, 0))
        tick_ms = self.env.model.opt.timestep*1000.
        self.delay_vars = [tk.DoubleVar(value=step*tick_ms) for step in self.env.delay_steps]
        for index, label in enumerate(('Minimum (ms)', 'Maximum (ms)')):
            ttk.Label(sensors, text=label).pack(anchor='w', pady=(8, 0))
            tk.Scale(sensors, from_=0, to=40, resolution=tick_ms, orient='horizontal', length=350,
                     variable=self.delay_vars[index],
                     command=lambda value, index=index: self.delay_changed(index)).pack(fill='x')
        ttk.Button(sensors, text='Clear noise and delay', command=self.clear_sensors).pack(fill='x', pady=8)
        ttk.Label(sensors, text='After residual OFF, older torque commands may remain\n'
                  'until the maximum delay has elapsed.').pack(anchor='w')
        self.status = tk.StringVar(value='Residual only in RL at zero velocity and nominal pose commands.')
        ttk.Label(panel, textvariable=self.status, wraplength=370).pack(anchor='w', pady=6)

    def mass_changed(self, value):
        self.mass_setting = float(value)
        if self.mass:
            self.set_mass(self.mass_setting)

    def force_changed(self, value):
        self.force_setting = float(value)

    def record_settings(self):
        self.setting_changes.append(dict(simulation_time_s=float(self.env.data.time),
            residual_requested=self.residual_enabled, **self.env.perturbation_settings()))

    def enable_changed(self):
        self.residual_enabled = bool(self.enabled_var.get())
        self.record_settings()

    def friction_changed(self, value):
        self.env.set_ground_friction(float(value))
        self.record_settings()

    def noise_changed(self, value=None):
        self.env.set_sensor_noise(**{key: variable.get() for key, variable in self.noise_vars.items()})
        self.record_settings()

    def delay_changed(self, index):
        low, high = [variable.get() for variable in self.delay_vars]
        if low > high:
            self.delay_vars[1-index].set(self.delay_vars[index].get())
        self.env.set_torque_delay(*[variable.get() for variable in self.delay_vars])
        self.record_settings()

    def clear_sensors(self):
        for variable in self.noise_vars.values():
            variable.set(0.)
        for variable in self.delay_vars:
            variable.set(0.)
        self.noise_changed()
        self.delay_changed(0)

    def press(self, event=None):
        self.push = True
        self.pushes += 1

    def release(self, event=None):
        self.push = False
        self.apply()

    def update(self, enabled, state):
        if self.root is None:
            self.apply()
            return
        self.root.update_idletasks()
        self.root.update()
        if self.root is None:
            return
        viewer = self.env.viewer
        if viewer is not None:
            with viewer.lock():
                body = int(viewer.perturb.select)
                local = viewer.perturb.localpos.copy()
            if body in self.mounts.values():
                payload = body
                body = int(self.env.model.body_parentid[payload])
                local = self.env.model.body_pos[payload]+local
            selected = (body, *np.round(local, 6))
            if body in self.mounts and selected != self.selection:
                self.set_mass(self.mass_setting, body, local)
            self.selection = selected
        self.show_status(enabled, state)
        self.apply()

    def show_status(self, enabled, state):
        if self.root is None:
            return
        self.status.set(f'{state} | residual request {"ON" if self.residual_enabled else "OFF"}'
                        f' / eligible {"YES" if enabled else "NO"}\n'
                        f'Added mass {self.mass:.1f}kg | push {self.force_setting if self.push else 0.:.0f}N\n'
                        f'Ground mu {self.friction_var.get():.2f} | current torque lag {self.env.last_delay_ms:.0f}ms')

    def close(self):
        self.release()
        if self.root is not None:
            self.root.destroy()
            self.root = None
