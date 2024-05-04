<p align="center">
  <img src="image/logo.jpg" width="500">
</p>

## MoMa-Pos: Where Should Mobile Manipulators Stand in Cluttered Environment Before Task Execution?
[Beichen Shao<sup>1<sup>](https://github.com/ssspeg), [Yan Ding<sup>2<sup>](https://yding25.com/)  

Welcome to the official repository for MoMa-Pos. 

You can access the paper [here](https://arxiv.org/abs/2403.19940),  and the project website [here](https://yding25.com/MoMa-Pos/).

###  Installation

Clone the repository and initialize submodules:

```
git clone https://github.com/AutonoBot-Lab/Project_MoMa-Pos.git
git submodule init
git submodule update
```
Install the OMPL package:

[Download the latest OMPL release.](https://github.com/ompl/ompl/releases/tag/prerelease)

```
pip3 install pygccxml==2.2.1.
cd BestMan_Pybullet/package_OMPL
pip3 install ompl-1.6.0-cp38-cp38-manylinux_2_28_x86_64.whl
```
### Main Project Structure
```
├── Kitchen_models
├── MoMa_Pos
│   ├── MoMa_main.py
│   ├── ...
├── URDF_models
├── URDF_robot
│   ├── segbot.urdf
│   ├── ur5e.urdf
│   └── ...
└── utils
    ├── pb_ompl.py
    ├── utils_Bestman.py
    ├── utils_sample_R.py
    ├── utils_Potential_R.py
```

## Basic Demos

Run a basic demo:
```
python3 ./MoMa_Pos/MoMa_main.py
```
## Attention
The current code's parameter input is not written succinctly. We will address this by refining the code encapsulation in subsequent updates
