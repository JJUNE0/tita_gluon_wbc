"""CO-RL/MOO runner configuration for the combined TITA+GLUON task."""

from isaaclab.utils import configclass

from scripts.co_rl.core.wrapper import (
    CoRlHybridPpoActorCriticCfg,
    CoRlPolicyRunnerCfg,
    CoRlPpoAlgorithmCfg,
)

from ddt_lab.tasks.moo_based.locomotion.velocity.tita_env.agents.co_rl_cfg import (
    TitaMOOPPORunnerCfg_Flat_Stand_Drive,
    TitaMOOPPORunnerCfg_Flat_Stand_Drive_RMATeacher,
)


@configclass
class TitaGluonMOOPPORunnerCfg(TitaMOOPPORunnerCfg_Flat_Stand_Drive):
    """Keep the validated TITA MOO-PPO settings under a separate experiment."""

    def __post_init__(self):
        super().__post_init__()
        self.experiment_name = "Tita_Gluon_Flat_Stand_Drive-v0-mooppo"
        self.experiment_description = "TITA locomotion with GLUON held at the WORK posture"


@configclass
class TitaGluonRandomArmMOOPPORunnerCfg(TitaGluonMOOPPORunnerCfg):
    """Separate experiment namespace for the conditioned moving-arm stage."""

    def __post_init__(self):
        super().__post_init__()
        self.experiment_name = "Tita_Gluon_RandomArm_Flat_Stand_Drive-v0-mooppo"
        self.experiment_description = (
            "TITA locomotion with conditioned smooth random GLUON trajectories"
        )


@configclass
class TitaGluonCurriculumArmRMATeacherRunnerCfg(
    TitaMOOPPORunnerCfg_Flat_Stand_Drive_RMATeacher
):
    """Validated TITA RMA parent plus the staged GLUON motion curriculum."""

    def __post_init__(self):
        super().__post_init__()
        self.experiment_name = "Tita_Gluon_CurriculumArm_RMATeacher-v0-mooppo"
        self.logger = "wandb"
        self.wandb_project = "tita-gluon-moo-teacher"
        self.run_name = "phase1-fixed-to-phase2-expanded-arm"
        self.experiment_description = (
            "RMA Teacher: validated TITA v4 height curriculum followed by "
            "conditioned GLUON workspace expansion at rollout steps 120000-204000"
        )


@configclass
class TitaGluonInspectionCurriculumArmRMATeacherRunnerCfg(
    TitaGluonCurriculumArmRMATeacherRunnerCfg
):
    """Clean RMA Teacher run over the selected inspection graph hubs."""

    def __post_init__(self):
        super().__post_init__()
        self.experiment_name = (
            "Tita_Gluon_InspectionCurriculumArm_RMATeacher-v0-mooppo"
        )
        self.max_iterations = 10_000
        self.resume = False
        self.add_cfg.w_disc = 0.5
        self.add_cfg.w_fm = 0.5
        self.enable_teacher_tsne = False
        self.run_name = "phase1-work-phase2-inspection-hubs"
        self.experiment_description = (
            "Train an RMA Teacher from scratch: hold GLUON at WORK while the "
            "TITA height curriculum completes at step 120000, widen to four "
            "offline mesh-validated inspection hubs through step 216000, then "
            "consolidate at full range through step 240000"
        )


@configclass
class TitaGluonSequentialInspectionHighLevelRunnerCfg(CoRlPolicyRunnerCfg):
    """Hybrid PPO configuration for the future frozen-low-level wrapper."""

    num_steps_per_env = 64
    max_iterations = 300
    save_interval = 25
    # The final four actor inputs are binary option masks consumed directly by
    # HybridActorCritic. Normalizing the entire observation would turn a valid
    # mask into non-binary history-dependent values.
    empirical_normalization = False
    experiment_name = "Tita_Gluon_SequentialInspection_Trigger-v0-ppo"
    experiment_description = (
        "Hybrid high-level timing policy over a frozen inspection-hub-conditioned "
        "TITA locomotion checkpoint"
    )
    run_name = "gate0-phase-trigger-timing"
    logger = "wandb"
    wandb_project = "tita-gluon-highlevel"

    policy = CoRlHybridPpoActorCriticCfg(
        init_noise_std=0.5,
        actor_hidden_dims=[256, 256, 128],
        critic_hidden_dims=[256, 256, 128],
        activation="elu",
        continuous_action_dim=2,
        discrete_action_dim=2,
        action_mask_obs_start=41,
    )

    algorithm = CoRlPpoAlgorithmCfg(
        value_loss_coef=1.0,
        use_clipped_value_loss=True,
        clip_param=0.2,
        entropy_coef=0.01,
        num_learning_epochs=5,
        num_mini_batches=4,
        learning_rate=3.0e-4,
        schedule="fixed",
        gamma=0.995,
        lam=0.95,
        desired_kl=0.01,
        max_grad_norm=1.0,
    )
