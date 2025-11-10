from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from ..auth.auth import authenticate
from ..models.car_model import Car
from ..services.car_service import CarService

router = APIRouter()
service = CarService()

@router.post("/cars", response_model=Car, status_code=status.HTTP_201_CREATED)
async def create_car(car: Car, _: str = Depends(authenticate)) -> Car:
    return await service.create(car)

@router.get("/cars", response_model=List[Car])
async def list_cars(
    _: str = Depends(authenticate),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> List[Car]:
    return await service.list(limit=limit, offset=offset)

@router.get("/cars/{car_id}", response_model=Car)
async def get_car(car_id: int, _: str = Depends(authenticate)) -> Car:
    car = await service.get(car_id)
    if car is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    return car

@router.put("/cars/{car_id}", response_model=Car)
async def update_car(car_id: int, car: Car, _: str = Depends(authenticate)) -> Car:
    updated = await service.update(car_id, car)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    return updated

@router.delete("/cars/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(car_id: int, _: str = Depends(authenticate)) -> None:
    deleted = await service.delete(car_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    return None
