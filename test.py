import gymnasium as gym 
import custom_minigrid
import matplotlib.pyplot as plt 
from minigrid.wrappers import RGBImgObsWrapper


# env = RGBImgObsWrapper(gym.make('AdvancedDoorKey-19x19-v0',
#                render_mode='rgb_array'))

env = RGBImgObsWrapper(gym.make('SmallAdvancedDoorKey-8x8-v0',
               render_mode='rgb_array'))

# env = RGBImgObsWrapper(gym.make('LockedRoom-v0',
#                render_mode='rgb_array'))

img, _ = env.reset()

img = img["image"]

print(img.shape)

fig = plt.figure(num=1, clear=True)
ax = fig.add_subplot()
ax.imshow(img)
plt.show()


