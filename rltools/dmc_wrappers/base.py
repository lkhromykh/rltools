from typing import MutableMapping, NamedTuple

import dm_env
import numpy as np
from dm_env import specs

OBS_SPECS = MutableMapping[str, specs.Array]


class EnvironmentSpecs(NamedTuple):
    observation_spec: OBS_SPECS
    action_spec: specs.BoundedArray
    reward_spec: specs.Array
    discount_spec: specs.BoundedArray


# pylint: disable=no-staticmethod-decorator
class Wrapper(dm_env.Environment):
    """This allows to modify methods of an already initialized environment.

    On reset reward and discount provide default float values instead of Nones.
    """

    def __init__(self, env: dm_env.Environment):
        self._env = env

    def _observation_fn(self, timestep: dm_env.TimeStep
                        ) -> MutableMapping[str, np.ndarray]:
        return timestep.observation

    def _reward_fn(self, timestep: dm_env.TimeStep) -> float:
        if timestep.reward is None:
            return 0.
        return timestep.reward

    def _done_fn(self, timestep: dm_env.TimeStep) -> bool:
        return timestep.last()

    def _step_type_fn(self, timestep: dm_env.TimeStep) -> dm_env.StepType:
        return timestep.step_type

    def _discount_fn(self, timestep: dm_env.TimeStep) -> float:
        if timestep.discount is None:
            return 1.
        return timestep.discount

    def step(self, action) -> dm_env.TimeStep:
        timestep = self._env.step(action)
        return self._wrap_timestep(timestep)

    def reset(self) -> dm_env.TimeStep:
        return self._wrap_timestep(self._env.reset())

    def _wrap_timestep(self, timestep) -> dm_env.TimeStep:
        # pylint: disable-next=protected-access
        return timestep._replace(
            step_type=self._step_type_fn(timestep),
            reward=self._reward_fn(timestep),
            discount=self._discount_fn(timestep),
            observation=self._observation_fn(timestep)
        )

    def action_spec(self) -> specs.Array:
        return self._env.action_spec()

    def observation_spec(self) -> OBS_SPECS:
        return self._env.observation_spec()

    def reward_spec(self) -> specs.Array:
        return self._env.reward_spec()

    def discount_spec(self) -> specs.BoundedArray:
        return self._env.discount_spec()

    @property
    def environment_specs(self):
        return EnvironmentSpecs(
            observation_spec=self.observation_spec(),
            action_spec=self.action_spec(),
            reward_spec=self.reward_spec(),
            discount_spec=self.discount_spec()
        )

    @property
    def unwrapped(self) -> dm_env.Environment:
        if hasattr(self._env, "unwrapped"):
            return self._env.unwrapped
        return self._env
