from fastapi import APIRouter, HTTPException

from app.dependencies import db_dep, current_user_dep
from app.schemas.sellers import SellerCreate, SellerUpdate, SellerResponse
from app.models.seller import SellerProfile
from app.models.user import User


router = APIRouter(
    prefix='/sellers',
    tags=['Profil']
  )


@router.get('/', response_model= list[SellerResponse])
async def all_seller(session: db_dep, current_user: current_user_dep):
    return session.query(SellerProfile).all()


@router.post('/', response_model= SellerResponse)
async def create_profil(session: db_dep, profil: SellerCreate, current_user: current_user_dep):

    db_user = session.query(User).filter(User.id == profil.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Bunday user mavjud emas.")

    db_profil = SellerProfile(**profil.model_dump())

    session.add(db_profil)
    session.commit()
    session.refresh(db_profil)

    return db_profil



@router.patch('/{profil_id}', response_model= SellerResponse)
async def update_profil(profil_id: int, session: db_dep, profil_update: SellerUpdate, current_user: current_user_dep):

    db_profil = session.query(SellerProfile).filter(SellerProfile.id == profil_id).first()

    if not db_profil:
        raise HTTPException(status_code=404, detail="Bunday profil mavjud emas.")

    for key, value in profil_update.model_dump(exclude_unset=True).items():
        setattr(db_profil, key, value)

    session.commit()
    session.refresh(db_profil)

    return db_profil


@router.delete('/{profil_id}')
async def delete_profil(profil_id: int, session: db_dep, current_user: current_user_dep):

    db_delete = session.query(SellerProfile).filter(SellerProfile.id == profil_id).first()

    if not db_delete:
        raise HTTPException(status_code=404, detail="Bunday profil mavjud emas.")

    session.delete(db_delete)
    session.commit()

    return db_delete













