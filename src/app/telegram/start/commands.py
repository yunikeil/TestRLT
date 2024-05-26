from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, ContextTypes

from core.settings import config

def get_start_command():
    names = ["start", "help"]

    async def command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        parse_mode="Markdown"
        
        if config.BETTER_FORMAT:
            output = f"Hi, User with id: `{update.message.from_user.id}`"
        else:
            output = f"Hi {update.message.from_user.mention_markdown()}!"
            
        await update.message.reply_text(
            text=output, parse_mode=parse_mode, 
        )
        
    return CommandHandler(command=names, callback=command)


commands_handlers = [get_start_command()]
