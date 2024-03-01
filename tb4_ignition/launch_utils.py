# Scratch for testing/introspecting launch files in python


from ament_index_python.packages import get_package_share_directory

pkgs = ['turtlebot4_ignition_bringup', 'tb4_ignition']

for pkg in pkgs:
    print(pkg + ": " + get_package_share_directory(pkg))
