from minigrid.envs.doorkey import DoorKeyEnv
from minigrid.core.world_object import Door, Key, Goal
from minigrid.core.grid import Grid

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
        self.put_obj(Door(colors[color_idx], is_locked=True), splitIdx, doorIdx)
        
        # Place key of corresponding color on left side
        self.place_obj(obj=Key(colors[color_idx]), top=(0,0), size=(splitIdx, height))
        
        num_additional_keys = self._rand_int(1, 4)
        for _ in range(num_additional_keys):
            while color_idx in used_colors:
                color_idx = self._rand_int(0, len(colors))
            
            self.place_obj(obj=Key(colors[color_idx]), top=(0,0), size=(splitIdx, height))
            used_colors.append(color_idx)
        
        self.mission = "use key to open the door then get to the goal"
        
    
    
    
    