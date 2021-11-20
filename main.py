from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, status
import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
import services as _services
import schemas as _schemas
from typing import List
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

app = _fastapi.FastAPI()
_services.create_database()


@app.get('/', tags=["root"])
async def read_root():
    return {"Message": "Welcome! add '/docs' at the end of URL to open Swagger UI"}


@app.post("/users", response_model=_schemas.User, tags=["user"])
def create_user(
    user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = _services.get_user_by_username(db=db, username=user.username)
    if db_user:
        raise _fastapi.HTTPException(
            status_code=400, detail="username is not available!"
        )
    return _services.create_user(db=db, user=user)


@app.get("/users", response_model=List[_schemas.User], tags=["user"])
def read_all_users(
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    users = _services.get_users(db=db)
    return users


@app.get("/users/{user_id}", response_model=_schemas.User, tags=["user"])
def read_user(user_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this user does not exist"
        )
    return db_user


@app.delete("/user/{user_id}", tags=["user"])
def delete_user(user_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    _services.delete_user(db=db, user_id=user_id)
    return {"message": f"successfully deleted data user with id: {user_id}"}


@app.post("/token", response_model=_schemas.Token, tags=["user"])
async def login_for_access_token(form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
                                 db: _orm.Session = _fastapi.Depends(_services.get_db)):
    user = _services.authenticate_user(
        form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(hours=_services.ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = _services.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/paymentMethod", response_model=_schemas.PaymentMethod, tags=["payment method"])
def create_payment_method(
        payment_method: _schemas.PaymentMethodCreate, db: _orm.Session = _fastapi.Depends(_services.get_db), token: str = Depends(_services.oauth2schema)):
    return _services.create_payment_method(db=db, payment_method=payment_method)


@app.get("/paymentMethod", response_model=List[_schemas.PaymentMethod], tags=["payment method"])
def read_all_payment_method(
    db: _orm.Session = _fastapi.Depends(_services.get_db), token: str = Depends(_services.oauth2schema)
):
    payment_methods = _services.get_payment_methods(db=db)
    return payment_methods


@app.get("/paymentMethod/{payment_method_id}", response_model=_schemas.PaymentMethod, tags=["payment method"])
def read_payment_method(payment_method_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db), token: str = Depends(_services.oauth2schema)):
    db_payment_method = _services.get_payment_method(
        db=db, payment_method_id=payment_method_id)
    if db_payment_method is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="Payment method is not available!"
        )
    return db_payment_method


@app.delete("/paymentMethod/{payment_method_id}", tags=["payment method"])
def delete_payment_method(payment_method_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db), token: str = Depends(_services.oauth2schema)):
    _services.delete_payment_method(db=db, payment_method_id=payment_method_id)
    return {"message": f"successfully deleted payment method with id: {payment_method_id}"}


@app.put("/paymentMethod/{payment_method_id}", response_model=_schemas.PaymentMethod, tags=["payment method"])
def update_payment_method(
    payment_method_id: int,
    payment_method: _schemas.PaymentMethodCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    token: str = Depends(_services.oauth2schema)
):
    return _services.update_payment_method(db=db, payment_method=payment_method, payment_method_id=payment_method_id)


@app.post("/payment", response_model=_schemas.Payment, tags=["payment"])
def create_payment(
        payment: _schemas.PaymentCreate, db: _orm.Session = _fastapi.Depends(_services.get_db), token: str = Depends(_services.oauth2schema)):
    return _services.create_payment(db=db, payment=payment)


@app.get("/payment", response_model=List[_schemas.Payment], tags=["payment"])
def read_all_payment(
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    token: str = Depends(_services.oauth2schema)
):
    payment = _services.get_payments(db=db)
    return payment


@app.get("/payment/{payment_id}", response_model=_schemas.Payment, tags=["payment"])
def read_payment(payment_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db), token: str = Depends(_services.oauth2schema)):
    db_payment = _services.get_payment(
        db=db, payment_id=payment_id)
    if db_payment is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="Data payment is not available!"
        )
    return db_payment


@app.delete("/payment/{payment_id}", tags=["payment"])
def delete_payment(payment_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db), token: str = Depends(_services.oauth2schema)):
    _services.delete_payment(db=db, payment_id=payment_id)
    return {"message": f"successfully deleted data payment with id: {payment_id}"}


@app.put("/payment/{payment_id}", response_model=_schemas.Payment, tags=["payment"])
def update_payment(
    payment_id: int,
    payment: _schemas.PaymentCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    token: str = Depends(_services.oauth2schema)
):
    return _services.update_payment(db=db, payment=payment, payment_id=payment_id)
