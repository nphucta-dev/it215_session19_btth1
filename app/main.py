from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
import app.models as models
import app.schemas as schemas
import app.service as service


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Khởi tạo toàn bộ cấu trúc bảng khi ứng dụng khởi động
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Supply Chain Management API",
    description="Hệ thống Quản lý Chuỗi Cung ứng (Warehouse, Package, Waybill)",
    version="1.0.0",
    lifespan=lifespan,
)


# 1. API Tạo mới Nhà kho
@app.post(
    "/warehouses",
    response_model=schemas.WarehouseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Tạo mới Nhà kho",
)
def create_warehouse(
    warehouse_in: schemas.WarehouseCreate,
    db: Session = Depends(get_db),
):
    try:
        return service.create_warehouse(db, warehouse_in)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# 2. API Lấy chi tiết Nhà kho chứa liên kết 1-N
@app.get(
    "/warehouses/{warehouse_id}",
    response_model=schemas.WarehouseDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Lấy chi tiết Nhà kho kèm danh sách Kiện hàng",
)
def get_warehouse(
    warehouse_id: int,
    db: Session = Depends(get_db),
):
    warehouse = service.get_warehouse_by_id(db, warehouse_id)
    if not warehouse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nhà kho không tồn tại",
        )
    return warehouse


# 3. API Cập nhật động thông tin Kiện hàng
@app.patch(
    "/packages/{package_id}",
    response_model=schemas.PackageResponse,
    status_code=status.HTTP_200_OK,
    summary="Cập nhật động thông tin Kiện hàng",
)
def update_package(
    package_id: int,
    package_in: schemas.PackageUpdate,
    db: Session = Depends(get_db),
):
    try:
        updated_package = service.update_package(db, package_id, package_in)
        if not updated_package:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Kiện hàng không tồn tại",
            )
        return updated_package
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# 4. API Xóa vĩnh viễn Vận đơn
@app.delete(
    "/waybills/{waybill_id}",
    status_code=status.HTTP_200_OK,
    summary="Xóa vĩnh viễn Vận đơn",
)
def delete_waybill(
    waybill_id: int,
    db: Session = Depends(get_db),
):
    try:
        success = service.delete_waybill(db, waybill_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vận đơn không tồn tại",
            )
        return {"message": "Xóa vận đơn thành công", "waybill_id": waybill_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# --- Helper endpoints for Package and Waybill creation ---
@app.post(
    "/packages",
    response_model=schemas.PackageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Tạo mới Kiện hàng",
)
def create_package(
    package_in: schemas.PackageCreate,
    db: Session = Depends(get_db),
):
    try:
        return service.create_package(db, package_in)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@app.post(
    "/waybills",
    response_model=schemas.WaybillResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Tạo mới Vận đơn",
)
def create_waybill(
    waybill_in: schemas.WaybillCreate,
    db: Session = Depends(get_db),
):
    try:
        return service.create_waybill(db, waybill_in)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
