

from dataclasses import dataclass
import string
from typing import Any


@dataclass
class Node:
    state: int | str
    parent_node: Any
    action: str
    path_cost: int = 1