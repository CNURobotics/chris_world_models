#!/usr/bin/python

import   os.path
import   cv2
import   numpy as np
from     copy import deepcopy
from     make_map import *

# Define our map parameters
w_cells     = 16
h_cells     = 15
cell_size   = 0.6096
pixel_size  = 0.05
origin_cells = np.array([8,5]) # origin in cells (image) space  (upper left with x to right and y down)
box_size=np.array([12.,17.5])*0.0254   # copier paper box
wall_size=np.array([1.0,48.0])*0.0254 # Styrofoam wall


# Vectors to center of box and wall in cell coordinates
half_vector = np.array([np.cos(np.pi/4.),
                        np.sin(np.pi/4.)])

half_box_vector = (0.5*box_size[0]/cell_size)*half_vector

# Half wall vector in cell size
half_wall_vector = (0.5*wall_size[0]/cell_size)*half_vector

box_size_cells = box_size/cell_size


print "half vector  =",half_vector
print "half box     =",half_box_vector
print "half wall    =",half_wall_vector

back_wall = (58*0.0254/cell_size)*half_vector
print "back wall=",back_wall
front_wall = ( (6*0.0254 + 12*0.0254)/cell_size)*half_vector + half_wall_vector
print "front_wall =",front_wall
side_wall = (50*0.0254/cell_size)*half_vector + half_wall_vector
side_wall[1] = -side_wall[1]
print "side_wall =",side_wall
office_wall = (7*0.0254/cell_size)*half_vector + half_wall_vector
office_wall[1] = -office_wall[1]
print "office_wall =",office_wall

# Locate center reference of all boxes in world (in cell coordinates w.r.t origin but rotation in image frame (negative cartesian frame))
boxes = [np.array([  2.0 - 0.0*box_size_cells[1], (-2.0 + 0.5*box_size_cells[0]) , np.pi/2 ]),
         np.array([  2.0 + 1.0*box_size_cells[1], (-2.0 + 0.5*box_size_cells[0]) , np.pi/2 ]),
         np.array([  2.0 - 0.0*box_size_cells[1], (-3.0 - 0.5*box_size_cells[0]) , np.pi/2 ]),
         np.array([  2.0 + 1.0*box_size_cells[1], (-3.0 - 0.5*box_size_cells[0]) , np.pi/2 ]),
         np.array([  2.0 + 1.5*box_size_cells[1]+0.5*box_size_cells[0],
                    -2.5 , 0.0]),
         np.array([  (3.0 - 0.5*box_size_cells[0]*half_vector[0] + side_wall[0] - (8.5*0.0254/cell_size)*half_vector[0]) ,
                     (-3.0 - 0.5*box_size_cells[0]*half_vector[1] + side_wall[1] + (8.5*0.0254/cell_size)*half_vector[1]) ,
                     np.pi/4 ]), # side computer
         np.array([  (0.0  - 0.5*box_size_cells[0]) ,
                     (-3.0 - 0.5*box_size_cells[1]) ,
                     0.0 ]), # solitary box
         np.array([ -2.0 - 0.5*box_size_cells[0], ( 0.0 - 0.5*box_size_cells[1]) , 0 ]),
         np.array([ -2.0 - 0.5*box_size_cells[0], ( 0.0 - 0.5*box_size_cells[1]) , 0 ]),
         np.array([ -2.0 - 0.5*box_size_cells[0], ( 0.0 - 1.5*box_size_cells[1]) , 0 ]),
         np.array([ -1.0 + 0.5*box_size_cells[0], ( 0.0 - 0.5*box_size_cells[1]) , 0 ]),
         np.array([ -1.0 + 0.5*box_size_cells[0], ( 0.0 - 1.5*box_size_cells[1]) , 0 ]),
         np.array([ -1.5 ,
                     0.0 - 2.0*box_size_cells[1]-0.5*box_size_cells[0], np.pi/2.0])
                  ] # box center in meters and orientation

# Locate the center reference of all walls in world (in cells with rotation in image frame)
walls = [np.array([ -4.5 - back_wall[0]      ,  0.5 - back_wall[1]       ,  np.pi/4.0 ]), # back wall top
         np.array([ -3.0 - back_wall[0]      , -1.0 - back_wall[1]       ,  np.pi/4.0 ]), # back wall center
         np.array([ -2.0 - back_wall[0]      , -2.0 - back_wall[1]       ,  np.pi/4.0 ]), # back wall top
         np.array([ -1.0 - back_wall[0]      , -3.0 - back_wall[1]       ,  np.pi/4.0 ]), # back wall bottom
         np.array([ -3.0 + office_wall[0]    , -6.0 + office_wall[1]     , -np.pi/4.0 ]), # Office wall
         np.array([ -2.5                     ,  3.0                      ,  np.pi/4.0 ]), # Table side
         np.array([  0.0 + front_wall[0]     ,  3.0 + front_wall[1]      ,  np.pi/4.0 ]), # Front wall
         np.array([  1.0 + front_wall[0]     ,  2.0 + front_wall[1]      ,  np.pi/4.0 ]), # Front wall
         np.array([  2.0 + front_wall[0]     ,  1.0 + front_wall[1]      ,  np.pi/4.0 ]), # Front wall
         np.array([  3.0 + front_wall[0]     ,  0.0 + front_wall[1]      ,  np.pi/4.0 ]), # Front wall
         np.array([  4.0 + front_wall[0]     , -1.0 + front_wall[1]      ,  np.pi/4.0 ]), # Front wall
         np.array([  5.0 + front_wall[0]     , -2.0 + front_wall[1]      ,  np.pi/4.0 ]), # Front wall
         np.array([  6.0 + front_wall[0]     , -3.0 + front_wall[1]      ,  np.pi/4.0 ]), # Front wall
         np.array([ -2.0 + side_wall[0]      , -8.0 + side_wall[1]       , -np.pi/4.0 ]), # side cabinet
         np.array([ -1.0 + side_wall[0]      , -7.0 + side_wall[1]       , -np.pi/4.0 ]), # side wall
         np.array([  0.0 + side_wall[0]      , -6.0 + side_wall[1]       , -np.pi/4.0 ]), # side cabinet
         np.array([  1.0 + side_wall[0]      , -5.0 + side_wall[1]       , -np.pi/4.0 ]), # side wall
         np.array([  2.0 + side_wall[0]      , -4.0 + side_wall[1]       , -np.pi/4.0 ]), # side wall
         np.array([  3.0 + side_wall[0]      , -3.0 + side_wall[1]       , -np.pi/4.0 ]), # side wall
         np.array([  4.0 + side_wall[0]      , -2.0 + side_wall[1]       , -np.pi/4.0 ]), # side wall
         np.array([  5.0 + side_wall[0]      , -1.0 + side_wall[1]       , -np.pi/4.0 ]), # side wall
         np.array([ -0.5 +half_wall_vector[0],  3.5 + half_wall_vector[1], -np.pi/4.0 ]), # desk wall
         np.array([ -1.0 +half_wall_vector[0],  3.0 + half_wall_vector[1], -np.pi/4.0 ]), # desk wall
         np.array([ -3.0 -half_wall_vector[0],  3.0 + half_wall_vector[1], -np.pi/4.0 ]), # desk wall
         np.array([ -4.5 -half_wall_vector[0],  1.5 + half_wall_vector[1], -np.pi/4.0 ]), # desk wall
         np.array([ -6.0 -half_wall_vector[0],  0.0 + half_wall_vector[1], -np.pi/4.0 ])  # desk wall
                 ]


make_map("lab_world_050", h_cells, w_cells, origin_cells, boxes, walls,box_size=box_size, wall_size=wall_size)
