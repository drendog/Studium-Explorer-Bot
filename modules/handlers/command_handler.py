from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from modules.utils.kb_util import generate_keyboard
from modules.scraper.scraper import StudiumScraper
from modules.handlers import STATE


def start_cmd(update: Update, context: CallbackContext):
    """Handles the /start command.
    Sends a welcoming message

    Args:
        update (Update): update event
        context (CallbackContext): context passed by the handler
    
    Returns:
        int: next state of the conversation
    """
    studium_out = StudiumScraper.get_years()

    context.user_data['last_studium_out'] = studium_out
    context.user_data['shift_menu_index'] = 0
    context.user_data['last_url'] = None
    context.user_data['base_url'] = None

    generate_keyboard(update=update, context=context, studium_out=studium_out, message_text='Seleziona l\'anno accademico')
    return STATE['select_department']
