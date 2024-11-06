"""Models declarations."""

import enum

from sqlalchemy import BigInteger, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base


class Kind(enum.Enum):
    helptip: str
    mood: str
    selfesteem: str


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    full_name: Mapped[str] = mapped_column(String, nullable=True)

    notes: Mapped[list['Note']] = relationship(
        'Note',
        back_populates='user',
        cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return (
            f'Пользователь с id = {self.id}:'
            f'{self.__name__}, {self.full_name}')


class Note(Base):
    __tablename__ = 'note'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    kind: Mapped[str] = mapped_column(Enum(Kind))
    user: Mapped['User'] = relationship('User', back_populates='notes')

    def __repr__(self) -> str:
        return (f'Запись типа {self.kind} у'
                f'пользователя {self.user_id}')
