import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(f"Olá, {user.first_name}! Bem-vindo ao nosso bot de suporte.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "📌 *Comandos disponíveis:*\n\n"
        "/start - Inicia a conversa com o bot\n"
        "/help - Mostra esta mensagem de ajuda"
    )
    await update.message.reply_text(help_text)

def main() -> None:
    """Start the bot."""
    try:
        # Create application
        application = Application.builder().token(TOKEN).build()

        # Add command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        
        # Start the bot
        logger.info("Bot iniciado com sucesso!")
        application.run_polling()
        
    except Exception as e:
        logger.critical(f"Erro crítico ao iniciar o bot: {str(e)}")
        print(f"Erro ao iniciar o bot: {str(e)}")

if __name__ == "__main__":
    main()