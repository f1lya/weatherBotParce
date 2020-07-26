import requests
import re
import logging
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)
URL = 'https://yandex.ru/pogoda/yaroslavl/month?via=hnav'
TOKEN = 'Вставте ваш токен'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def get_html(url, params=None):
    r = requests.get(url, params=params)
    return r


def get_info(html, number):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        day = soup.find(text=re.compile(number)).parent
        params = day.find_parent('div')
        temperature = params.find('span', class_='temp__value').text + '°'
        precipitation = params.find('td', class_='climate-calendar-day__detailed-data-table-cell_value_yes').text
        pressure = params.find_all('td', class_='climate-calendar-day__detailed-data-table-cell_value_yes')[1].text
        windSpeed = params.find('div', class_='wind-speed').text + ' м/с'
        info = 'Температура: ' + temperature + '\nДавление: ' + precipitation + '\nВлажность: ' + pressure + \
               '\nСкорость ветра: ' + windSpeed
        return info
    except AttributeError:
        return "Введите корректную дату"


def parse(number):
    html = get_html(URL)
    if html.status_code == 200:
        info = get_info(html.text, number)
        return info


@dp.message_handler(commands=['start'])
async def cmd_start(msg: types.Message):
    await msg.answer('Привет! Я могу дать прогноз погоды в г. Ярославле.\nВведи нужную дату. Например: 3 августа')


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, parse(msg.text))


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
