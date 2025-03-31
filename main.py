import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from datetime import datetime
import json
import aiohttp
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get your bot token from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')


# Store for managing active purchases and player data
class GameStore:
    def __init__(self):
        self.pending_purchases = {}
        self.player_data = {}

    async def create_purchase(self, player_id: int, item_id: str, amount: int):
        purchase_id = f"{player_id}_{datetime.now().timestamp()}"
        self.pending_purchases[purchase_id] = {
            "player_id": player_id,
            "item_id": item_id,
            "amount": amount,
            "status": "pending"
        }
        return purchase_id

    async def complete_purchase(self, purchase_id: str):
        if purchase_id in self.pending_purchases:
            purchase = self.pending_purchases[purchase_id]
            purchase["status"] = "completed"
            # Here you would typically update the player's inventory
            await self.update_player_inventory(purchase["player_id"], purchase["item_id"], purchase["amount"])
            return True
        return False

    async def update_player_inventory(self, player_id: int, item_id: str, amount: int):
        if player_id not in self.player_data:
            self.player_data[player_id] = {"inventory": {}}

        if item_id not in self.player_data[player_id]["inventory"]:
            self.player_data[player_id]["inventory"][item_id] = 0

        self.player_data[player_id]["inventory"][item_id] += amount


# Initialize the store
game_store = GameStore()

# Define available items
GAME_ITEMS = {
    "coins_100": {"name": "100 Coins", "price": 1},
    "coins_500": {"name": "500 Coins", "price": 4},
    "coins_1000": {"name": "1000 Coins", "price": 7},
    "special_item": {"name": "Special Item", "price": 2},
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        "Welcome to the game store! Use /shop to see available items."
    )


async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Display available items for purchase."""
    keyboard = []
    for item_id, item_data in GAME_ITEMS.items():
        keyboard.append([InlineKeyboardButton(
            f"{item_data['name']} - {item_data['price']} Stars",
            callback_data=f"buy_{item_id}"
        )])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select an item to purchase:", reply_markup=reply_markup)


async def handle_purchase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle purchase button clicks."""
    query = update.callback_query
    await query.answer()

    item_id = query.data.replace("buy_", "")
    if item_id in GAME_ITEMS:
        item = GAME_ITEMS[item_id]
        player_id = query.from_user.id  # You can map this to your game's player ID

        # Create a pending purchase
        purchase_id = await game_store.create_purchase(player_id, item_id, 1)

        # Create payment invoice
        keyboard = [[InlineKeyboardButton(
            f"Pay {item['price']} Stars",
            callback_data=f"confirm_{purchase_id}"
        )]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"Confirm purchase of {item['name']} for {item['price']} Stars?",
            reply_markup=reply_markup
        )


async def confirm_purchase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle purchase confirmation."""
    query = update.callback_query
    await query.answer()

    purchase_id = query.data.replace("confirm_", "")
    success = await game_store.complete_purchase(purchase_id)

    if success:
        await query.edit_message_text(
            "Purchase successful! Your items have been added to your inventory."
        )

        # Here you would typically notify your game server about the successful purchase
        # This is where you'd integrate with your Unity game's backend
        purchase_data = game_store.pending_purchases[purchase_id]
        await notify_game_server(purchase_data)
    else:
        await query.edit_message_text(
            "Purchase failed. Please try again later."
        )


async def notify_game_server(purchase_data: dict):
    """Notify the game server about the successful purchase."""
    # Replace with your game server's API endpoint
    game_server_url = os.getenv('GAME_SERVER_URL')

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                    f"{game_server_url}/purchase-complete",
                    json={
                        "player_id": purchase_data["player_id"],
                        "item_id": purchase_data["item_id"],
                        "amount": purchase_data["amount"],
                        "timestamp": datetime.now().isoformat()
                    }
            ) as response:
                if response.status == 200:
                    print(f"Successfully notified game server about purchase {purchase_data}")
                else:
                    print(f"Failed to notify game server. Status: {response.status}")
        except Exception as e:
            print(f"Error notifying game server: {e}")


def main():
    """Start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("shop", shop))
    application.add_handler(CallbackQueryHandler(handle_purchase, pattern="^buy_"))
    application.add_handler(CallbackQueryHandler(confirm_purchase, pattern="^confirm_"))

    # Start the bot
    application.run_polling()


if __name__ == "__main__":
    main()