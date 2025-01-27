import pprint
import asyncio

import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from fsm.fsm import FSMStyleGen

logger = logging.getLogger(__name__)


class FirstOuterMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:

        logger.debug(
            'Вошли в миддлварь %s, тип события %s',
            __class__.__name__,
            event.__class__.__name__
        )

        # if data["event_update"].message.photo:
        #     #data_dict = await data["state"].get_data()
        #
        #
        #     if data.get("photo_num"):
        #         logger.debug("to_second_photo")
        #
        #     else:
        #         logger.debug("to_first_photo")
        #         data["photo_num"] = True

        await asyncio.sleep(1)
        st = await data["state"].get_state()
        logger.debug("%s", st)




        result = await handler(event, data)

        logger.debug('Выходим из миддлвари  %s', __class__.__name__)

        return result