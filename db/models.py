"""Models declarations."""

from sqlalchemy import BigInteger, ForeignKey, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base


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

    advices: Mapped[list['Advice']] = relationship(
        'Advice',
        back_populates='user',
        cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return (
            f'Пользователь с id = {self.id}: '
            f'{self.username}, {self.full_name}')


class Note(Base):
    __tablename__ = 'note'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)
    user: Mapped['User'] = relationship('User', back_populates='notes')

    def __repr__(self) -> str:
        return (f'Запись типа {self.type} у'
                f'пользователя {self.user_id}')


class Advice(Base):
    __tablename__ = 'advice'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    rating: Mapped[float] = mapped_column(Float)
    user: Mapped['User'] = relationship('User', back_populates='advices')

    def __repr__(self) -> str:
        return f'Совет {self.text} с рейтингом {self.rating}'
