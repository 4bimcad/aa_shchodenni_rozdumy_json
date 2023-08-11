import json
import telebot
import datetime

TOKEN = 'YOUR_TELEGRAM_TOKEN_HERE'
bot = telebot.TeleBot(TOKEN)

def send_message(chat_id, text):
    bot.send_message(chat_id, text, parse_mode="Markdown")

def get_matching_object(data, today_date):
    return next((item for item in data if item['date'] == today_date), None)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, 'Вітаю!😉 Я Працюю.😎 Для початку роботи нажміть «Меню»')

@bot.message_handler(commands=["getquote"])
def get_quote(message):
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime('%d-%m')

    with open('aa_shchodenni_rozdumy.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    matching_object = get_matching_object(data, formatted_date)

    if matching_object:
        quote_message = f"""
        *{matching_object['text_date']}*
        *{matching_object['title']}*
        _{matching_object['quote']}_
        _{matching_object['source']}_
        _{matching_object['source_page']}_
        {matching_object['comment']}
        """
        send_message(message.chat.id, quote_message)
    else:
        error_message = 'Для поточної дати немає відповідного об´єкта.'
        send_message(message.chat.id, 'Помилка: ' + error_message)

@bot.message_handler(commands=["aboutbook"])
def about_book(message):
    try:
        with open('aa_shchodenni_rozdumy_about.json', 'r', encoding='utf-8') as about_file:
            about_data = json.load(about_file)

        about_message = f"""
        *Назва книги: {about_data[0]['title']}*
        _Автор: {about_data[0]['author']}_
        _Рік: {about_data[0]['year']}_
        Передмова: {about_data[0]['description']}
        """
        send_message(message.chat.id, about_message)
    except Exception as e:
        print('Помилка:', e)
        send_message(message.chat.id, 'Помилка при отриманні інформації про книгу.')

bot.polling(none_stop=True)