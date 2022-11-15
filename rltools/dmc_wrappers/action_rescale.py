import numpy as np

from dm_env import specs

from rltools.dmc_wrappers.base import Wrapper


class ActionRescale(Wrapper):
    """Normalize action to [-1, 1] range."""

    def __init__(self, env):
        super().__init__(env)
        spec = env.action_spec()
        assert isinstance(spec, specs.BoundedArray)
        low = spec.minimum
        high = spec.maximum
        self._diff = (high - low) / 2.
        self._spec = spec.replace(
            minimum=np.full_like(low, -1),
            maximum=np.full_like(high, 1)
        )
        self._low = low

    def step(self, action):
        action = (action + 1.) * self._diff + self._low
        return self._env.step(action)

    def action_spec(self):
        return self._spec
