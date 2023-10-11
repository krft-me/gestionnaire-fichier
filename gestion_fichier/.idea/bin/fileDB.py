from sqlalchemy import Integer, String, LargeBinary,BLOB
from sqlalchemy.orm import Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy,Model
from sqlalchemy.orm import DeclarativeBase
from init_database import db

class File(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique = False, nullable=False)
    userName: Mapped[str] = mapped_column(String, nullable =True)
    idConversation : Mapped[int] = mapped_column(Integer, nullable= True)
    fileContent : Mapped[str] = mapped_column(String, nullable=True)

    def __init__(self, name, userName, idConversation, fileContent ):
        self.name = name
        self.userName = userName;
        self.idConversation = idConversation
        self.fileContent = fileContent
