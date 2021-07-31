from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import CallbackContext
from modules.utils.kb_util import generate_keyboard
from modules.scraper.scraper import StudiumScraper
from modules.handlers import STATE
from modules.data.data_reader import config_map


def course_callback(update: Update, context: CallbackContext) -> int:
    """Ask to select a course

    Args:
        update (Update): update event
        context (CallbackContext): context passed by the handler

    Returns:
        int: next state of the conversation
    """

    query = update.callback_query

    url: str = query.data

    # print(url)

    if not url.startswith('http'):
        if context.user_data['base_url'] == None:
            url = "https://studium.unict.it" + url
        elif url.startswith('/'):
            url = context.user_data['base_url'] + url
        else:
            url = context.user_data['last_url'] + url

    if url.find('category=') != -1 or len(url) <= 36 or (url.find("studiumarchive.unict.it/dokeos/") != -1 and len(url) <= 43):
        studium_out = StudiumScraper.get_cats(url)
    elif url.find('/courses/') != -1:
        if is_file(url):
            send_file(update=update, context=context, url=url)
            return STATE['end']
        studium_out = StudiumScraper.get_files_list(url)
    else:
        query.edit_message_text(
            text=f"Cannot get this path. Please /start again.")
        return STATE['end']

    context.user_data['last_studium_out'] = studium_out
    context.user_data['shift_menu_index'] = 0
    context.user_data['last_url'] = url
    context.user_data['base_url'] = url[:url.find(
        'unict.it') + len('unict.it')]

    generate_keyboard(update=update.callback_query, context=context,
                      studium_out=studium_out, message_text='Seleziona l\'anno accademico')

    return STATE['select_department']


def is_file(url: str) -> bool:
    """Return value for know if the url is a file

    Args:
        url (str): url

    Returns:
        bool: return true if is a file
    """
    last_folder_index = url.rfind('/')
    if url.find('.', last_folder_index) != -1:
        return True
    return False


def send_file(update: Update, context: CallbackContext, url: str) -> None:
    """Send message for download file

    Args:
        update (Update): update event
        context (CallbackContext): context passed by the handler
        url (str): url
    """
    query = update.callback_query
    query.edit_message_text(text=f'[📥]({url}) *Download File*\. If you need another file, /start again\.',
                            parse_mode=ParseMode.MARKDOWN_V2)


def shift_menu_index_down(update: Update, context: CallbackContext) -> None:
    """Goes down on menu

    Args:
        update (Update): update event
        context (CallbackContext): context passed by the handler
    """
    context.user_data['shift_menu_index'] += config_map['max_buttons']
    generate_keyboard(update=update.callback_query, context=context,
                      studium_out=context.user_data['last_studium_out'], message_text='Seleziona l\'anno accademico')


def shift_menu_index_up(update: Update, context: CallbackContext) -> None:
    """Goes up on menu

    Args:
        update (Update): update event
        context (CallbackContext): context passed by the handler
    """
    context.user_data['shift_menu_index'] -= config_map['max_buttons']
    generate_keyboard(update=update.callback_query, context=context,
                      studium_out=context.user_data['last_studium_out'], message_text='Seleziona l\'opzione desiderata')
