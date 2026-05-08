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
import os
from pathlib import Path
from typing import Optional

import typer

from helimos_visualizer.datasets import dataset_factory, jumpable_dataloaders
from helimos_visualizer.visualizer import Visualizer


def version_callback(value: bool):
    if value:
        import helimos_visualizer

        print(f"HeLiMOS Visualizer Version: {helimos_visualizer.__version__}")
        raise typer.Exit(0)


docstring = """
:Automobile: HeLiMOS visualizer :person_running:\n
\b
[bold green]Examples: [/bold green]
# Your helimos folder structure is as follows:

$HOME/HeLiMOS/{sequence}
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

# Visualize all pointclouds in the <$HOME/HeLiMOS/sequence/Deskewed_LiDAR>]
$ helimos_visualizer --sensor <Aeva, Avia, Ouster, Velodyne> --split <all, train, val, test> :open_file_folder:

"""
app = typer.Typer(add_completion=False, rich_markup_mode="rich")


@app.command(help=docstring)
def helimos_visualizer(
    data: Path = typer.Option(
        os.path.join(os.getenv("HOME"), "HeLiMOS", "KAIST05", "Deskewed_LiDAR"),
        help="The data directory used by the specified dataloader",
        show_default=False,
    ),
    sensor: str = typer.Option(
        "Ouster",
        help="Sensor you want to visualize e.g. 'Velodyne', 'Ouster', 'Aeva', 'Avia'",
        show_default=False,
    ),
    split: str = typer.Option(
        "all",
        help="The split of the data you want to visualize, e.g. 'train', 'val', 'test', 'all'",
        show_default=False,
    ),
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
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        help="Show the current version of helimos-visualizer",
        callback=version_callback,
        is_eager=True,
    ),
):
    data = Path(os.path.join(data, sensor))
    dataloader = "generic"

    if (jump != 0 or n_scans != -1) and dataloader not in jumpable_dataloaders():
        print(f"[WARNING] '{dataloader}' does not support '-jump' or '--n_scans'")
        print(f"[WARNING] Visualizing entire dataset")
        jump = 0
        n_scans = -1

    Visualizer(
        dataset=dataset_factory(
            dataloader=dataloader,
            data_dir=data,
            split=split,
        ),
        n_scans=n_scans,
        jump=jump,
    ).run()


def main():
    app()
