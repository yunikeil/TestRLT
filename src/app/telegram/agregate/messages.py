import json
import logging
from uuid import uuid4
from io import BytesIO

import telegram
from telegram import Update, InputFile
from telegram.ext import filters, MessageHandler, ContextTypes

from app.services.mongodata import aggregate_salary_data
from app.schemas.input import InputData
from core.settings import config


logger = logging.getLogger("telegram")


def get_agregate_message_handler():
    # Тут можно расписать фильтер через регулярное выражение 
    #  и после добавить fallbacks на остальной текст, однако я решил не усложнять
    pattern = filters.TEXT

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        parse_mode = None
        
        try:
            input_validated = InputData.model_validate_json(update.message.text)
        except (ValueError, TypeError) as ex:
            output = 'Невалидный запос. Пример запроса:\n' \
                '{"dt_from": "2022-09-01T00:00:00", "dt_upto":' \
                '"2022-12-31T23:59:00", "group_type": "month"}'
        except BaseException as ex:
            error_id = uuid4()
            logger.exception(ex)
            logger.debug(f"ErrorId: {error_id}")
            output = "Something went wrong, we are already looking for a problem.\n" \
                f"ErrorId: `{error_id}`"
            parse_mode = "Markdown"
        else:
            processed_data = await aggregate_salary_data(input_validated)
            if config.BETTER_FORMAT:
                output = f"```json\n{json.dumps(processed_data, indent=4)}```"
                parse_mode = "Markdown"
            else:
                output = json.dumps(processed_data)
        
        try:
            await update.message.reply_text(text=output, parse_mode=parse_mode)
        except telegram.error.BadRequest:
            # Немного костыльненько, но думаю не сильно
            output_md_deleted = output.replace("```json", "").replace("```", "")
            file_like_object = BytesIO(output_md_deleted.encode('utf-8'))
            file_like_object.name = 'agregated.json'
            await update.message.reply_document(document=InputFile(file_like_object))
        except BaseException as ex:
            logger.critical(ex)
        
    return MessageHandler(pattern, callback)


messages_handlers = [get_agregate_message_handler()]
