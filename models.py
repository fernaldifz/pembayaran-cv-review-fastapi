import sqlalchemy as _sql
import database as _database


class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    username = _sql.Column(_sql.String, unique=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)
    is_active = _sql.Column(_sql.Boolean, default=True)


class PaymentMethod(_database.Base):
    __tablename__ = "payment methods"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    payment_type = _sql.Column(_sql.String, index=True)
    name = _sql.Column(_sql.String, index=True)


class Payment(_database.Base):
    __tablename__ = "data payments"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    packet = _sql.Column(_sql.String, index=True)
    payment_method = _sql.Column(_sql.String, index=True)
    price = _sql.Column(_sql.Integer, index=True)
