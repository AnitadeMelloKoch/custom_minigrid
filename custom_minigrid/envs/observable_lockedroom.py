from minigrid.envs.lockedroom import LockedRoomEnv

class ObservableLockedRoomEnv(LockedRoomEnv):
    
    def gen_obs_grid(self, agent_view_size=100):
        return super().gen_obs_grid(agent_view_size)


