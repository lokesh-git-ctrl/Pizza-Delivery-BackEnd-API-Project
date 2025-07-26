from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from models import User, Order
from schemas import OrderModel,OrderStatusModel
from database import get_db

order_router = APIRouter(
    prefix='/order',
    tags=['orders']
)


@order_router.get('/')
async def hello(Authorize: AuthJWT = Depends()):

    """
    
        ## A sample hello world route
        This returns hello world

    """

    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Token'
        )
    
    return {'message': 'Hello World'}


@order_router.post('/order', status_code=status.HTTP_201_CREATED)
async def place_an_order(
    order: OrderModel,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)  # ✅ using shared get_db
):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )

    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == current_user).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    new_order = Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity,
        user_id=user.id
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return jsonable_encoder({
        "id": new_order.id,
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "order_status": new_order.order_status
    })

@order_router.get('/orders')
async def list_all_orders(
    Authorize: AuthJWT = Depends(),
    db=Depends(get_db)
):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Token'
        )

    current_user = Authorize.get_jwt_subject()
    user = db.query(User).filter(User.username == current_user).first()

    if user and user.is_staff:
        orders = db.query(Order).all()
        return jsonable_encoder(orders)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='You are not authorized to view all orders'
    )

@order_router.get('/orders/{id}')
async def get_order_by_id(
    id: int,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)  # ✅ Inject DB session
):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Token'
        )

    user = Authorize.get_jwt_subject()

    current_user = db.query(User).filter(User.username == user).first()  # ✅ use db

    if current_user and current_user.is_staff:  # ✅ Check user exists
        order = db.query(Order).filter(Order.id == id).first()

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Order not found'
            )

        return jsonable_encoder(order)

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,  # ✅ 403 is more appropriate
        detail='User not allowed to carry out request'
    )
  # ✅ Check us_

@order_router.get('/user/orders')
async def get_user_orders(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)  # ✅ Fix here
):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Token'
        )
    
    user = Authorize.get_jwt_subject()

    current_user = db.query(User).filter(User.username == user).first()  # ✅ use db not session

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return jsonable_encoder(current_user.orders)

@order_router.get('/user/order/{id}/', response_model=OrderModel)
async def get_specific_order(
    id: int,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)  # ✅ FIX: Inject DB session
):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Token'
        )

    subject = Authorize.get_jwt_subject()

    current_user = db.query(User).filter(User.username == subject).first()  # ✅ use db

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )

    orders = current_user.orders

    for o in orders:
        if o.id == id:
            return o

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="No order with such id"
    )

@order_router.put('/order/update/{id}/')
async def update_order(
    id: int,
    order: OrderModel,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)  # ✅ Add this
):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Token'
        )

    order_to_update = db.query(Order).filter(Order.id == id).first()  # ✅ use db

    if not order_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    order_to_update.quantity = order.quantity
    order_to_update.pizza_size = order.pizza_size

    db.commit()  # ✅ use db, not session
    db.refresh(order_to_update)

    reponse = {
        "id":order_to_update.id,
        "quantity":order_to_update.quantity,
        "pizza_size":order_to_update.pizza_size,
        "order_status":order_to_update.order_status
    }

    return jsonable_encoder(reponse)


@order_router.patch('/order/update/{id}')
async def update_order_status(
    id: int,
    order: OrderStatusModel,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db)  # ✅ FIX: inject db session
):
    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Token'
        )

    username = Authorize.get_jwt_subject()

    # ✅ FIX: use User model, not Order
    current_user = db.query(User).filter(User.username == username).first()

    if not current_user or not current_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action"
        )

    order_to_update = db.query(Order).filter(Order.id == id).first()

    if not order_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    order_to_update.order_status = order.order_status

    db.commit()
    db.refresh(order_to_update)

    reponse = {
        "id":order_to_update.id,
        "quantity":order_to_update.quantity,
        "pizza_size":order_to_update.pizza_size,
        "order_status":order_to_update.order_status
    }

    return jsonable_encoder(reponse)

@order_router.delete('/order/delete/{id}/',status_code = status.HTTP_204_NO_CONTENT)
async def delete_an_order(id:int,Authorize:AuthJWT=Depends(),db: Session = Depends(get_db)):

    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Token'
        )
    
    order_to_delete = db.query(Order).filter(Order.id == id).first()

    db.delete(order_to_delete)
    db.commit()

    return order_to_delete




