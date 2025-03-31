import logging
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update
import random
import asyncio
from datetime import datetime, timedelta
import json

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

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


# Function to send random notifications
async def send_random_notifications(context: ContextTypes.DEFAULT_TYPE):
    while True:
        # Random interval between 1 to 4 hours
        wait_time = random.randint(3600, 14400)

        # Send messages to all active users
        for user_id in active_users.keys():
            try:
                await context.bot.send_message(
                    chat_id=user_id,
                    text=get_random_message()
                )
                logging.info(f"Sent message to user {user_id}")
            except Exception as e:
                logging.error(f"Failed to send message to {user_id}: {str(e)}")

        await asyncio.sleep(wait_time)


async def main():
    # Load existing users
    global active_users
    active_users = load_users()

    # Initialize bot with your token
    application = Application.builder().token('7695007286:AAH_6A-kOTUp9C1Z4assCExNzu2WK0EBK-U').build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop))

    # Start the notification task
    application.job_queue.run_once(
        send_random_notifications,
        when=1
    )

    # Start the bot
    await application.run_polling()


if __name__ == '__main__':
    asyncio.run(main())