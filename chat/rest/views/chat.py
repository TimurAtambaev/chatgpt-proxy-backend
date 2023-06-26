"""Модуль с представлениями обработки запросов."""
from typing import Optional

import openai
from fastapi import HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from loguru import logger
from starlette import status

from chat.config import settings
from chat.db import async_session
from chat.rest.models.message import ResponseGPTModelSession, UserMessageModel
from chat.rest.repository.user_conversation import get_context, save_response

router = InferringRouter()


@cbv(router)
class Proxy:
    """Представление для обработки и перенаправления запросов к ChatGPT."""

    @router.post("/chat-gpt", response_model=ResponseGPTModelSession)
    async def proxy_chat_gpt(
        self, user_message: UserMessageModel
    ):  # noqa ANN201
        """Проксировать запрос к ChatGPT с передачей контекста диалога.

        Вернуть массив вопросов и ответов в рамках текущего диалога (сессии).
        """
        async with async_session() as sqlalchemy_session:
            try:
                session_id, user_id, messages = await get_context(
                    sqlalchemy_session, user_message
                )
                response = self.get_chat_gpt_response(messages)
                if not response:
                    return ResponseGPTModelSession(
                        messages=messages, session_id=session_id
                    )
                await save_response(
                    sqlalchemy_session,
                    user_message.text,
                    session_id,
                    user_id,
                    response,
                )
                await sqlalchemy_session.commit()

                messages.append({"role": "assistant", "content": response})
                return ResponseGPTModelSession(
                    messages=messages, session_id=session_id
                )
            except openai.error.InvalidRequestError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Превышено максимальное число токенов в этом "
                    "диалоге. Пожалуйста, начните новый диалог.",
                )
            except Exception as exc:
                logger.error(exc)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Внутренняя ошибка сервера. В случае повторного "
                    "возникновения обратитесь к разработчикам.",
                )

    def get_chat_gpt_response(self, messages: list) -> Optional[str]:
        """Получить ответ от ChatGPT с передачей контекста диалога."""
        try:
            response = openai.ChatCompletion.create(
                model=settings.GPT_MODEL,
                messages=messages,
                temperature=settings.GPT_TEMPERATURE,
            )
            return response["choices"][0]["message"]["content"]
        except openai.error.InvalidRequestError as err:
            logger.error(err)
            raise err
        except Exception as err:
            logger.error(err)
        return None
