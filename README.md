<div align="center">
<h1>🚗 HeLiMOS Visualizer 🏃</h1>
<h3>
    <a href="https://sites.google.com/view/helimos/">Dataset</a> |
    <a href="https://www.arxiv.org/abs/2408.06328">Paper</a>
</h3>

Forked from the original repository: https://github.com/PRBonn/lidar-visualizer.git

</div>

<p align="center"><img src="img/helimos_viz.gif" alt="animated" width="480"/></p>

<div align="center">
HeLiMOS-visualizer is a tool that visualizes moving objects from heterogeneous LiDAR data.
</div>

## :wrench: How to install

```sh
git clone https://github.com/url-kaist/HeLiMOS-visualizer.git
cd HeLiMOS-visualizer
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

In HeLiMOS, we are currently using only the sequence `KAIST05`. If your dataset
lives elsewhere, pass `--data /path/to/HeLiMOS/{sequence}/Deskewed_LiDAR`
explicitly instead of relying on the symlink.

### 2. Visualize moving objects

```sh
helimos_visualizer --sensor [Aeva | Avia | Velodyne | Ouster] \
                   --split  [train | val | test | all]
# e.g. helimos_visualizer --sensor Aeva --split train
```

- `--sensor`: one of `Aeva`, `Avia`, `Velodyne`, `Ouster`. Default: `Ouster`.
- `--split` : one of `train`, `val`, `test`, `all`. Default: `all`.
- `-n / --n-scans`: limit the number of scans to render.
- `-j / --jump`: skip the first N scans.

For details about the splits, see [our dataset page](https://sites.google.com/view/helimos/tasks).

## Help

```sh
helimos_visualizer --help
```

## Citation

If you use this visualizer for any academic work, please cite the original
[KISS-ICP](https://www.ipb.uni-bonn.de/wp-content/papercite-data/pdf/vizzo2023ral.pdf)
and our [HeLiMOS](https://www.arxiv.org/abs/2408.06328).
