#!/usr/bin/python

import     os.path
import     cv2
import     numpy as np
from     copy import deepcopy


def rotate(pose, origin, points,pixel_size):

    x = deepcopy(points)

    # Return image coordinates by defining (x,-y) relative the origin
    x[:,0] = origin[0] + (points[:,0]*np.cos(pose[2]) - points[:,1]*np.sin(pose[2]) + pose[0])/pixel_size
    x[:,1] = origin[1] - (points[:,0]*np.sin(pose[2]) + points[:,1]*np.cos(pose[2]) + pose[1])/pixel_size
    return x


def gazebo_world_box(label, box, box_size, color):

    print "    <model name=\""+label+"\">"
    print "      <static>true</static>"
    print "      <link name=\""+label+"_link\">"
    print "        <pose> "+str(box[0]) + " " + str(box[1])+"  0.15 0 0 "+str(box[2])+"</pose>"
    print "        <collision name=\""+label+"_collision\">"
    print "          <geometry>"
    print "            <box>"
    print "              <size>"+str(box_size[0]) + " " + str(box_size[1])+" 0.3</size>"
    print "            </box>"
    print "          </geometry>"
    print "        </collision>"
    print "        <visual name=\""+label+"_visual\">"
    print "          <geometry>"
    print "            <box>"
    print "              <size>"+str(box_size[0]) + " " + str(box_size[1])+" 0.3</size>"
    print "            </box>"
    print "          </geometry>"
    print "          <material>"
    print "             <ambient>"+' '.join(map(str, color))+"</ambient>"
    print "             <diffuse>"+' '.join(map(str, color))+"</diffuse>"
    print "             <specular>0.1 0.1 0.1 1</specular>"
    print "             <emissive>0 0 0 0</emissive>"
    print "           </material>"
    print "        </visual>"
    print "      </link>"
    print "    </model>"
    print "    "
    print "    "


w_cells     = 10
h_cells     = 10
cell_size   = 0.6096

pixel_size  = 0.05

w_pixels    = w_cells*cell_size/pixel_size
h_pixels    = h_cells*cell_size/pixel_size

grid_map    = np.zeros((h_pixels,w_pixels,3),np.uint8) + 255


origin         = np.array([5,3])*cell_size/pixel_size # origin in image space  (upper left with x to right and y down)


box_size    = np.array([12.,17.5])*0.0254  # box size in meters
wall_size   = np.array([1.0,48.0])*0.0254  # wall size in meters

box_poly = np.array([[-box_size[0]*0.5, -box_size[1]*0.5],
                     [ box_size[0]*0.5, -box_size[1]*0.5],
                     [ box_size[0]*0.5,  box_size[1]*0.5],
                     [-box_size[0]*0.5,  box_size[1]*0.5]])

wall_poly = np.array([[-wall_size[0]*0.5, -wall_size[1]*0.5],
                      [ wall_size[0]*0.5, -wall_size[1]*0.5],
                      [ wall_size[0]*0.5,  wall_size[1]*0.5],
                      [-wall_size[0]*0.5,  wall_size[1]*0.5]])
axes_line = np.array([[w_pixels*pixel_size*0.05, 0],
                      [            0           , 0]])

cell_poly = np.array([[-cell_size*0.5, -cell_size*0.5],
                      [ cell_size*0.5, -cell_size*0.5],
                      [ cell_size*0.5,  cell_size*0.5],
                      [-cell_size*0.5,  cell_size*0.5]])

print "pixels=(",h_pixels,", ",w_pixels,")"
print "origin=",origin
print "box_size=",box_size
print "wall_size=",wall_size

print "box polygon =",box_poly
print "wall=",wall_poly

# Use Cartesian coordinates in meters
boxes = [np.array([                0.0                , (-1.0*cell_size +0.5*box_size[0]) ,  np.pi/2]),
         np.array([                0.0                , (-3.0*cell_size -0.5*box_size[0]) ,  np.pi/2]),
         np.array([( 1.0*cell_size  + 0.5*box_size[1]), (-7.0*cell_size +0.5*box_size[0]) ,  np.pi/2]),
         np.array([(-1.0*cell_size  - 0.5*box_size[1]), (-7.0*cell_size +0.5*box_size[0]) ,  np.pi/2]),
         np.array([                0.0                ,     -5.0*cell_size                ,    0.0]),
         np.array([( 2.0*cell_size + 0.5*box_size[0]) ,     -5.0*cell_size                ,    0.0]),
         np.array([(-2.0*cell_size - 1.0*box_size[0]) ,     -5.0*cell_size                ,    0.0]),
         np.array([( 3.0*cell_size + 0.5*box_size[0]) ,      1.5*cell_size                ,    0.0]),
         np.array([(-3.0*cell_size - 1.0*box_size[0]) ,      1.5*cell_size                ,    0.0])
         ] # box center in meters and orientation

walls = [#np.array([ 2.5,-0.5 , np.pi/4 ]),
         #np.array([-2.5,-0.5 ,-np.pi/4 ]),
         #np.array([ 1.125, 0.875 , np.pi/4 ]),
         #np.array([-1.125, 0.875 ,-np.pi/4 ]),
         np.array([ 0.0,-7.0 , np.pi/2 ]),
         np.array([ 0.0,-2.0 ,     0.0   ]),
         np.array([ 0.0, 2.0 , np.pi/2 ]),
         np.array([ 3.0,-2.0 ,     0.0   ]),
         np.array([-3.0,-2.0 ,     0.0   ]),
         np.array([-3.0,-4.0 , np.pi/4 ]),]

cell_2_meters = np.array([[cell_size,0,0],[0,cell_size,0],[0,0,1]] )
walls = np.dot(walls,cell_2_meters) # Convert cells into meters
print "walls=",walls


for i in np.arange(0,w_cells):
    for j in np.arange(0,h_cells):
        if ((i+j)%2 == 0):
            pose = np.dot(np.array([(0.5 + i ), -(0.5 + j), 0.0]),cell_2_meters)
            poly= np.int32(rotate(pose,np.array([0,0]),cell_poly,pixel_size)).reshape(-1,1,2)
            #print "-----",i,", ",j
            #print poly
            cv2.fillConvexPoly(grid_map, poly, (208,208,208))#(248,248,248))

for box in boxes:
    poly= np.int32(rotate(box,origin,box_poly,pixel_size)).reshape(-1,1,2)
    cv2.fillConvexPoly(grid_map,poly, (0,0,0))

for box in walls:
    poly= np.int32(rotate(box,origin,wall_poly,pixel_size)).reshape(-1,1,2)
    cv2.fillConvexPoly(grid_map,poly, (0,0,0))

# Draw the grayscale map without axes for use with AMCL
cv2.imwrite("creech_map_050.pgm",grid_map)

# draw axes
x_line = tuple(map(tuple,np.int32(rotate(np.array([0,0,0]),origin,axes_line,pixel_size))))
cv2.line(grid_map,x_line[0],x_line[1],(0,0,255))
y_line = tuple(map(tuple,np.int32(rotate(np.array([0,0,np.pi/2]),origin,axes_line,pixel_size))))
cv2.line(grid_map,y_line[0],y_line[1],(0,255,0))

cv2.imwrite("creech_map_050.png",grid_map)
cv2.imshow("map",grid_map)

if (True):
	print "<!--______________________________gazebo world______________________________ -->"
	color =  np.array([0.7, 0.9, 0.7, 1.0])
	cnt = 0
	for box in  walls:
	    cnt = cnt +1
	    gazebo_world_box("wall_"+str(cnt), box, wall_size,color)

	for box in  boxes:
	    cnt = cnt +1
	    gazebo_world_box("box_"+str(cnt), box, box_size, color)
	print "<!--______________________________gazebo world______________________________ -->"

cv2.waitKey(0)
cv2.destroyAllWindows()
