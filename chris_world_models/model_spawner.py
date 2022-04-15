"""
Based on spawn_turtlebot.py
https://zmk5.github.io/general/demo/2019/07/15/ros2-spawning-entity.html


Script used to spawn a URDf model in a generic position
"""
import csv
import os
import sys
import rclpy
from ament_index_python.packages import get_package_share_directory, PackageNotFoundError
from gazebo_msgs.srv import SpawnEntity
import xacro

def make_spawn_request(name, urdf_file_path, robot_namespace, pose_args):
    try:
        if "xacro" in urdf_file_path:
            description_config = xacro.process_file(urdf_file_path)
            urdf_xml = description_config.toxml()
        else:
            urdf_xml = open(urdf_file_path, 'r').read()

        if isinstance(urdf_xml, str) and len(urdf_xml) > 1:
            request = SpawnEntity.Request()
            request.name = name
            request.xml = urdf_xml
            request.robot_namespace = robot_namespace
            request.initial_pose.position.x = pose_args[0]
            request.initial_pose.position.y = pose_args[1]
            request.initial_pose.position.z = pose_args[2]
            if len(pose_args) > 6:
                request.initial_pose.orientation.x = pose_args[3]
                request.initial_pose.orientation.y = pose_args[4]
                request.initial_pose.orientation.z = pose_args[5]
                request.initial_pose.orientation.w = pose_args[6]
            return request
        else:
            print(f"Invalid XML for {name}\n {e}")

    except Exception as e:
        print(f"Failed to generate request for {name}\n {e}")
        print(">", pose_args)
        pass

    return None

def load_models_from_csv_file(file_path):
    try:
        with open(file_path, "rt") as fin:
            models_text = fin.read()
            return load_models_from_string(models_text)

    except Exception as e:
        print(f"Failed to load models from {file_path}")
        print(e)
        return None

def load_models_from_string(models_string, model_pose=None):
    """
    Load models from single string interpreted as csv data
    Lines terminated with newline ('\n')
    comma separated  name, namespace, udrf_file, position x, y, z<, optional orientation x, y, z, w>
    """
    try:
        models_to_spawn = {}

        for line in models_string.split("\n"):
            if len(line) == 0 or line[0] == '#':
                continue  # ignore blank or comment lines

            try:
                data  = line.strip().split(",")
                if len(data) > 2 and (model_pose or len(data) > 5):
                    name = data[0].strip()
                    robot_namespace = data[1].strip()
                    model_path = data[2].strip()

                    if model_pose:
                        # Override any pose data on line
                        pose_args = [float(val.strip()) for val in model_pose.split(",")]

                    else:
                        pose_args = [float(val.strip()) for val in data[3:]]  # Position and optional orientation

                    if not os.path.exists(model_path):
                        # Not a full path,
                        if "/" in model_path:
                            # Assume data starts with package name, now find full path
                            model_path = model_path.split("/")
                            pkg_path = get_package_share_directory(model_path[0])
                            model_path = os.path.join(pkg_path, *model_path[1:])
                        else:
                            # Assume in this package
                            pkg_path = get_package_share_directory("chris_world_models")
                            model_path = os.path.join(pkg_path, "urdf", model_path)

                    # Find model path
                    if not os.path.exists(model_path):
                        print(f"Failed to find {model_path}")
                        print(line)
                        print(data)
                    else:
                        print(f" Set up spawn request for {name} at pose = {pose_args}")
                        request = make_spawn_request(name, model_path, robot_namespace, pose_args)
                        if request is not None:
                            models_to_spawn[name] = request
                        else:
                            print(f"    invalid request for <{data}>")
                else:
                    print(f"   invalid line <{line}>")

            except Exception as e:
                print(f"Failed to handle {line}")
                print("   ", e)

        return models_to_spawn
    except Exception as e:
        print(f"Failed to load models string\n {models_string}")
        print(e)
        return None


def main():

    """ Main for spawning URDF model node """

    argv = sys.argv[1:]  # skip node name
    if "-h" in argv or "--help" in argv:
        print("Usage of model_spawner node:")
        print("   No required arguments")
        print("   Set either models_file (CSV file) or models_string (CSV-style string) parameter")
        sys.exit(-1)

    # Start model_spawner node
    rclpy.init()

    node = rclpy.create_node("chris_world_models_urdf_model_spawner")
    node.declare_parameter('models_file', "")  # CSV style file with spawning data
    node.declare_parameter('models_string', "")  # single CSV-style string with spawning data
    node.declare_parameter('model_name', "")
    node.declare_parameter('model_namespace', "")
    node.declare_parameter('model_urdf_file', "")
    node.declare_parameter('model_pose', "")


    models_file = node.get_parameter('models_file').get_parameter_value().string_value
    if len(models_file) == 0:
        models_file = None

    models_string = node.get_parameter('models_string').get_parameter_value().string_value
    if len(models_string) == 0:
        models_string = None

    # NOTE: This is simple csv string x,y,z or x,y,z,qx,qy,qz,qw values
    #    ano not a pose message format
    model_pose = node.get_parameter('model_pose').get_parameter_value().string_value
    if len(model_pose) == 0:
        model_pose = None

    # If using parameters, must define name and urdf (in addition to model_pose)
    # namespace can be blank.
    model_name = node.get_parameter('model_name').get_parameter_value().string_value
    if len(model_name) == 0:
        model_name = None
    model_urdf_file = node.get_parameter('model_urdf_file').get_parameter_value().string_value
    if len(model_urdf_file) == 0:
        model_urdf_file = None

    model_namespace = node.get_parameter('model_namespace').get_parameter_value().string_value

    model_by_parameters = model_name and model_urdf_file and model_pose

    models_to_spawn = None  # Initialize spawn requests

    if not models_string and not models_file and not model_by_parameters:
        print("Must define models by parameters, models_string or models_file!")
        print("file: >", models_file, "<")
        print("string: >", models_string, "<")
        print("by parameters: >", model_by_parameters,"<")
        print("  name: >", model_name, "<")
        print("  namespace: >", model_namespace, "<")
        print("  pose: >", model_pose, "<")
        print("  urdf: >", model_urdf_file, "<")

        node.get_logger().info("Shutting down spawner node.")
        node.destroy_node()
        rclpy.shutdown()
        sys.exit(0)

    elif models_file:
        # We have a few options for how to access the file
        if not os.path.exists(models_file):
            # If not full path, consider two alternative locations
            try:
                if "/" not in models_file:
                    # Assume file in param folder of this package
                    pkg_path = get_package_share_directory("chris_world_models")
                    models_file = os.path.join(pkg_path, "param", models_file)
                else:
                    # Check for case where data starts with package name, now find full path
                        file_path_split = models_file.split("/")
                        pkg_path = get_package_share_directory(file_path_split[0])
                        models_file = os.path.join(pkg_path, *file_path_split[1:])
            except PackageNotFoundError:
                pass

        if os.path.exists(models_file):
            # file path exists, so try to load as csv
            print(f"Processing csv file <{models_file}>")
            models_to_spawn = load_models_from_csv_file(models_file)
        else:
            print(f"Failed to access models file <{models_file}>!")

    elif models_string:
        # Use models_string directly
        models_to_spawn = load_models_from_string(models_string, model_pose)

    elif model_by_parameters:
        print(f"Request model spawn from parameters:")
        pose_args = [float(val.strip()) for val in model_pose.split(",")]
        print(f"    name: >{model_name}<")
        print(f"    namespace: >{model_namespace}<")
        print(f"    pose: >{pose_args}<")
        print(f"    urdf: >{model_urdf_file}<")

        models_to_spawn = {model_name: make_spawn_request(model_name,
                                                          model_urdf_file,
                                                          model_namespace,
                                                          pose_args)}

    if not models_to_spawn:
        print("No valid models to spawn!")

    else:

        node.get_logger().info(
            'Creating Service client to connect to `/spawn_entity`')
        client = node.create_client(SpawnEntity, "/spawn_entity")

        node.get_logger().info("Connecting to `/spawn_entity` service...")
        if not client.service_is_ready():
            client.wait_for_service()
            node.get_logger().info("...connected!")

        for name, request in models_to_spawn.items():
            try:
                assert isinstance(request, SpawnEntity.Request), f"Not Request type ({type(request)})"
                node.get_logger().info(f"Sending service request for {request.name} to `/spawn_entity` service ...")
                future = client.call_async(request)
                rclpy.spin_until_future_complete(node, future)
                if future.result() is not None:
                    result = future.result()
                    if not result.success:
                        print(f"    Failed to spawn model {name} : {result.status_message}")
                    else:
                        print(f"    Successfully spawned {name}!")
                else:
                    raise RuntimeError(
                        'Null result when calling service: %r' % future.exception())
            except Exception as e:
                print(f"  Exception: {type(e)}, {e}")
                print(f"    Request for {name}: ({request})")

        node.get_logger().info("Done! Shutting down spawner node.")
        node.destroy_node()
        rclpy.shutdown()
        sys.exit(0)


if __name__ == "__main__":
    main()
