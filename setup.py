import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'tb4_ignition'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Install all launch files matching naming convention
        #(os.path.join('share', package_name, 'launch'),
        # glob(os.path.join('launch', '*launch.[pxy][yma]*')))
        # Install all launch, world, model files matching naming convention
        (os.path.join('share', package_name), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, "worlds"), glob('worlds/*.sdf')),
        (os.path.join('share', package_name, "gui"), glob('gui/*.config')),
        #(os.path.join('share', package_name, "models", "arashcamera"), glob('models/arashcamera/*')),
    ],
    install_requires=['setuptools','ros_ign_interfaces','ros_ign_gazebo'],
    zip_safe=True,
    maintainer='bsb',
    maintainer_email='briansbingham@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_node = tb4_ignition.my_node:main'
        ],
    },
)
