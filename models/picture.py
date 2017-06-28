from sqlalchemy import Binary
from sqlalchemy import LargeBinary
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()


class Picture(Base):
	__tablename__ = "tbl_picture"

	id_picture = Column(String(36), primary_key=True)
	picture = Column(String)