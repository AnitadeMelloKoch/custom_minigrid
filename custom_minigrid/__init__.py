from custom_minigrid.envs import AdvancedDoorKeyEnv
from gymnasium.envs.registration import register

register(
    id="AdvancedDoorKey-8x8-v0",
    entry_point="custom_minigrid.envs:AdvancedDoorKeyEnv",
    kwargs={"size": 8}
)

register(
    id="AdvancedDoorKey-16x16-v0",
    entry_point="custom_minigrid.envs:AdvancedDoorKeyEnv",
    kwargs={"size": 16}
)



