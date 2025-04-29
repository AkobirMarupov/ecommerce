from fastapi import APIRouter, HTTPException

from app.dependencies import db_dep, current_user_dep
from app.schemas.wishlist import WishlistResponse, WishlistCreate, WishlistUpdate
from app.models.wishlist import Wishlist
from app.models.product import Product


router = APIRouter(
    prefix='/wishlist',
    tags=['Wishlist']
  )


@router.get('/', response_model=list[WishlistResponse])
async def get_all(session: db_dep, current_user: current_user_dep):
    return session.query(Wishlist).filter(Wishlist.user_id == current_user.id).all()


@router.get('/{wis_id}', response_model=WishlistResponse)
async def get_one(wis_id: int, session: db_dep, current_user: current_user_dep):
    one = session.query(Wishlist).filter(Wishlist.id == wis_id).first()

    if not one:
        raise HTTPException(status_code=404, detail='Bunday mahsulot topilmadi.')

    if one.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bunga ruxsatingiz yo‘q.")


    return one



@router.post('/create', response_model=WishlistResponse)
async def create(wislist: WishlistCreate, session: db_dep, current_user: current_user_dep):

    product = session.query(Product).filter(Product.id == wislist.product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Mahsulot topilmadi")

    new_item = Wishlist(
        user_id= current_user.id,
        product_id= wislist.product_id
    )

    session.add(new_item)
    session.commit()
    session.refresh(new_item)

    return new_item


@router.patch('/{wis_id}', response_model=WishlistResponse)
async def update(wis_id: int, session: db_dep, wislis: WishlistUpdate, current_user: current_user_dep):

    db_wislis = session.query(Wishlist).filter(Wishlist.id == wis_id).first()

    if not db_wislis:
        raise HTTPException(status_code=404, detail="Mahsulot topilmadi")

    if db_wislis.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bunga ruxsatingiz yo‘q.")

    for key, value in wislis.model_dump(exclude_unset=True).items():
        setattr(db_wislis, key, value)

    session.commit()
    session.refresh(db_wislis)

    return db_wislis



@router.delete('/{wis_id}')
async def delete(wis_id: int, session: db_dep, current_user: current_user_dep):

    db_delete = session.query(Wishlist).filter(Wishlist.id == wis_id).first()

    if not db_delete:
        raise HTTPException(status_code=404, detail="Mahsulot topilmadi")

    if db_delete.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bunga ruxsatingiz yo‘q.")


    session.delete(db_delete)
    session.commit()

    return db_delete
