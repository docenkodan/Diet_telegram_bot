hello_msg = 'Вы начали диету!\n' \
            'Сегодня день №1.\n' \
            'Если хотите начать диету не сегодня введите "/start" в день, ' \
            'когда хотите начать.\n' \
            'Если вы уже начали диету, и ваш текущий день не первый, введите ' \
            '"/set_day [day]", где [day] - ваш текущий день (от 1 до 30).'


def recommendations_msg():
    return 'Рекомендации к диете:\n\n' + \
           open('data/recommendations.txt', 'r').read()


settings_msg = 'Чтобы посмотреть рацион на определенный день введите "/show_day [day]", ' \
               'где [day] - день, который вам интересен(от 1 до 30).\n' \
               'Если хотите начать диету не сегодня введите "/start" в день, ' \
               'когда хотите начать.\n' \
               'Если вы уже начали диету, и ваш текущий день не первый, введите ' \
               '"/set_day [day]", где [day] - ваш текущий день (от 1 до 30).\n'

wrong_format_msg = 'Вы ввели неизвестную команду. Нажмите "Другое" для подсказки по командам.'

today_diet_msg = 'Рацион на сегодня:'
tomorrow_diet_msg = 'Рацион на завтра:'


def show_day_msg(day):
    return 'Рацион на ' + str(day) + ' день:'


def set_day_msg(day):
    return 'Теперь вы на ' + str(day) + ' дне.'


def wrong_format_day_msg(day):
    return 'Вы ввели ошибочный день: ' + str(day) + '\n День может быть от 1 до 30.'