import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, LabeledPrice, Message
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    PreCheckoutQueryHandler,
    MessageHandler,
    filters,
    CallbackContext
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Hardcoded item data
FLASK_ONE = {
    'id': 'flask_one',
    'name': '1 Flask',
    'price': 1,
    'description': 'One Flask for 1 Star',
    'secret': 'FLASKONE'
}

async def start(update: Update, context: CallbackContext) -> None:
    """Handle /start command to introduce the bot and offer game launch."""
    logger.info("Received /start command")
    await update.message.reply_photo(
        photo="https://github.com/VghostS/backNotifications/blob/main/home.jpg?raw=true",
        caption="Welcome to The Last Strip \nCollect coins, Upgrade your Character and Never Stop\n \nClick the button below to play The Last Strip!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(
                "🎮 Launch The Last Strip",
                web_app=WebAppInfo(url="https://vghosts.github.io/Gmae/")
            )]
        ])
    )


async def oneflask_purchase(update: Update, context: CallbackContext) -> None:
    """Direct purchase handler for OneFlask."""
    await update.message.reply_text(
        "You are buying one flask for one star!")

    # Create a single confirmation button for purchase
    keyboard = [
        [InlineKeyboardButton(
            f"Confirm Purchase: {FLASK_ONE['name']} - {FLASK_ONE['price']} ⭐",
            callback_data=FLASK_ONE['id']
        )]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Item: {FLASK_ONE['name']}\n"
        f"Description: {FLASK_ONE['description']}\n"
        f"Price: {FLASK_ONE['price']} ⭐\n\n"
        "Click the button below to purchase:",
        reply_markup=reply_markup
    )


async def button_handler(update: Update, context: CallbackContext) -> None:
    """Handle button clicks for item selection."""
    query = update.callback_query
    if not query or not query.message:
        return

    try:
        await query.answer()

        item_id = query.data
        # Only handle flask_one for now
        if item_id == FLASK_ONE['id']:
            item = FLASK_ONE
        else:
            await query.message.reply_text("Item not available.")
            return

        # Make sure message exists before trying to use it
        if not isinstance(query.message, Message):
            return

        await context.bot.send_invoice(
            chat_id=query.message.chat_id,
            title=item['name'],
            description=item['description'],
            payload=item_id,
            provider_token="",  # Empty for digital goods
            currency="XTR",  # Telegram Stars currency code
            prices=[LabeledPrice(item['name'], int(item['price']))],
            start_parameter="start_parameter"
        )

    except Exception as e:
        logger.error(f"Error in button_handler: {str(e)}")
        if query and query.message and isinstance(query.message, Message):
            await query.message.reply_text(
                "Sorry, something went wrong while processing your request."
            )


async def precheckout_callback(update: Update, context: CallbackContext) -> None:
    """Handle pre-checkout queries."""
    query = update.pre_checkout_query
    if query.invoice_payload == FLASK_ONE['id']:
        await query.answer(ok=True)
    else:
        await query.answer(ok=False, error_message="Something went wrong...")


async def successful_payment_callback(update: Update, context: CallbackContext) -> None:
    """Handle successful payments."""
    payment = update.message.successful_payment
    item_id = payment.invoice_payload

    # Only handle flask_one for now
    if item_id == FLASK_ONE['id']:
        item = FLASK_ONE
    else:
        await update.message.reply_text("Item not recognized.")
        return

    user_id = update.effective_user.id

    logger.info(
        f"Successful payment from user {user_id} "
        f"for item {item_id} (charge_id: {payment.telegram_payment_charge_id})"
    )

    await update.message.reply_text(
        f"Thank you for your purchase! 🎉\n\n"
        f"Here's your secret code for {item['name']}:\n"
        f"`{item['secret']}`\n\n"
        f"To get a refund, use this command:\n"
        f"`/refund {payment.telegram_payment_charge_id}`\n\n"
        "Save this message to request a refund later if needed.",
        parse_mode='Markdown'
    )


async def error_handler(update: Update, context: CallbackContext) -> None:
    """Handle errors caused by Updates."""
    logger.error(f"Update {update} caused error {context.error}")


def main() -> None:
    """Start the bot."""
    try:
        application = Application.builder().token(BOT_TOKEN).build()

        # Add only the necessary handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("oneflask", oneflask_purchase))
        application.add_handler(CallbackQueryHandler(button_handler))
        application.add_handler(PreCheckoutQueryHandler(precheckout_callback))
        application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))

        # Add error handler
        application.add_error_handler(error_handler)

        # Start the bot
        logger.info("Bot started")
        application.run_polling()

    except Exception as e:
        logger.error(f"Error starting bot: {str(e)}")


if __name__ == '__main__':
    main()