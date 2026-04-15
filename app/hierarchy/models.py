from dataclasses import dataclass, field

SENSOR_VIBRATION = "vibration"
SENSOR_ENERGY = "energy"

STATUS_OPERATING = "operating"
STATUS_ALERT = "alert"

NODE_TYPE_ROOT = "root"
NODE_TYPE_LOCATION = "location"
NODE_TYPE_ASSET = "asset"
NODE_TYPE_COMPONENT = "component"

@dataclass
class Location:
    id: str
    name: str
    parent_id: str | None


@dataclass
class Asset:
    id: str
    name: str
    location_id: str | None
    parent_id: str | None


@dataclass
class Component:
    id: str
    name: str
    parent_id: str | None
    sensor_type: str
    status: str

@dataclass
class TreeNode:
    id: str = ""
    name: str = ""
    type: str = ""
    children: list["TreeNode"] = field(default_factory=list)
    sensor_type: str = ""
    status: str = ""
    location_id: str = ""
    parent_id: str = ""