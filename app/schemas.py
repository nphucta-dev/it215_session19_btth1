from pydantic import BaseModel, ConfigDict
from typing import List, Optional


# --- Waybill Schemas ---
class WaybillBase(BaseModel):
    tracking_number: str
    shipping_status: str


class WaybillCreate(WaybillBase):
    package_id: int


class WaybillResponse(WaybillBase):
    id: int
    package_id: int

    model_config = ConfigDict(from_attributes=True)


# --- Package Schemas ---
class PackageBase(BaseModel):
    package_code: str
    weight: float


class PackageCreate(PackageBase):
    warehouse_id: int


class PackageResponse(PackageBase):
    id: int
    warehouse_id: int
    waybill: Optional[WaybillResponse] = None

    model_config = ConfigDict(from_attributes=True)


class PackageUpdate(BaseModel):
    package_code: Optional[str] = None
    weight: Optional[float] = None
    warehouse_id: Optional[int] = None


# --- Warehouse Schemas ---
class WarehouseCreate(BaseModel):
    warehouse_name: str
    location: str


class WarehouseResponse(WarehouseCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class WarehouseDetailResponse(WarehouseResponse):
    packages: List[PackageResponse] = []

    model_config = ConfigDict(from_attributes=True)
