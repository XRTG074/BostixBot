import telebot

import BostixActions.Messaging.MessagingActions as Messaging

bot = telebot.TeleBot("МестоДляОченьКрутогоТокена") # - Бот


# - Инициализация бота в другом файле

Messaging.InitBot(bot)