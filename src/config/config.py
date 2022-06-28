from typing import List, Optional, Tuple
from pathlib import Path
from pydantic import BaseModel
import tensorflow as tf
import definitions


class BaseConfigModel(BaseModel):
    def __getitem__(self, item):
        return getattr(self, item)


class DatasetConfig(BaseConfigModel):
    shot_no: int
    batch_size: int = 32
    noise: dict = {}
    copy_input_to_output: bool = False

    @property
    def path(self) -> Path:
        return Path("processed") / "mantis" / str(self.shot_no)

    @property
    def full_path(self) -> Path:
        return definitions.DATA_DIR / self.path


class ModelConfig(BaseConfigModel):
    name: str
    shot_no: int

    encoder_filters: List[int] = [64, 64, 64, 128, 128, 128]
    decoder_filters: List[int] = [128, 128, 128, 64, 64, 64]
    bottleneck_filters: List[int] = [128]

    activation_function: str = "relu"
    final_activation_function: str = "relu"

    double_conv: bool = False
    unfolded_intermediate_output_loss: bool = False

    normalization_layer: str = "instance_normalization"
    mu: float = 1
    n_iterations: Optional[int] = None
    input_shape: Tuple[int, int] = None
    output_shape: Tuple[int, int] = None

    def set_shape_from_ds(self, dataset: tf.data.Dataset):
        sample_image, sample_inversion = dataset.__iter__().next()
        self.input_shape = (sample_image.shape[1], sample_image.shape[2])
        self.output_shape = (sample_inversion.shape[1], sample_inversion.shape[2])


class TrainingConfig(BaseConfigModel):
    epochs: int = 20
    optimizer: str = "adam"
    optimizer_params: dict = {}
    loss_function: str = "mse"
    cycle_loss: bool = False


class Config(BaseConfigModel):
    dataset: DatasetConfig
    model: ModelConfig
    training: TrainingConfig = TrainingConfig()