from typing import List, Optional
from ..models.car_model import Car
from ..db.mongo import get_db, get_next_sequence

class CarService:
    # Do NOT touch Mongo in __init__ anymore
    def __init__(self) -> None:
        pass

    @property
    def collection(self):
        # Lazily get the collection after init_mongo() has run
        return get_db()["cars"]

    async def create(self, car: Car) -> Car:
        data = car.model_dump()
        if data.get("id") is None:
            data["id"] = await get_next_sequence("car_id")
        data["_id"] = data["id"]
        await self.collection.insert_one(data)
        data.pop("_id", None)
        return Car.model_validate(data)

    async def list(self, limit: int = 10, offset: int = 0) -> List[Car]:
        cursor = self.collection.find({}, sort=[("id", 1)]).skip(offset).limit(limit)
        items = []
        async for doc in cursor:
            doc.pop("_id", None)
            items.append(Car.model_validate(doc))
        return items

    async def get(self, car_id: int) -> Optional[Car]:
        doc = await self.collection.find_one({"_id": car_id})
        if not doc:
            return None
        doc.pop("_id", None)
        return Car.model_validate(doc)

    async def update(self, car_id: int, car: Car) -> Optional[Car]:
        payload = car.model_dump()
        payload["id"] = car_id
        payload["_id"] = car_id
        res = await self.collection.replace_one({"_id": car_id}, payload, upsert=False)
        if res.matched_count == 0:
            return None
        payload.pop("_id", None)
        return Car.model_validate(payload)

    async def delete(self, car_id: int) -> bool:
        res = await self.collection.delete_one({"_id": car_id})
        return res.deleted_count == 1
