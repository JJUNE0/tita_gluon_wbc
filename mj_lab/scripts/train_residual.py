"""VALIDATION_SIM: renderer compatibility for the already-running Experiment1.

New torque training uses train_residual_torque; this module only renders saved
traces and imports no retired action-residual task.
"""
from mj_lab.scripts.residual_training import main

if __name__=='__main__':
    main()
