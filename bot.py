import logging
import json
import html
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN = os.getenv("TOKEN")


def load_questions():
    """Carrega as perguntas do arquivo JSON."""
    try:
        with open("questions.json", "r", encoding="utf-8") as file:
            questions = json.load(file)
        return questions
    except Exception as e:
        logger.error(f"Erro ao carregar arquivo de perguntas: {str(e)}")
        return {"categorias": []}


# Carrega as perguntas
QUESTIONS = load_questions()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Inicia a interação com o bot."""
    user = update.effective_user
    welcome_message = (
        f"Olá, {html.escape(user.first_name)}! 👋\n\n"
        "Bem-vindo ao nosso chat de suporte ao cliente.\n\n"
        "Estou aqui para ajudar! Escolha uma categoria abaixo:"
    )

    keyboard = [
        [InlineKeyboardButton(f"📚 {category['nome']}", callback_data=f"category_{i}")]
        for i, category in enumerate(QUESTIONS["categorias"])
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        welcome_message, reply_markup=reply_markup, parse_mode=ParseMode.HTML
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Gerencia os cliques em botões."""
    try:
        query = update.callback_query
        await query.answer()
        data = query.data

        if data.startswith("category_"):
            # Display questions for the selected category
            category_index = int(data.split("_")[1])
            category = QUESTIONS["categorias"][category_index]

            keyboard = [
                [
                    InlineKeyboardButton(
                        q["pergunta"][:50],
                        callback_data=f"question_{category_index}_{i}",
                    )
                ]
                for i, q in enumerate(category["perguntas"])
            ]

            keyboard.append(
                [InlineKeyboardButton("🏠 Voltar ao Início", callback_data="start")]
            )

            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f"📂 Categoria: {category['nome']}", reply_markup=reply_markup
            )

        elif data == "start":
            # Retorna ao menu inicial
            user = query.from_user
            welcome_message = (
                f"Olá, {html.escape(user.first_name)}! 👋\n\n"
                "Estou aqui para ajudar! Escolha uma categoria abaixo:"
            )

            keyboard = [
                [
                    InlineKeyboardButton(
                        f"📚 {category['nome']}", callback_data=f"category_{i}"
                    )
                ]
                for i, category in enumerate(QUESTIONS["categorias"])
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                welcome_message, reply_markup=reply_markup, parse_mode=ParseMode.HTML
            )

    except Exception as e:
        logger.error(f"Erro no processamento de botão: {str(e)}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mostra comandos disponíveis."""
    help_text = (
        "📌 *Comandos disponíveis:*\n\n"
        "/start - Inicia a conversa com o bot\n"
        "/help - Mostra esta mensagem de ajuda"
    )
    await update.message.reply_text(help_text)


def main() -> None:
    """Executa o bot."""
    try:
        # Cria aplicação
        application = Application.builder().token(TOKEN).build()

        # Registra os handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CallbackQueryHandler(button))

        # Inicia o bot
        logger.info("Bot iniciado com sucesso!")
        application.run_polling()

    except Exception as e:
        logger.critical(f"Erro crítico ao iniciar o bot: {str(e)}")
        print(f"Erro ao iniciar o bot: {str(e)}")


if __name__ == "__main__":
    main()
