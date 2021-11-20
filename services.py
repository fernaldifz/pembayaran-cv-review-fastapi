from datetime import datetime, timedelta
from typing import Optional
import sqlalchemy.orm as _orm
import models as _models
import schemas as _schemas
import database as _database
from passlib.context import CryptContext
import fastapi.security as _security
import jwt as jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/token")

SECRET_KEY = "5dd606c980b456f773dfb2993fc4b0f517a2eaebf6b3b129e1d4c4604e29a9d8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 1


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(db: _orm.Session, user_id: int):
    return db.query(_models.User).filter(_models.User.id == user_id).first()


def get_user_by_username(db: _orm.Session, username: str):
    return db.query(_models.User).filter(_models.User.username == username).first()


def get_users(db: _orm.Session):
    return db.query(_models.User).all()


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(db: _orm.Session, user: _schemas.UserCreate):
    db_user = _models.User(
        username=user.username, email=user.email, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: _orm.Session, user_id: int):
    db.query(_models.User).filter(
        _models.User.id == user_id).delete()
    db.commit()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db: _orm.Session):
    user = get_user_by_username(db=db, username=username)

    if not user:
        return False

    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_payment_method(db: _orm.Session, payment_method: _schemas.PaymentMethodCreate):
    db_payment_method = _models.PaymentMethod(
        payment_type=payment_method.payment_type, name=payment_method.name)
    db.add(db_payment_method)
    db.commit()
    db.refresh(db_payment_method)
    return db_payment_method


def get_payment_methods(db: _orm.Session):
    return db.query(_models.PaymentMethod).all()


def get_payment_method(db: _orm.Session, payment_method_id: int):
    return db.query(_models.PaymentMethod).filter(_models.PaymentMethod.id == payment_method_id).first()


def delete_payment_method(db: _orm.Session, payment_method_id: int):
    db.query(_models.PaymentMethod).filter(
        _models.PaymentMethod.id == payment_method_id).delete()
    db.commit()


def update_payment_method(db: _orm.Session, payment_method_id: int, payment_method: _schemas.PaymentMethodCreate):
    db_payment_method = get_payment_method(
        db=db, payment_method_id=payment_method_id)
    db_payment_method.payment_type = payment_method.payment_type
    db_payment_method.name = payment_method.name
    db.commit()
    db.refresh(db_payment_method)
    return db_payment_method


def create_payment(db: _orm.Session, payment: _schemas.PaymentCreate):
    db_payment = _models.Payment(
        packet=payment.packet, payment_method=payment.payment_method, price=payment.price)
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


def get_payments(db: _orm.Session):
    return db.query(_models.Payment).all()


def get_payment(db: _orm.Session, payment_id: int):
    return db.query(_models.Payment).filter(_models.Payment.id == payment_id).first()


def delete_payment(db: _orm.Session, payment_id: int):
    db.query(_models.Payment).filter(
        _models.Payment.id == payment_id).delete()
    db.commit()


def update_payment(db: _orm.Session, payment_id: int, payment: _schemas.PaymentCreate):
    db_payment = get_payment(
        db=db, payment_id=payment_id)
    db_payment.packet = payment.packet
    db_payment.payment_method = payment.payment_method
    db_payment.price = payment.price

    db.commit()
    db.refresh(db_payment)
    return db_payment
