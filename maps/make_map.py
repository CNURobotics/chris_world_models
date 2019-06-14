#!/usr/bin/python

import     os.path
import     cv2
import     numpy as np
from       copy import deepcopy


def rotate(pose, origin, points,pixel_size):

    x = deepcopy(points)

    # Return image coordinates by defining (x,-y) relative the origin
    x[:,0] = origin[0] + (points[:,0]*np.cos(pose[2]) - points[:,1]*np.sin(pose[2]) + pose[0])/pixel_size
    x[:,1] = origin[1] - (points[:,0]*np.sin(pose[2]) + points[:,1]*np.cos(pose[2]) + pose[1])/pixel_size
    return x


def gazebo_world_box(fout,label, box, box_size, color):

    fout.write( "    <model name=\""+label+"\">\n")
    fout.write( "      <static>true</static>\n")
    fout.write( "      <link name=\""+label+"_link\">\n")
    fout.write( "        <pose> "+str(box[0]) + " " + str(box[1])+"  0.15 0 0 "+str(box[2])+"</pose>\n")
    fout.write( "        <collision name=\""+label+"_collision\">\n")
    fout.write( "          <geometry>\n")
    fout.write( "            <box>\n")
    fout.write( "              <size>"+str(box_size[0]) + " " + str(box_size[1])+" 0.3</size>\n")
    fout.write( "            </box>\n")
    fout.write( "          </geometry>\n")
    fout.write( "        </collision>\n")
    fout.write( "        <visual name=\""+label+"_visual\">\n")
    fout.write( "          <geometry>\n")
    fout.write( "            <box>\n")
    fout.write( "              <size>"+str(box_size[0]) + " " + str(box_size[1])+" 0.3</size>\n")
    fout.write( "            </box>\n")
    fout.write( "          </geometry>\n")
    fout.write( "          <material>\n")
    fout.write( "             <ambient>"+' '.join(map(str, color))+"</ambient>\n")
    fout.write( "             <diffuse>"+' '.join(map(str, color))+"</diffuse>\n")
    fout.write( "             <specular>0.1 0.1 0.1 1</specular>\n")
    fout.write( "             <emissive>0 0 0 0</emissive>\n")
    fout.write( "           </material>\n")
    fout.write( "        </visual>\n")
    fout.write( "      </link>\n")
    fout.write( "    </model>\n")
    fout.write( "\n")
    fout.write( "\n")


def write_gazebo_header(fout):
    fout.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    fout.write("<sdf version=\"1.4\">\n")
    fout.write("  <world name=\"default\">\n")
    fout.write("    <scene>\n")
    fout.write("      <ambient>0.5 0.5 0.5 1</ambient>\n")
    fout.write("      <background>0.5 0.5 0.5 1</background>\n")
    fout.write("      <shadows>false</shadows>\n")
    fout.write("    </scene>\n")
    fout.write("    <physics type=\"ode\">\n")
    fout.write("      <gravity>0 0 -9.81</gravity>\n")
    fout.write("      <ode>\n")
    fout.write("        <solver>\n")
    fout.write("          <type>quick</type>\n")
    fout.write("          <iters>10</iters>\n")
    fout.write("          <sor>1.3</sor>\n")
    fout.write("        </solver>\n")
    fout.write("        <constraints>\n")
    fout.write("          <cfm>0.0</cfm>\n")
    fout.write("          <erp>0.2</erp>\n")
    fout.write("          <contact_max_correcting_vel>100.0</contact_max_correcting_vel>\n")
    fout.write("          <contact_surface_layer>0.001</contact_surface_layer>\n")
    fout.write("        </constraints>\n")
    fout.write("      </ode>\n")
    fout.write("      <real_time_update_rate>1000</real_time_update_rate>\n")
    fout.write("      <max_step_size>0.001</max_step_size>\n")
    fout.write("    </physics>\n")
    fout.write("    <light type=\"directional\" name=\"directional_light_1\">\n")
    fout.write("      <cast_shadows>false</cast_shadows>\n")
    fout.write("      <pose>0 0 30 0.1 0.1 0</pose>\n")
    fout.write("      <diffuse>1.0 1.0 1.0 1</diffuse>\n")
    fout.write("      <specular>.1 .1 .1 1</specular>\n")
    fout.write("      <attenuation>\n")
    fout.write("        <range>300</range>\n")
    fout.write("      </attenuation>\n")
    fout.write("      <direction>0.1 0.1 -1</direction>\n")
    fout.write("    </light>\n")
    fout.write("    <model name=\'ground_plane\'>\n")
    fout.write("      <static>1</static>\n")
    fout.write("      <link name=\'link\'>\n")
    fout.write("        <collision name=\'collision\'>\n")
    fout.write("          <geometry>\n")
    fout.write("            <plane>\n")
    fout.write("              <normal>0 0 1</normal>\n")
    fout.write("              <size>100 100</size>\n")
    fout.write("            </plane>\n")
    fout.write("          </geometry>\n")
    fout.write("          <surface>\n")
    fout.write("            <friction>\n")
    fout.write("              <ode>\n")
    fout.write("                <mu>100</mu>\n")
    fout.write("                <mu2>50</mu2>\n")
    fout.write("              </ode>\n")
    fout.write("              <torsional>\n")
    fout.write("                <ode/>\n")
    fout.write("              </torsional>\n")
    fout.write("            </friction>\n")
    fout.write("            <contact>\n")
    fout.write("              <ode/>\n")
    fout.write("            </contact>\n")
    fout.write("            <bounce/>\n")
    fout.write("          </surface>\n")
    fout.write("          <max_contacts>10</max_contacts>\n")
    fout.write("        </collision>\n")
    fout.write("        <visual name=\'visual\'>\n")
    fout.write("          <cast_shadows>0</cast_shadows>\n")
    fout.write("          <geometry>\n")
    fout.write("            <plane>\n")
    fout.write("              <normal>0 0 1</normal>\n")
    fout.write("              <size>100 100</size>\n")
    fout.write("            </plane>\n")
    fout.write("          </geometry>\n")
    fout.write("          <material>\n")
    fout.write("            <script>\n")
    fout.write("              <uri>file://media/materials/scripts/gazebo.material</uri>\n")
    fout.write("              <name>Gazebo/Grey</name>\n")
    fout.write("            </script>\n")
    fout.write("          </material>\n")
    fout.write("        </visual>\n")
    fout.write("        <self_collide>0</self_collide>\n")
    fout.write("        <kinematic>0</kinematic>\n")
    fout.write("        <gravity>1</gravity>\n")
    fout.write("      </link>\n")
    fout.write("    </model>\n")
    fout.write("\n")

def write_gazebo_footer(fout):
    fout.write("\n")
    fout.write("  </world>\n")
    fout.write("</sdf>\n")


def write_gazebo(filename, walls, boxes,wall_size,box_size):
    fout = open(filename,"w")

    write_gazebo_header(fout)

    fout.write("<!--______________________________gazebo world______________________________ -->\n")
    color =  np.array([0.7, 0.9, 0.7, 1.0])
    cnt = 0
    for wall in  walls:
        cnt = cnt +1
        gazebo_world_box(fout,"wall_"+str(cnt), wall, wall_size,color)

    cnt = 0
    for box in  boxes:
        cnt = cnt +1
        gazebo_world_box(fout,"box_"+str(cnt), box, box_size, color)
    fout.write("<!--______________________________gazebo world______________________________ -->\n")
    write_gazebo_footer(fout)
    fout.close()

def write_map_yaml(filename, resolution, origin_meters):

    fout = open(filename+".yaml","w")

    fout.write("image: "+filename+".pgm\n")
    fout.write("resolution: %.3f\n" % resolution)
    fout.write("origin: [%.3f, %.3f, 0.0]\n"%tuple(origin_meters))
    fout.write("negate: 0\n")
    fout.write("occupied_thresh: 0.65\n")
    fout.write("free_thresh: 0.196\n")
    fout.close()

def make_map(filename,
             h_cells, w_cells, origin_cells, boxes, walls,
             cell_size=0.6096, pixel_size=0.050,     # 2 foot floor tiles
             box_size=np.array([12.,17.5])*0.0254,   # copier paper box
             wall_size=np.array([1.0,48.0])*0.0254): # Styrofoam wall

    #define the size of the map
    w_pixels    = int(round(w_cells*cell_size/pixel_size))
    h_pixels    = int(round(h_cells*cell_size/pixel_size))

    grid_map    = np.zeros((h_pixels,w_pixels,3),np.uint8) + 255

    # Origin in pixels
    origin         = origin_cells*cell_size/pixel_size # origin in image space  (upper left with x to right and y down)

    box_poly = np.array([[-box_size[0]*0.5, -box_size[1]*0.5],
                         [ box_size[0]*0.5, -box_size[1]*0.5],
                         [ box_size[0]*0.5,  box_size[1]*0.5],
                         [-box_size[0]*0.5,  box_size[1]*0.5]])

    wall_poly = np.array([[-wall_size[0]*0.5, -wall_size[1]*0.5],
                          [ wall_size[0]*0.5, -wall_size[1]*0.5],
                          [ wall_size[0]*0.5,  wall_size[1]*0.5],
                          [-wall_size[0]*0.5,  wall_size[1]*0.5]])

    # Draw axes on image
    axes_line = np.array([[w_pixels*pixel_size*0.05, 0],
                          [            0           , 0]])

    # To draw checkerboard pattern
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

    cell_2_meters = np.array([[cell_size,0,0],[0,cell_size,0],[0,0,1]] )
    walls = np.dot(walls,cell_2_meters) # Convert cells into meters
    boxes = np.dot(boxes,cell_2_meters) # Convert cells into meters
    print "walls=",walls
    print "boxes=",boxes

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
    cv2.imwrite(filename+".pgm",grid_map)

    # draw axes
    x_line = tuple(map(tuple,np.int32(rotate(np.array([0,0,0]),origin,axes_line,pixel_size))))
    cv2.line(grid_map,x_line[0],x_line[1],(0,0,255))
    y_line = tuple(map(tuple,np.int32(rotate(np.array([0,0,np.pi/2]),origin,axes_line,pixel_size))))
    cv2.line(grid_map,y_line[0],y_line[1],(0,255,0))

    # Draw png image with axes drawn for reference
    cv2.imwrite(filename+".png",grid_map)
    cv2.imshow("map",grid_map)

    write_gazebo(filename+".world", walls,boxes,wall_size,box_size)


    corner_bottom_left_cartesian = np.array([-origin[0]*pixel_size,
                                             -(h_pixels - origin[1])*pixel_size ])
    write_map_yaml(filename, pixel_size, corner_bottom_left_cartesian)

    cv2.waitKey(1)
    cv2.destroyAllWindows()
