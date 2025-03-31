import logging
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update
import random
import asyncio
from datetime import datetime, timedelta
import json
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Dictionary to store active users
active_users = {}


# Store users in a JSON file
def save_users():
    with open('users.json', 'w') as f:
        json.dump(active_users, f)


# Load users from JSON file
def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


# Command handler for /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    username = update.effective_user.username

    active_users[user_id] = {
        'username': username,
        'joined_at': datetime.now().isoformat()
    }
    save_users()

    await update.message.reply_text(
        "Welcome! You've been subscribed to random notifications. "
        "Use /stop to unsubscribe."
    )


# Command handler for /stop
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id in active_users:
        del active_users[user_id]
        save_users()
        await update.message.reply_text("You've been unsubscribed from notifications.")
    else:
        await update.message.reply_text("You weren't subscribed to notifications.")


# Function to generate random messages
def get_random_message():
    messages = [
        "Hope you're having a great day! 🌟",
        "Remember to stay hydrated! 💧",
        "Time for a quick stretch! 🧘‍♂️",
        "You're doing great! Keep it up! 👍",
        "Here's your random reminder to smile! 😊"
    ]
    return random.choice(messages)


async def send_notifications(app):
    """Send notifications to all active users."""
    for user_id in active_users.keys():
        try:
            await app.bot.send_message(
                chat_id=user_id,
                text=get_random_message()
            )
            logger.info(f"Sent message to user {user_id}")
        except Exception as e:
            logger.error(f"Failed to send message to {user_id}: {str(e)}")


async def schedule_notifications(app, scheduler):
    """Schedule the next notification."""
    await send_notifications(app)
    next_interval = random.randint(3600, 14400)  # 1-4 hours in seconds
    next_time = datetime.now() + timedelta(seconds=next_interval)

    scheduler.add_job(
        schedule_notifications,
        'date',
        run_date=next_time,
        args=[app, scheduler]
    )
    logger.info(f"Next notification scheduled for {next_time}")


async def main():
    try:
        # Load existing users
        global active_users
        active_users = load_users()

        # Get bot token
        token = os.getenv("BOT_TOKEN")
        if not token:
            raise ValueError("No BOT_TOKEN provided in environment variables!")

        # Initialize application
        application = Application.builder().token(token).build()

        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("stop", stop))

        # Initialize scheduler
        scheduler = AsyncIOScheduler()

        # Schedule first notification (10 seconds after start)
        scheduler.add_job(
            schedule_notifications,
            'date',
            run_date=datetime.now() + timedelta(seconds=10),
            args=[application, scheduler]
        )

        # Start the scheduler
        scheduler.start()

        logger.info("Bot started successfully!")

        # Start polling
        await application.run_polling(allowed_updates=Update.ALL_TYPES)

    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise


if __name__ == "__main__":
    asyncio.run(main())