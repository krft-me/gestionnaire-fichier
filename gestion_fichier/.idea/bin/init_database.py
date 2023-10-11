from sqlalchemy import Integer, String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy,Model
from sqlalchemy.orm import DeclarativeBase

class GenericModel(Model):
    @classmethod
    def get(cls, id):
        try:
            return cls.query.filter_by(id=id).first()
        except Exception:
            return None

    @classmethod
    def all(cls, sortby=None):
        if sortby:
            return cls.query.order_by(sortby).all()
        return cls.query.all()

    @classmethod
    def remove(cls, id):
        try:
            cls.query.filter_by(id=id).first().remove()
            return True
        except Exception:
            return False

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception:
            db.session.commit()
            return False

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



db = SQLAlchemy(model_class=GenericModel)

