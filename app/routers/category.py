from fastapi import APIRouter, HTTPException

from app.schemas.categiries import CategoryCreate, CategoryResponse, CategoryUpdate
from app.dependencies import db_dep, current_user_dep
from app.models import Category


router = APIRouter(
    prefix="/category",
    tags=["Category"]
)


@router.get('/{id}', response_model= CategoryResponse)
async def get_category(id: int, session: db_dep, current_user: current_user_dep):

    db_category = session.query(Category).filter(Category.id == id).first()

    if not db_category:
        raise HTTPException(status_code=404, detail="Kategoriya topilmadi")
    
    return db_category


@router.get('/', response_model= list[CategoryResponse])
async def get_response(session: db_dep, current_user: current_user_dep):

    categories = session.query(Category).all()

    return categories



from datetime import datetime

@router.post('/', response_model=CategoryResponse)
async def creat_category(category: CategoryCreate, session: db_dep, current_user: current_user_dep):
   
    db_add = Category(
        name=category.name,
        parent_id=None,  
        created_at=datetime.now() 
    )

    session.add(db_add)
    session.commit()
    session.refresh(db_add)

    return db_add



@router.put('/{category_id}', response_model= CategoryResponse)
async def update_db(category_id: int, category_data: CategoryUpdate, session: db_dep, current_user: current_user_dep):

    db_category = session.query(Category).filter(Category.id == category_id).first()

    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    if category_data.parent_id and category_data.parent_id != db_category.parent_id:
        db_parent = session.query(Category).filter(Category.id == category_data.parent_id).first()
        if not db_parent:
            raise HTTPException(status_code=404, detail="Categoriya topilmadi")

    for field, value in category_data.model_dump(exclude_unset=True).items():
        setattr(db_category, field, value)
    
    session.commit()
    session.refresh(db_category)

    return db_category

@router.delete('/{category_id}')
async def delete_category(category_id: int, session: db_dep, current_user: current_user_dep):

    db_delete = session.query(Category).filter(Category.id == category_id).first()

    if not db_delete:
        raise HTTPException(status_code=404, detail="Category not found")
    
    session.delete(db_delete)
    session.commit()

    return db_delete