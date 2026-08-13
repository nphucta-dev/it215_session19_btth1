from sqlalchemy.orm import Session
from typing import Optional
from app.models import Warehouse, Package, Waybill
from app.schemas import (
    WarehouseCreate,
    PackageCreate,
    PackageUpdate,
    WaybillCreate,
)


def create_warehouse(db: Session, warehouse_in: WarehouseCreate) -> Warehouse:
    """Tạo mới Nhà kho với giải nén dict dữ liệu bằng toán tử **"""
    try:
        db_warehouse = Warehouse(**warehouse_in.model_dump())
        db.add(db_warehouse)
        db.commit()
        db.refresh(db_warehouse)
        return db_warehouse
    except Exception as e:
        db.rollback()
        raise e


def get_warehouse_by_id(db: Session, warehouse_id: int) -> Optional[Warehouse]:
    """Lấy thông tin chi tiết Nhà kho (ORM tự động nạp liên kết packages 1-N)"""
    return db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()


def update_package(db: Session, package_id: int, package_in: PackageUpdate) -> Optional[Package]:
    """Cập nhật động thông tin Kiện hàng sử dụng model_dump(exclude_unset=True) và setattr"""
    package = db.query(Package).filter(Package.id == package_id).first()
    if not package:
        return None

    update_data = package_in.model_dump(exclude_unset=True)
    try:
        for field, value in update_data.items():
            setattr(package, field, value)
        db.commit()
        db.refresh(package)
        return package
    except Exception as e:
        db.rollback()
        raise e


def delete_waybill(db: Session, waybill_id: int) -> bool:
    """Thực hiện Hard Delete (xóa vật lý vĩnh viễn khỏi DB) đối với Waybill"""
    waybill = db.query(Waybill).filter(Waybill.id == waybill_id).first()
    if not waybill:
        return False
    try:
        db.delete(waybill)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e


# --- Helper methods for creating packages & waybills in API/Tests ---
def create_package(db: Session, package_in: PackageCreate) -> Package:
    """Tạo mới Kiện hàng (dùng để test & hỗ trợ thao tác dữ liệu)"""
    try:
        db_package = Package(**package_in.model_dump())
        db.add(db_package)
        db.commit()
        db.refresh(db_package)
        return db_package
    except Exception as e:
        db.rollback()
        raise e


def create_waybill(db: Session, waybill_in: WaybillCreate) -> Waybill:
    """Tạo mới Vận đơn chi tiết (dùng để test & hỗ trợ thao tác dữ liệu)"""
    try:
        db_waybill = Waybill(**waybill_in.model_dump())
        db.add(db_waybill)
        db.commit()
        db.refresh(db_waybill)
        return db_waybill
    except Exception as e:
        db.rollback()
        raise e
