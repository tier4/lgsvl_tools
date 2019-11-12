# LGSVL Tools
Python Based Tools for the LGSVL Simulator

## How to setup

### with pipenv
```
sudo pip install pipenv
cd (LGSVL_TOOLD_DIR)
pipenv install
```

## Modules
### URDF Generator
urdf generation tools for LGSVL Simulator 
It reads json setting file from LGSVL simulator and generate ROS urdf file.

#### How to use

##### run with pipenv
```
pipenv shell
python .\urdf_generator.py .\data\example.json .\data\output.lexus 0 0 0 lexus package://minimum_visual_robot/meshes/DAE/base/lexus.dae
```