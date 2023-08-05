# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# pyre-strict

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Production:
    name: str
    children: str
    version: Optional[str]

    def __str__(self) -> str:
        return f"{self.name}: {self.children}"
