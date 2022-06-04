from functools import partial
from pathlib import Path
from typing import Any, Callable, List

import pytest
from omegaconf import OmegaConf
from torch import nn

from oml.const import CONFIGS_PATH
from oml.registry.losses import get_criterion_by_cfg
from oml.registry.miners import get_miner_by_cfg
from oml.registry.models import get_extractor_by_cfg
from oml.registry.optimizers import get_optimizer_by_cfg
from oml.utils.misc import TCfg


def create_objects_via_yamls(path_to_folder: Path, factory_fun: Callable[[TCfg], Any]) -> List[Any]:
    objs = []
    for cfg_path in path_to_folder.glob("**/*.yaml"):
        with open(cfg_path, "r") as f:
            cfg = OmegaConf.load(f)

        objs.append(factory_fun(cfg))

    print(f"We created {len(objs)} objects using configs in {path_to_folder}")
    return objs


@pytest.mark.parametrize(
    "folder_name,factory_fun",
    [
        ("model", get_extractor_by_cfg),
        ("criterion", get_criterion_by_cfg),
        ("miner", get_miner_by_cfg),
        ("optimizer", partial(get_optimizer_by_cfg, params=list(nn.Linear(10, 20).parameters()))),
    ],
)
def test_registry(folder_name: str, factory_fun: Callable[[TCfg], Any]) -> None:
    create_objects_via_yamls(CONFIGS_PATH / folder_name, factory_fun)
    assert True
