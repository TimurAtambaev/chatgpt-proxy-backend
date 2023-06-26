"""Модели таблиц сессий, пользователей, диалогов."""
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """Модель пользователей."""

    __tablename__ = "user"

    id = sa.Column(  # noqa A003
        "id", sa.Integer, primary_key=True, autoincrement=True
    )
    username = sa.Column("username", sa.String, nullable=False)


class Session(Base):
    """Модель сессий с ChatGPT."""

    __tablename__ = "session"

    id = sa.Column(  # noqa A003
        "id", sa.Integer, primary_key=True, autoincrement=True
    )


class Conversation(Base):
    """Модель диалогов с ChatGPT."""

    __tablename__ = "conversation"

    id = sa.Column(  # noqa A003
        "id", sa.Integer, primary_key=True, autoincrement=True
    )
    session_id = sa.Column(
        "session_id", sa.ForeignKey("session.id"), nullable=False
    )
    user_id = sa.Column("user_id", sa.ForeignKey("user.id"), nullable=False)
    question = sa.Column("question", sa.Text(), nullable=False)
    answer = sa.Column("answer", sa.Text(), nullable=False)
    created_at = sa.Column(  # noqa E731
        "created_at", sa.TIMESTAMP, server_default=sa.func.now()
    )
