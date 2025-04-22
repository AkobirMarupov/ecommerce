from fastapi import APIRouter, HTTPException

from app.dependencies import db_dep, current_user_dep
from app.schemas.inventory import InventoryUpdate, InventoryCreate, InventoryResponse
from app.models.inventory import Inventory


router = APIRouter(
    prefix='/Inventory',
    tags=['Inventorys']
  )


@router.get('/', response_model=list[InventoryResponse])
async def inventory_all(session: db_dep):
    return session.query(Inventory).all()


@router.get('/{inventory_id}', response_model=InventoryResponse)
async def inventory_one(inventory_id: int, session: db_dep, current_user: current_user_dep):
    inventory = session.query(Inventory).filter(Inventory.id == inventory_id).first()

    if not inventory:
        raise HTTPException(status_code=404, detail="inventory not fount(yuq)")

    return inventory


@router.post('/inventory', response_model=InventoryResponse)
async def create(inventory: InventoryCreate, session: db_dep, current_user: current_user_dep):

    db_inventory = Inventory(**inventory.model_dump())

    session.add(db_inventory)
    session.commit()
    session.refresh(db_inventory)

    return db_inventory


@router.patch('/{inventory_id}', response_model= InventoryResponse)
async def update(inventory_id: int, inventory: InventoryUpdate, session: db_dep, current_user: current_user_dep):

    db_inventory = session.query(Inventory).filter(Inventory.id == inventory_id).first()

    if not db_inventory:
        raise HTTPException(status_code=404, detail="Inventory not found(yuq)!")

    for key, value in inventory.model_dump(exclude_unset=True).items():
        setattr(db_inventory, key, value)

    session.commit()
    session.refresh(db_inventory)

    return db_inventory


@router.delete('/{inventory_id}')
async def delete(inventory_id: int, session: db_dep, current_user: current_user_dep):

    db_delete = session.query(Inventory).filter(Inventory.id == inventory_id).first()

    if not db_delete:
        raise HTTPException(status_code=404, detail="Inventory not found(yuq)!")

    session.delete(db_delete)
    session.commit()
    session.refresh(db_delete)

    return db_delete








