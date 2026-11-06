"""TRAINING_SIM: save resolved manager joint order for portable policy playback."""

import json
from pathlib import Path


def _plain(value):
    if hasattr(value, 'detach'):
        return value.detach().cpu().tolist()
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    return value


def save_policy_interface(env, destination):
    env = env.unwrapped
    robot = env.scene['robot']
    names = list(robot.joint_names)
    manager = env.observation_manager
    observations = []
    for name, cfg in zip(manager.active_terms['policy'], manager._group_obs_term_cfgs['policy']):
        item = {'name': name, 'scale': _plain(cfg.scale) if cfg.scale is not None else 1., 'clip': _plain(cfg.clip)}
        entity = cfg.params.get('asset_cfg')
        if entity is not None and entity.name == 'robot':
            indices = entity.joint_ids
            item['joints'] = names[indices] if isinstance(indices, slice) else [names[index] for index in indices]
        observations.append(item)
    actions = []
    for name in env.action_manager.active_terms:
        term = env.action_manager.get_term(name)
        if hasattr(term, '_joint_names'):
            actions.append({'name': name, 'joints': list(term._joint_names)})
    interface = {'schema_version': 1, 'articulation_joint_names': names, 'observations': observations, 'actions': actions}
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(interface, indent=2) + '\n')
    return interface
