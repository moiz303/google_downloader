import sqlalchemy
from db_session import SqlAlchemyBase


class DataBase(SqlAlchemyBase):
    __tablename__ = 'Data'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    url = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    device = sqlalchemy.Column(sqlalchemy.String, nullable=True)
