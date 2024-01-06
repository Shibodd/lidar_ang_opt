import surface_generators
import numpy as np
import matplotlib.pyplot as plt
import math
import utils
import scipy.spatial.transform as scipy_tf

DENSITY = 10
CHUNKS = 10


ANGLES_PATH = "angles_vlp-32c.txt"
LIDAR_HEIGHT = 0.85
TF = np.array([[1, 0, 0],
               [0, 1, 0],
               [0, 0, -1]])
DETECTION_WIDTH = 10
DETECTION_MIN_DISTANCE = 1.5
DETECTION_MAX_DISTANCE = 31
CONE_HEIGHT = 0.35

LIDAR_ANGLES = np.arange(start=6, stop=-7, step=-1)
LIDAR_RANGE = 30

RENDER = True

vertex = utils.vec(0, 0, LIDAR_HEIGHT)
box_min = utils.vec(-DETECTION_WIDTH / 2, DETECTION_MIN_DISTANCE, 0)
box_max = utils.vec(DETECTION_WIDTH / 2, DETECTION_MAX_DISTANCE, CONE_HEIGHT)

if RENDER:
  fig = plt.figure()
  ax = fig.add_subplot(projection='3d')
  ax: plt.Axes

  ax.set_xlabel('x')
  ax.set_ylabel('y')
  ax.set_zlabel('z')

  box_x,box_y,box_z = utils.get_cube()
  box_size = box_max - box_min
  box_center = box_min + (box_size / 2)
  ax.plot_surface(
    box_center[0] + box_x * box_size[0],
    box_center[1] + box_y * box_size[1],
    box_center[2] + box_z * box_size[2],
    color=(0,0,0,0.05), 
    edgecolors=(0,0,0,0.3)
  )

ray_angles = utils.load_angles(ANGLES_PATH)

def evaluate(lidar_angle):
  global TF, ray_angles, RENDER, CHUNKS
  tf = np.matmul(scipy_tf.Rotation.from_euler('x', -lidar_angle, degrees=True).as_matrix(), TF)

  n = 0
  for ray_angle in ray_angles:
    for i in range(CHUNKS):
      pts = surface_generators.rand_cone_surface(DENSITY, math.radians(90 + ray_angle), (0, 2*np.pi), LIDAR_RANGE)
      pts = np.matmul(tf, pts)
      pts = vertex + pts
      pts = pts[:, utils.pts_in_box(pts, box_min, box_max)]

      n += np.count_nonzero(utils.pts_in_box(pts, box_min, box_max))

      if RENDER:
        ax.scatter(pts[0], pts[1], pts[2], marker=('.'))
  return n

if RENDER:
  plt.ion()
  plt.show()

for lidar_angle in LIDAR_ANGLES:
  n = evaluate(lidar_angle)
  print(f"{lidar_angle}: {n}")
  if RENDER:
    input()
    ax.cla()
