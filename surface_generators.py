import numpy as np
import math

def rand_cone_surface(density, theta, phi_range=(0, 2*np.pi), slant_height=1):
  """
  Generates uniformly distributed random points with the specified density
  on the section specified by phi_range
  of the surface of a cone with vertex (0,0,0)
  and specified vertical angle theta and slant height.
  """

  assert(abs(phi_range[1] - phi_range[0]) <= 2*np.pi)
  assert(slant_height > 0)

  r = abs(math.sin(theta)) * slant_height
  n = round(density * (np.pi * slant_height * r))

  phis = np.random.uniform(phi_range[0], phi_range[1], n)
  ss = np.sqrt(np.random.uniform(0, slant_height * slant_height, n))
  
  xs = ss * math.sin(theta) * np.cos(phis)
  ys = ss * math.sin(theta) * np.sin(phis)
  zs = ss * math.cos(theta)
  return np.vstack((xs, ys, zs))