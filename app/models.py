from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(Integer, primary_key=True, index=True)
    warehouse_name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)

    # 1-N relationship: One Warehouse has many Packages
    packages = relationship("Package", back_populates="warehouse", cascade="all, delete-orphan")


class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True)
    package_code = Column(String(100), nullable=False, unique=True, index=True)
    weight = Column(Float, nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)

    # N-1 relationship: Belongs to one Warehouse
    warehouse = relationship("Warehouse", back_populates="packages")

    # 1-1 relationship: Possesses one Waybill (uselist=False forces single object response)
    waybill = relationship("Waybill", back_populates="package", uselist=False, cascade="all, delete-orphan")


class Waybill(Base):
    __tablename__ = "waybills"

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String(100), nullable=False, unique=True, index=True)
    shipping_status = Column(String(100), nullable=False)
    package_id = Column(Integer, ForeignKey("packages.id"), nullable=False, unique=True)

    # 1-1 relationship: Linked to one Package
    package = relationship("Package", back_populates="waybill")
