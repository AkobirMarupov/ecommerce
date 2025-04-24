from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from sqlalchemy.orm import Session
import shutil
import uuid
import os
from app.schemas.image import  ProductMediaUpdate, ProductMediaResponse
from app.models.product_media import ProductImage
from app.models.user import User
from app.dependencies import db_dep, current_user_dep, get_db, get_current_user



router = APIRouter(
    prefix='/product_images',
    tags=['ProductImages']
)





@router.get('/', response_model=list[ProductMediaResponse])
async def root_all(session: db_dep, current_user: current_user_dep):
    return session.query(ProductImage).all()


@router.get('/{images_id}', response_model=ProductMediaResponse)
async def images_one(images_id: int, session: db_dep, current_user: current_user_dep):

    db_images = session.query(ProductImage).filter(ProductImage.id == images_id).first()

    if not db_images:
        raise HTTPException(status_code=404, detail='Bunday id dagi product yuq yoki rasm yuklanmagan.')

    return db_images


# @router.post("/upload", response_model=ProductMediaResponse)
# async def upload_image(
#     product_id: int,
#     session: db_dep,
#     current_user: current_user_dep
# ):
#
#
#
#     session.add(new_image)
#     session.commit()
#     session.refresh(new_image)
#
#     return new_image


@router.patch('/update/{product_id}', response_model= ProductMediaResponse)
async def update_image(product_id: int, session: db_dep, current_user: current_user_dep, product_image: ProductMediaUpdate):

    db_image = session.query(ProductImage).filter(ProductImage.product_id == product_id).first()

    if not db_image:
        raise HTTPException(status_code=404, detail="Rasm topilmadi.")

    for key, value in product_image.model_dump(exclude_unset=True).items():
        setattr(db_image, key, value)

    session.commit()
    session.refresh(db_image)

    return db_image


@router.delete('/delete/{productimage_id}')
async def delete_image(productimage_id: int, session: db_dep, current_user: current_user_dep):

    db_productimage = session.query(ProductImage).filter(ProductImage.id == productimage_id).first()

    if not db_productimage:
        raise HTTPException(status_code=404, detail='Bunday id dagi product yuq yoki rasm yuklanmagan.')

    file_path = db_productimage.image_url.lstrip("/")
    if os.path.exists(file_path):
        os.remove(file_path)

    session.delete(db_productimage)
    session.commit()

    return {"detail": "Rasm muvaffaqiyatli o'chirildi."}



















