from pathlib import Path

import typer

import definitions
from src.config.load import load_config_from_path
from src.data.generate import generate_all_datasets
from src.models.training import train_from_config

app = typer.Typer()


@app.command()
def train(config_filepath: Path = definitions.ROOT_DIR / "config.yaml"):
    """
    Train a neural network to estimate the tomographic reconstruction. The used dataset, model and other configurations are defined in
    config.yaml. You can find more information about the default configuration in src/config/config.py.
    :param config_filepath: The configuration file (yaml) which determines the (hyper)parameters used for training
    """
    config = load_config_from_path(config_filepath)
    train_from_config(config)


@app.command()
def generate_dataset(shot_no: int, count: int):
    """
    Generate a synthetic dataset to train the networks on. The shot_no is used to determine which geometry matrix to use, and count defines
    the number of training samples to create. The number of validation and test samples are 20% of the number of training samples.
    """
    generate_all_datasets(shot_no, count)


if __name__ == "__main__":
    app()