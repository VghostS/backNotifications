import os
import logging
import traceback
from collections import defaultdict
from typing import DefaultDict, Dict
from dotenv import load_dotenv
from telegram import Update, LabeledPrice, InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackContext
)

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Store statistics
STATS: Dict[str, DefaultDict[str, int]] = {
    'purchases': defaultdict(int),
    'refunds': defaultdict(int)
}

async def play_game(update: Update, context: CallbackContext) -> None:
    """Handle /playgame command to open game as a Mini App."""
    await update.message.reply_text(
        "Click the button below to play The Last Strip!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(
                "🎮 Launch The Last Strip",
                web_app=WebAppInfo(url="https://vkss.itch.io/tls")
            )]
        ])
    )

async def oneflask_purchase(update: Update, context: CallbackContext) -> None:
    """Direct purchase handler for OneFlask."""

    await context.bot.send_invoice(
        chat_id=update.effective_chat.id,
        title='flask_one',
        description='get One Flask',
        payload='flask_one',
        currency="XTR",
        prices=[LabeledPrice('flask_one', 1)],
        start_parameter="start_parameter"
    )
def main() -> None:
    """Start the bot."""
    try:
        application = Application.builder().token(BOT_TOKEN).build()

        # Add handlers
        application.add_handler(CommandHandler("oneflask", oneflask_purchase))

        # Add error handler
        application.add_error_handler(error_handler)

        # Start the bot
        logger.info("Bot started")
        application.run_polling()

    except Exception as e:
        logger.error(f"Error starting bot: {str(e)}")

async def error_handler(update: Update, context: CallbackContext) -> None:
    """Handle errors caused by Updates."""
    logger.error(f"Update {update} caused error {context.error}")

if __name__ == "__main__":
    main()