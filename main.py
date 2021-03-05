# telegram
from telegram import BotCommand
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler,\
     Filters, Dispatcher
# data
from modules.data.data_reader import config_map
# modules
from modules.handlers import STATE
from modules.handlers.command_handler import start_cmd
from modules.handlers.callback_handlers import course_callback, shift_menu_index_down, shift_menu_index_up

def add_commands(updater: Updater):
    """Adds the list of commands with their description to the bot

    Args:
        updater (Updater): supplyed Updater
    """
    commands = [
        BotCommand("start", "presentazione iniziale del bot"),
    ]
    updater.bot.set_my_commands(commands=commands)

def add_handlers(dp: Dispatcher):
    """Adds all the needed handlers to the dispatcher

    Args:
        dp (Dispatcher): supplyed dispatcher
    """

    # Conversation handler

    dp.add_handler(CallbackQueryHandler(shift_menu_index_down, pattern=r"^DOWN\.*"))
    dp.add_handler(CallbackQueryHandler(shift_menu_index_up, pattern=r"^UP\.*"))


    dp.add_handler(
        ConversationHandler(entry_points=[CommandHandler("start", start_cmd)],
                            states={
                                STATE['select_department']: [CallbackQueryHandler(course_callback)],
                            },
                            fallbacks=[CommandHandler("start", start_cmd)],
                            allow_reentry=False))


def main():
    """Main function
    """
    updater = Updater(config_map['token'], request_kwargs={'read_timeout': 20, 'connect_timeout': 20}, use_context=True)
    add_commands(updater)
    add_handlers(updater.dispatcher)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
