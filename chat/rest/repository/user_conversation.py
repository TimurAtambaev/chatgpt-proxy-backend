"""Репозиторий для запросов связанных с пользователями и диалогами."""
from sqlalchemy import and_, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from chat.rest.models.message import UserMessageModel
from chat.tables.user_session_conversation import Conversation, Session, User


async def create_session(sqlalchemy_session: AsyncSession) -> int:
    """Создать новую сессию (диалог) пользователя с ChatGPT."""
    return (
        await sqlalchemy_session.execute(insert(Session).returning(Session.id))
    ).scalar()


async def get_or_create_user(
    sqlalchemy_session: AsyncSession, username: str
) -> int:
    """Получить или создать пользователя."""
    query = select(User).where(User.username == username)
    if user := (await sqlalchemy_session.execute(query)).scalar():
        return user.id
    query_insert = insert(User).values(username=username).returning(User.id)
    return (await sqlalchemy_session.execute(query_insert)).scalar()


async def get_context(
    sqlalchemy_session: AsyncSession,
    user_message: UserMessageModel,
) -> tuple[int, int, list]:
    """Получить контекст диалога пользователя с ChatGPT."""
    messages = []
    user_id = await get_or_create_user(
        sqlalchemy_session, user_message.username
    )
    if session_id := user_message.session_id:
        query = (
            select(Conversation)
            .where(
                and_(
                    Conversation.session_id == session_id,
                    Conversation.user_id == user_id,
                )
            )
            .order_by(Conversation.id)
        )
        previous_messages = (await sqlalchemy_session.execute(query)).all()
        for message in previous_messages:
            message = message._mapping["Conversation"].__dict__
            messages.append({"role": "user", "content": message["question"]})
            messages.append(
                {"role": "assistant", "content": message["answer"]}
            )
    else:
        session_id = await create_session(sqlalchemy_session)
    messages.append({"role": "user", "content": user_message.text})

    return session_id, user_id, messages


async def save_response(
    sqlalchemy_session: AsyncSession,
    text: str,
    session_id: int,
    user_id: int,
    response: str,
) -> None:
    """Сохранить запрос пользователя и ответ ChatGPT."""
    query = insert(Conversation).values(
        session_id=session_id, user_id=user_id, question=text, answer=response
    )
    await sqlalchemy_session.execute(query)
