import numpy as np
import math

def load_angles(path):
  with open(path, "rt") as f:
    return [float(line.strip()) for line in f]

def pts_in_box(pts, min, max):
  return np.all(np.logical_and(pts > min, pts < max), axis=0)

def vec(x, y, z):
  return np.array([x, y, z]).reshape(-1, 1)

def get_cube():  
  phi = np.arange(1,10,2)*np.pi/4
  Phi, Theta = np.meshgrid(phi, phi)

  x = np.cos(Phi)*np.sin(Theta)
  y = np.sin(Phi)*np.sin(Theta)
  z = np.cos(Theta)/np.sqrt(2)
  return x,y,z