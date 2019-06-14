#!/usr/bin/python

import   os.path
import   cv2
import   numpy as np
from     copy import deepcopy
from     make_map import *

# Define our map parameters
w_cells     = 10
h_cells     = 10
cell_size   = 0.6096 # Corresponds to our floor tiles in lab
pixel_size  = 0.100  # larger resolution for high-level planning
origin_cells = np.array([5,3]) # origin in cells (image) space  (upper left with x to right and y down)

box_size=np.array([12.,17.5])*0.0254   # copier paper box
wall_size=np.array([1.0,48.0])*0.0254 # Styrofoam wall

# Vectors to center of box and wall in cell coordinates
half_box_vector = (0.5/cell_size)*box_size

# Half wall vector in cell size
half_wall_vector = (0.5/cell_size)*wall_size


# Locate center reference of all boxes in world (in cell coordinates w.r.t origin but rotation in image frame (negative cartesian frame))
boxes = [np.array([                0.0        , (-1.0+half_box_vector[0]) ,  np.pi/2]),
         np.array([                0.0        , (-3.0-half_box_vector[0]) ,  np.pi/2]),
         np.array([( 1.0 + half_box_vector[1]), (-7.0+half_box_vector[0]) ,  np.pi/2]),
         np.array([(-1.0 - half_box_vector[1]), (-7.0+half_box_vector[0]) ,  np.pi/2]),
         np.array([                0.0        ,     -5.0                  ,    0.0]),
         np.array([( 2.0 + half_box_vector[0]),     -5.0                  ,    0.0]),
         np.array([(-2.0 - box_size[0]/cell_size)       ,     -5.0                  ,    0.0]),
         np.array([( 3.0 + half_box_vector[0]),      1.5                  ,    0.0]),
         np.array([(-3.0 - box_size[0]/cell_size)       ,      1.5                  ,    0.0])
         ] # box center in meters and orientation

# Locate center reference of all walls in world (in cell coordinates w.r.t origin but rotation in image frame (negative cartesian frame))
walls = [np.array([ 0.0,-7.0 , np.pi/2 ]),
         np.array([ 0.0,-2.0 ,     0.0   ]),
         np.array([ 0.0, 2.0 , np.pi/2 ]),
         np.array([ 3.0,-2.0 ,     0.0   ]),
         np.array([-3.0,-2.0 ,     0.0   ]),
         np.array([-3.0,-4.0 , np.pi/4 ]),]


make_map("creech_map_100", h_cells, w_cells, origin_cells, boxes, walls,box_size=box_size,wall_size=wall_size,pixel_size=pixel_size)
