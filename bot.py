import telebot
import logging
import datetime

import constants as cns
import config as cfg
import template_messages as tmp_msg
from db_manager import DBManager

bot = telebot.TeleBot(cfg.TOKEN)
DBM = DBManager()


def getDietKeyboard():
    diet_keyboard = telebot.types.ReplyKeyboardMarkup(True)
    diet_keyboard.row('Рацион на сегодня')
    diet_keyboard.row('Рацион на завтра')
    diet_keyboard.row('Рекомендации', 'Книга рецептов', 'Другое')
    return diet_keyboard


def parseDateUnixTime(unix_time):
    return unix_time // cns.SECS_IN_DAY * cns.SECS_IN_DAY


# def unixTimeToDate(unix_time):
#     print(type(datetime.datetime.fromtimestamp(unix_time)))
#     print(datetime.datetime.fromtimestamp(unix_time))


def getDietForDay(day):
    return open(cfg.DIETS_PATH + '/' + str(day) + '.png', 'rb')


def getRecipesBook():
    return open(cfg.RECIPES_BOOK_PATH, 'rb')


@bot.message_handler(commands=[cfg.START_COMMAND])
def sendStartMessage(message):
    date_to_ins = parseDateUnixTime(message.date)
    ins_result = DBM.InsertClient(message.chat.id, date_to_ins, date_to_ins)
    if ins_result == 0:
        DBM.UpdateStartDietDate(message.chat.id, date_to_ins)
    bot.send_message(message.chat.id, tmp_msg.hello_msg, reply_markup=getDietKeyboard())
    if ins_result == 1:
        bot.send_message(message.chat.id, tmp_msg.recommendations_msg())


@bot.message_handler(commands=[cfg.SET_DAY_COMMAND])
def setDay(message):
    try:
        command__, day_str = message.text.split(' ')
        if int(day_str) > cns.DIET_DAYS_MAX or int(day_str) < 1:
            bot.send_message(message.chat.id, tmp_msg.wrong_format_day_msg(day_str))
        else:
            day_delta = int(day_str) - 1
            start_day = parseDateUnixTime(message.date) - day_delta * cns.SECS_IN_DAY
            DBM.UpdateStartDietDate(message.chat.id, start_day)
            bot.send_message(message.chat.id, tmp_msg.set_day_msg(day_str))
    except Exception:
        bot.send_message(message.chat.id, tmp_msg.wrong_format_msg)


@bot.message_handler(commands=[cfg.SHOW_DAY_COMMAND])
def sendDietByDay(message):
    try:
        command__, day_str = message.text.split(' ')
        if int(day_str) > cns.DIET_DAYS_MAX or int(day_str) < 1:
            bot.send_message(message.chat.id, tmp_msg.wrong_format_day_msg(day_str))
        else:
            bot.send_message(message.chat.id, tmp_msg.show_day_msg(day_str))
            bot.send_photo(message.chat.id, photo=getDietForDay(int(day_str)))
    except Exception:
        bot.send_message(message.chat.id, tmp_msg.wrong_format_msg)


@bot.message_handler(regexp=cfg.TODAY_DIET_REGEXP)
def sendTodayDiet(message):
    start_day = DBM.SelectStartDietDate(message.chat.id)
    qur_day = parseDateUnixTime(message.date)
    day = (qur_day - start_day) // cns.SECS_IN_DAY + 1
    if day > cns.DIET_DAYS_MAX:
        day = day % cns.DIET_DAYS_MAX
    if day == 0:
        day = cns.DIET_DAYS_MAX

    bot.send_message(message.chat.id, tmp_msg.today_diet_msg)
    bot.send_photo(message.chat.id, photo=getDietForDay(day))


@bot.message_handler(regexp=cfg.TOMORROW_DIET_REGEXP)
def sendTomorrowDiet(message):
    start_day = DBM.SelectStartDietDate(message.chat.id)
    qur_day = parseDateUnixTime(message.date)
    day = (qur_day - start_day) // cns.SECS_IN_DAY + 2
    if day > cns.DIET_DAYS_MAX:
        day = day % cns.DIET_DAYS_MAX
    if day == 0:
        day = cns.DIET_DAYS_MAX

    bot.send_message(message.chat.id, tmp_msg.tomorrow_diet_msg)
    bot.send_photo(message.chat.id, photo=getDietForDay(day))


@bot.message_handler(regexp=cfg.RECOMMENDATIONS_REGEXP)
def sendRecommendations(message):
    bot.send_message(message.chat.id, tmp_msg.recommendations_msg())


@bot.message_handler(regexp=cfg.SETTINGS_REGEXP)
def sendSettings(message):
    bot.send_message(message.chat.id, tmp_msg.settings_msg)


@bot.message_handler(regexp=cfg.RECIPES_BOOK_REGEXP)
def sendRecipesBook(message):
    bot.send_document(message.chat.id, data=getRecipesBook())


bot.infinity_polling()
