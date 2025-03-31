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


# Function to send notifications
async def send_notifications(bot):
    for user_id in active_users.keys():
        try:
            await bot.send_message(
                chat_id=user_id,
                text=get_random_message()
            )
            logger.info(f"Sent message to user {user_id}")
        except Exception as e:
            logger.error(f"Failed to send message to {user_id}: {str(e)}")


class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.application = None
        self.scheduler = None

    async def schedule_next(self):
        await send_notifications(self.application.bot)
        # Schedule next run in 1-4 hours
        next_interval = random.randint(3600, 14400)  # seconds
        next_run = datetime.now() + timedelta(seconds=next_interval)
        self.scheduler.add_job(
            self.schedule_next,
            'date',
            run_date=next_run
        )
        logger.info(f"Next notification scheduled for {next_run}")

    async def start_bot(self):
        try:
            # Initialize bot
            self.application = Application.builder().token(self.token).build()

            # Add command handlers
            self.application.add_handler(CommandHandler("start", start))
            self.application.add_handler(CommandHandler("stop", stop))

            # Initialize scheduler
            self.scheduler = AsyncIOScheduler()

            # Schedule first notification
            self.scheduler.add_job(
                self.schedule_next,
                'date',
                run_date=datetime.now() + timedelta(seconds=10)
            )

            # Start the scheduler
            self.scheduler.start()

            # Start the bot
            await self.application.run_polling(allowed_updates=Update.ALL_TYPES)

        except Exception as e:
            logger.error(f"Error in start_bot: {str(e)}")
            if self.scheduler and self.scheduler.running:
                self.scheduler.shutdown()
            raise


async def main():
    # Load existing users
    global active_users
    active_users = load_users()

    # Get bot token from environment variable
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    if not BOT_TOKEN:
        raise ValueError("No BOT_TOKEN provided in environment variables!")

    # Create and start bot
    bot = TelegramBot(BOT_TOKEN)
    await bot.start_bot()


if __name__ == '__main__':
    try:
        # Create new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Run the main function
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {str(e)}")
    finally:
        # Clean up
        loop.close()