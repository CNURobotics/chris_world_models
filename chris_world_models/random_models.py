#/usr/bin/python3
import sys
import time
import yaml
import numpy as np

def get_map_extents(map_path):

    print(" map path: ", map_path)

    with open (f"{map_path}.pgm", "rb") as pgmf:
        header = pgmf.readline().decode('utf-8').strip().split(" ")
        print(">", header,"<")
        while len(header) < 3:
            line =  pgmf.readline().decode('utf-8').strip()
            if line[0] == '#':
                continue  # Skip pure comment lines
            header += line.split(" ")

        print(">", header,"<")
        width, height = float(header[1]), float(header[2])

    with open(f"{map_path}.yaml", "r") as yamlf:
        try:
            params = yaml.safe_load(yamlf)
        except yaml.YAMLError as exc:
            print(exc)
            raise exc

        #print("MAP YAML: ", params)
        #print(f"Map {map_name} {width} x {height}")

    origin = params['origin']
    resolution = params['resolution']

    return (origin[0], origin[1],
            origin[0] + resolution*width,
            origin[1] + resolution*height)

def generate_random_spawn_string(map_path, models, counts):

    extents = get_map_extents(map_path)

    spawn_string = ""

    for i, model in enumerate(models):
        count = counts[i]

        x_pose = np.random.uniform(extents[0], extents[2], count)
        y_pose = np.random.uniform(extents[1], extents[3], count)
        z_pose = 0*x_pose + 0.25

        for j in range(count):
            name = f"{model.split('.')[0]}_{j}_{int(time.time_ns()%1e10)}"

            # Assume no namespace for now
            spawn_string += f"{name}, ,{model},{x_pose[j]},{y_pose[j]},{z_pose[j]}\n"
    return spawn_string


if __name__ == '__main__':

    map_path = sys.argv[1]
    models = ['blue_ball.urdf.xacro', 'red_ball.urdf.xacro', 'green_ball.urdf.xacro' ]
    counts = [3, 4, 2]

    extents = get_map_extents(map_path)
    print(f"Map {map_name} Extents : {extents}")

    spawn_string = generate_random_spawn_string(map_path, models, counts)
    print(30*"=")
    print(spawn_string)
