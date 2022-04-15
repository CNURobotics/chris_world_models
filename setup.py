import os
from glob import glob
from setuptools import setup, find_packages

package_name = 'chris_world_models'

setup(
    name=package_name,
    version='0.0.2',
    packages=[package_name],
    data_files=[
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'maps'), glob('maps/*')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*')),
        (os.path.join('share', package_name, 'param'), glob('param/*')),
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dcconner',
    maintainer_email='robotics@cnu.edu',
    description='Standard world models and corresponding map files for Gazebo used by CNU Robotics CHRISLab',
    license='Apache License, Version 2.0 ',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [ 'model_spawner=chris_world_models.model_spawner:main'
        ],
    },
)
