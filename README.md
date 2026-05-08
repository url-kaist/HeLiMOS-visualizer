<div align="center"> 
<h1> 🚗  HeLiMOS Visualizer 🏃</h1> 
<h3>
        <a href="https://sites.google.com/view/helimos/">Dataset</a> | 
        <a href="https://www.arxiv.org/abs/2408.06328">Paper</a>
    </h3>

Forked from the original repository: https://github.com/PRBonn/lidar-visualizer.git
</div>
<p align="center"><img src=img/helimos_viz.gif alt='animated' width=480/></p>
<div align="center"> HeLiMOS-visualizer is a tool that visualizes moving objects from heterogeneous LiDAR data.

 </div>

## :wrench: How to install

```sh
git clone https://github.com/OREOCHIZ/helimos-visualizer.git
cd helimos-visualizer

make install
```

## 💡 Usage

### 1. Set the symbolic link
Download the HeLiMOS dataset and create a symbolic link to it at `${HOME}/HeLiMOS`:
```sh
ln -s "/path/to/HeLiMOS" "$HOME/HeLiMOS"
```

After that, we expect the following directory layout:
```
${HOME}/HeLiMOS/{sequence}
└── Deskewed_LiDAR
    ├── train.txt
    ├── val.txt
    ├── test.txt
    ├── Aeva
    │   ├── calib.txt
    │   ├── velodyne
    │   └── labels
    ├── Avia
    │   ├── calib.txt
    │   ├── velodyne
    │   └── labels
    ├── Ouster
    │   ├── calib.txt
    │   ├── velodyne
    │   └── labels
    └── Velodyne
        ├── calib.txt
        ├── velodyne
        └── labels
```
In HeLiMOS, we are currently using only the sequence `KAIST05`.

### 2. Visualize Moving objects
If you want to visualize specific sensor,

```sh
helimos_visualizer --sensor [Aeva / Avia / Velodyne / Ouster] \
                   --split [train / val / test / all]
# e.g. helimos_visualizer --sensor Aeva --split train
```

- Set the `--sensor` flag to one of the following: `Avia`, `Aeva`, `Velodyne`, or `Ouster`. The default value is `Ouster`.
- Also, set the `--split` flag to `train`, `val`, `test` or `all`. The default value is `all`. 

If you would like more detailed information about the `--split`, please refer to [our dataset page](https://sites.google.com/view/helimos/tasks).


## Help
If you need more information, just type:
```sh
helimos_visualizer --help
```


## Citation

If you use this visualizer for any academic work, please cite original [kiss-icp](https://www.ipb.uni-bonn.de/wp-content/papercite-data/pdf/vizzo2023ral.pdf) and our [HeLiMOS](https://www.arxiv.org/abs/2408.06328).

