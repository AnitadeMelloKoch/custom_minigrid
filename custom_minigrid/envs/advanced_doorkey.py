from minigrid.envs.doorkey import DoorKeyEnv
from minigrid.core.world_object import Key, Goal
from custom_minigrid.core.custom_world_object import CustomDoor, CustomKey
from minigrid.core.grid import Grid
import numpy as np

class AdvancedDoorKeyEnv(DoorKeyEnv):
    def __init__(self, 
                 size=8, 
                 max_steps = None, 
                 door_color = None,
                 **kwargs):
        super().__init__(size, max_steps, **kwargs)
        
        self.door_color = door_color
        
    def place_agent_randomly(self, seed_tries):
        for _ in range(seed_tries):
            self.place_agent(size=(self.splitIdx, self.height))
        
        self.step(0)
        return self.step(1)
    
    def reset(self, *, seed=None, options=None):
        output = super().reset(seed=seed, options=options)
        self.carrying = []
        return output
    
    def _gen_grid(self, width, height):
        
        colors = ["red", "green", "blue", "purple", "yellow", "grey"]
        
        # create empty grid
        self.grid = Grid(width, height)
        
        # Generate surrounding walls
        self.grid.wall_rect(0, 0, width, height)
        
        # place a goal in the bottom-right corner
        self.put_obj(Goal(), width - 2, height - 2)
        
        # Create a vertical splittling wall
        splitIdx = self._rand_int(2, width - 2)
        self.splitIdx = splitIdx
        self.grid.vert_wall(splitIdx, 0)
        
        # place agent at random position and orientation
        # on the left side of spliting wall
        self.place_agent(size=(splitIdx, height))
        
        # Place a door in the wall
        doorIdx = self._rand_int(1, width - 2)
        if self.door_color is not None:
            color_idx = colors.index(self.door_color)
        else:
            color_idx = self._rand_int(0, len(colors))
        used_colors = []
        used_colors.append(color_idx)
        self.put_obj(CustomDoor(colors[color_idx], is_locked=True), splitIdx, doorIdx)
        
        # Place key of corresponding color on left side
        self.place_obj(obj=CustomKey(colors[color_idx]), top=(0,0), size=(splitIdx, height))
        
        num_additional_keys = self._rand_int(1, 5)
        for _ in range(num_additional_keys):
            while color_idx in used_colors:
                color_idx = self._rand_int(0, len(colors))
            
            self.place_obj(obj=CustomKey(colors[color_idx]), top=(0,0), size=(splitIdx, height))
            used_colors.append(color_idx)
        
        self.mission = "use key to open the door then get to the goal"
        
    
    def step(self, action):
        
        self.step_count += 1
            
        reward = 0
        terminated = False
        truncated = False
        
        fwd_pos = self.front_pos
        fwd_cell = self.grid.get(*fwd_pos)
        
        if action == self.actions.pickup:
            if fwd_cell and fwd_cell.can_pickup():
                self.carrying.append(fwd_cell)
                fwd_cell.cur_pos = np.array([-1, -1])
                self.grid.set(fwd_pos[0], fwd_pos[1], None)
        elif action == self.actions.drop:
            if not fwd_cell and len(self.carrying) > 0:
                self.grid.set(fwd_pos[0], fwd_pos[1], self.carrying[-1])
                self.carrying[-1].cur_pos = fwd_pos
                self.carrying.pop()
        else:
            return super().step(action)
        
        if self.step_count >= self.max_steps:
            truncated = True

        if self.render_mode == "human":
            self.render()

        obs = self.gen_obs()

        return obs, reward, terminated, truncated, {}
    
    def gen_obs_grid(self, agent_view_size=None):
        """
        Generate the sub-grid observed by the agent.
        This method also outputs a visibility mask telling us which grid
        cells the agent can actually see.
        if agent_view_size is None, self.agent_view_size is used
        """
        
        topX, topY, botX, botY = self.get_view_exts(agent_view_size)

        agent_view_size = agent_view_size or self.agent_view_size

        grid = self.grid.slice(topX, topY, agent_view_size, agent_view_size)

        for i in range(self.agent_dir + 1):
            grid = grid.rotate_left()

        # Process occluders and visibility
        # Note that this incurs some performance cost
        if not self.see_through_walls:
            vis_mask = grid.process_vis(
                agent_pos=(agent_view_size // 2, agent_view_size - 1)
            )
        else:
            vis_mask = np.ones(shape=(grid.width, grid.height), dtype=bool)

        # Make it so the agent sees what it's carrying
        # We do this by placing the carried object at the agent's position
        # in the agent's partially observable view
        agent_pos = grid.width // 2, grid.height - 1
        if self.carrying:
            grid.set(*agent_pos, self.carrying[-1])
        else:
            grid.set(*agent_pos, None)

        return grid, vis_mask
        
        