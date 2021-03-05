from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from modules.scraper.scraper import StudiumScraper
from modules.data.data_reader import config_map


def generate_keyboard(update: Update, context: CallbackContext, studium_out: StudiumScraper, message_text: str) -> None:
    """Generate the keyboard to select the options

    Args:
        update (Update): update event
        context (CallbackContext): context passed by the handler
        studium_out (StudiumScraper): output from studium scraper
        message_text (str): message to show above the keyboard
    """    
    keyboard = []

    start_index = context.user_data['shift_menu_index']
    end_index = start_index + config_map['max_buttons']

    if start_index > 0:
        keyboard.append([InlineKeyboardButton('⬆️ UP ⬆️', callback_data='UP')])

    for text, link in zip(studium_out.text_list[start_index:end_index], studium_out.url_list[start_index:end_index]):
        keyboard.append([InlineKeyboardButton(text, callback_data=link)])

    if end_index < len(studium_out.text_list) - 1:
        keyboard.append([InlineKeyboardButton('⬇️ DOWN ⬇️', callback_data='DOWN')])

    reply_markup = InlineKeyboardMarkup(keyboard)

    if hasattr(update, 'callback_query'):
        query = update.callback_query
    else:
        query = update

    if query is None:
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=message_text,
                                 reply_markup=reply_markup)
    else:
        query.edit_message_text(text=message_text,
                                reply_markup=reply_markup)
    