from custom_minigrid.envs import AdvancedDoorKeyEnv
from custom_minigrid.envs import ObservableLockedRoomEnv
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

register(
    id="AdvancedDoorKey-19x19-v0",
    entry_point="custom_minigrid.envs:AdvancedDoorKeyEnv",
    kwargs={"size": 19}
)

register(
    id="SmallAdvancedDoorKey-8x8-v0",
    entry_point="custom_minigrid.envs:AdvancedDoorKeyEnv",
    kwargs={"size": 8,
            "possible_key_colours": ["red", "green", "blue"],
            "door_color": "red"}
)

register(
    id="LockedRoom-v0",
    entry_point="custom_minigrid.envs:ObservableLockedRoomEnv",
)