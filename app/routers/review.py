from fastapi import APIRouter, HTTPException

from app.schemas.review import *
from app.dependencies import db_dep, current_user_dep
from app.models import *



router = APIRouter(
    prefix='/review',
    tags=['Review']
)



@router.get('/', response_model=list[RewievResponse])
async def get_reviews(session: db_dep):
    return session.query(Review).all()




@router.get('/{review_id}', response_model=RewievResponse)
async def get_review(review_id: int, session: db_dep):
    db_review = session.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail='Review not found')
    return db_review




@router.post('/', response_model=RewievResponse)
async def create_review(review: RewievCreate, session: db_dep, current_user: current_user_dep):

    product = session.query(Product).filter(Product.id == review.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    create = Review(
        **review.model_dump(),
        user_id=current_user.id
    )

    session.add(create)
    session.commit()
    session.refresh(create)

    return create




@router.patch('/{review_id}/update', response_model=RewievResponse)
async def update_review(review_id: int, session: db_dep, current_user: current_user_dep, review_c: RewievUpdate):
    review_update = session.query(Review).filter(Review.id == review_id).first()
    if not review_update:
        raise HTTPException(status_code=404, detail="Review with this ID not found.")

    if review_c.product_id:
        product = session.query(Product).filter(Product.id == review_c.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="New product ID is invalid.")
        review_update.product_id = review_c.product_id

    review_update.rating = review_c.rating if review_c.rating is not None else review_update.rating
    review_update.comment = review_c.comment if review_c.comment is not None else review_update.comment

    session.commit()
    session.refresh(review_update)
    return review_update



@router.delete('/{review_id}')
async def delete_review(review_id: int, current_user: current_user_dep, session: db_dep):
    review_delete = session.query(Review).filter(Review.id == review_id).first()
    if not review_delete:
        raise HTTPException(status_code=404, detail="Review not found.")
    session.delete(review_delete)
    session.commit()
    return {"detail": "Review deleted successfully"}
