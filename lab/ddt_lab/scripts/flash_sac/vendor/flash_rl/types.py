from typing import TYPE_CHECKING, Any, Union

import numpy as np
import numpy.typing as npt
import torch

NDArray = npt.NDArray[Any]
F32NDArray = npt.NDArray[np.float32]
if TYPE_CHECKING:
    import jax.numpy as jnp
    Tensor = Union[NDArray, jnp.ndarray, torch.Tensor]
else:
    Tensor = Union[NDArray, torch.Tensor]
