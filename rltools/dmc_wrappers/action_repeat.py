from .base import Wrapper


class ActionRepeat(Wrapper):
    """Repeat the same action multiple times."""
    def __init__(self, env, frames_number: int):
        assert frames_number > 0
        super().__init__(env)
        self.fn = frames_number

    def step(self, action):
        rew_sum = 0.
        discount = 1.
        for _ in range(self.fn):
            timestep = self._env.step(action)
            rew_sum += discount*timestep.reward
            discount *= timestep.discount
            if timestep.last():
                break
        # pylint: disable-next=protected-access
        return timestep._replace(reward=rew_sum, discount=discount)