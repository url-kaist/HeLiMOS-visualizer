# MIT License
#
# Copyright (c) 2023 Ignacio Vizzo, Tiziano Guadagnino, Benedikt Mersch, Cyrill
# Stachniss.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import glob
import os
from pathlib import Path
from typing import Optional

import typer

from helimos_visualizer.datasets import (
    available_dataloaders,
    dataset_factory,
    jumpable_dataloaders,
    supported_file_extensions,
)
from helimos_visualizer.visualizer import Visualizer


def version_callback(value: bool):
    if value:
        import helimos_visualizer

        print(f"HeLiMOS Visualizer Version: {helimos_visualizer.__version__}")
        raise typer.Exit(0)


def guess_dataloader(data: Path, default_dataloader: str):
    if data.is_file():
        if data.name == "metadata.yaml":
            return "rosbag", data.parent  # database is in directory, not in .yml
        if data.name.split(".")[-1] in "bag":
            return "rosbag", data
        if data.name.split(".")[-1] == "pcap":
            return "ouster", data
        if data.name.split(".")[-1] == "mcap":
            return "mcap", data
    elif data.is_dir():
        if (data / "metadata.yaml").exists():
            # a directory with a metadata.yaml must be a ROS2 bagfile
            return "rosbag", data
        bagfiles = [Path(path) for path in glob.glob(os.path.join(data, "*.bag"))]
        if len(bagfiles) > 0:
            return "rosbag", bagfiles
    return default_dataloader, data


def name_callback(value: str):
    if not value:
        return value
    dl = available_dataloaders()
    if value not in dl:
        raise typer.BadParameter(f"Supported dataloaders are:\n{', '.join(dl)}")
    return value


docstring = f"""
:Automobile: HeLiMOS visualizer :person_running:\n
\b
[bold green]Examples: [/bold green]
# Your helimos folder structure is as follows:

$HOME/HeLiMOS/sequence
├──Deskewed_LiDAR
    ├── train.txt
    ├── val.txt
    ├── test.txt
    ├── Aeva
    │   ├── calib.txt
    │   ├── velodyne
    │   ├── labels
    ├── Avia
    │   ├── calib.txt
    │   ├── velodyne
    │   ├── labels
    ├── Ouster
    │   ├── calib.txt
    │   ├── velodyne
    │   ├── labels
    └── Velodyne
        ├── calib.txt
        ├── velodyne
        └── labels

# Visualize all pointclouds in the <$HOME/HeLiMOS/sequence/Deskewed_LiDAR>]
$ helimos_visualizer --sensor <Aeva, Avia, Ouster, Velodyne> --split <all, train, val, test> :open_file_folder:

"""
app = typer.Typer(add_completion=False, rich_markup_mode="rich")

@app.command(help=docstring)


def lidar_visualizer(
    data: Path = typer.Option(
        os.path.join(os.getenv("HOME"), "HeLiMOS", "KAIST05", "Deskewed_LiDAR"),
        help="The data directory used by the specified dataloader",
        show_default=False,
    ),
    
    sensor: str = typer.Option(
        'Ouster',
        help="Sensor you want to visualize e.g. 'Velodyne', 'Ouster', 'Aeva', 'Avia'",
        show_default=False,
    ),
    
    split: str = typer.Option(
        'all',
        help="The split of the data you want to visualize, e.g. 'train', 'val', 'test', 'all'",
        show_default=False,
    ),
    
    # dataloader: str = typer.Option(
    #     None,
    #     show_default=False,
    #     case_sensitive=False,
    #     autocompletion=available_dataloaders,
    #     callback=name_callback,
    #     help="[Optional] Use a specific dataloader from those supported by helimos-visualizer",
    # ),
    
    # topic: Optional[str] = typer.Option(
    #     None,
    #     "--topic",
    #     "-t",
    #     show_default=False,
    #     help="[Optional] Only valid when processing rosbag files",
    #     rich_help_panel="Additional Options",
    # ),
    
    n_scans: int = typer.Option(
        -1,
        "--n-scans",
        "-n",
        show_default=False,
        help="[Optional] Specify the number of scans to process, default is the entire dataset",
        rich_help_panel="Additional Options",
    ),
    
    jump: int = typer.Option(
        0,
        "--jump",
        "-j",
        show_default=False,
        help="[Optional] Specify if you want to start to process scans from a given starting point",
        rich_help_panel="Additional Options",
    ),
    
    # meta: Optional[Path] = typer.Option(
    #     None,
    #     "--meta",
    #     "-m",
    #     exists=True,
    #     show_default=False,
    #     help="[Optional] For Ouster pcap dataloader, specify metadata json file path explicitly",
    #     rich_help_panel="Additional Options",
    # ),
    
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        help="Show the current version of helimos-visualizer",
        callback=version_callback,
        is_eager=True,
    ),
):
    
    data = Path(os.path.join(data, sensor))
    
    
    # dataloader, data = guess_dataloader(data, default_dataloader="generic")
    dataloader, data = "generic", data

    if (jump != 0 or n_scans != -1) and dataloader not in jumpable_dataloaders():
        print(f"[WARNING] '{dataloader}' does not support '-jump' or '--n_scans'")
        print(f"[WARNING] Visualazing entire dataset")
        jump = 0
        n_scans = -1

    Visualizer(
        dataset=dataset_factory(
            dataloader=dataloader,
            data_dir=data,
            split=split,
            # Additional options
            # topic=topic,
            # meta=meta,
        ),
        n_scans=n_scans,
        jump=jump,
    ).run()


def main():
    app()
