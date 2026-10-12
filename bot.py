import telebot
from telebot import types

TOKEN = "8749362993:AAFwSz4QMkHgdomRfXTqm50yoza_tKND5cg"
bot = telebot.TeleBot(TOKEN)

tariffs = []
clients = []

@bot.message_handler(commands=['start'])
def start(message):
    show_main_menu(message)

def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    btn1 = types.KeyboardButton("📋 Тарифи")
    btn2 = types.KeyboardButton("👥 Клієнти")
    btn3 = types.KeyboardButton("➕ Додати тариф")
    btn4 = types.KeyboardButton("➕ Додати клієнта")
    btn5 = types.KeyboardButton("🗑️ Видалити тариф")
    btn6 = types.KeyboardButton("🗑️ Видалити клієнта")
    btn7 = types.KeyboardButton("📊 Статистика")
    
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    
    bot.send_message(message.chat.id, 
                    "📱 Вітаю в системі мобільного зв'язку!\n\n"
                    "Оберіть дію з меню", 
                    reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "📋 Тарифи":
        show_tariffs(message)
    
    elif message.text == "👥 Клієнти":
        show_clients(message)
    
    elif message.text == "➕ Додати тариф":
        add_tariff1(message)
    
    elif message.text == "➕ Додати клієнта":
        add_client1(message)
    
    elif message.text == "🗑️ Видалити тариф":
        delete_tariff1(message)
    
    elif message.text == "🗑️ Видалити клієнта":
        delete_client1(message)
    
    elif message.text == "📊 Статистика":
        show_stats(message)
    
    else:
        bot.send_message(message.chat.id, "Використовуйте кнопки меню")

def show_tariffs(message):
    if not tariffs:
        bot.send_message(message.chat.id, "Список тарифів порожній")
        return
    
    text = "СПИСОК ТАРИФІВ:\n\n"
    for i, tariff in enumerate(tariffs, 1):
        parts = tariff.split(",")
        if len(parts) >= 4:
            text += f"{i}. {parts[0]} - {parts[1]} грн\n"
            text += f"   📞 {parts[2]} хв | 📶 {parts[3]} ГБ\n\n"
    
    bot.send_message(message.chat.id, text)

def show_clients(message):
    if not clients:
        bot.send_message(message.chat.id, "Список клієнтів порожній")
        return
    
    text = "СПИСОК КЛІЄНТІВ:\n\n"
    for i, client in enumerate(clients, 1):
        parts = client.split(",")
        if len(parts) >= 3:
            text += f"{i}. {parts[0]}\n"
            text += f"   📱 {parts[1]} | 📞 {parts[2]}\n\n"
    
    bot.send_message(message.chat.id, text)

def show_stats(message):
    text = f"📊 СТАТИСТИКА:\n\n"
    text += f"📋 Тарифів: {len(tariffs)}\n"
    text += f"👥 Клієнтів: {len(clients)}"
    bot.send_message(message.chat.id, text)

def add_tariff1(message):
    msg = bot.send_message(message.chat.id, "Введіть назву тарифу:")
    bot.register_next_step_handler(msg, add_tariff2)

def add_tariff2(message):
    tariff_name = message.text
    msg = bot.send_message(message.chat.id, "Введіть ціну (грн):")
    bot.register_next_step_handler(msg, add_tariff3, tariff_name)

def add_tariff3(message, tariff_name):
    price = message.text
    msg = bot.send_message(message.chat.id, "Введіть кількість хвилин:")
    bot.register_next_step_handler(msg, add_tariff4, tariff_name, price)

def add_tariff4(message, tariff_name, price):
    minutes = message.text
    msg = bot.send_message(message.chat.id, "Введіть обсяг інтернету (ГБ):")
    bot.register_next_step_handler(msg, add_tariff, tariff_name, price, minutes)

def add_tariff(message, tariff_name, price, minutes):
    internet = message.text
    
    tariff = f"{tariff_name},{price},{minutes},{internet}"
    tariffs.append(tariff)
    
    bot.send_message(message.chat.id, 
                    f"    Тариф додано!\n\n"
                    f"📋 {tariff_name}\n"
                    f"💰 {price} грн\n"
                    f"📞 {minutes} хв\n"
                    f"📶 {internet} ГБ")

def add_client1(message):
    msg = bot.send_message(message.chat.id, "Введіть ПІБ клієнта:")
    bot.register_next_step_handler(msg, add_client2)

def add_client2(message):
    client_name = message.text
    msg = bot.send_message(message.chat.id, "Введіть номер телефону:")
    bot.register_next_step_handler(msg, add_client3, client_name)

def add_client3(message, client_name):
    phone = message.text
    
    if tariffs:
        text = "Оберіть тариф зі списку (введіть номер):\n\n"
        for i, tariff in enumerate(tariffs, 1):
            parts = tariff.split(",")
            text += f"{i}. {parts[0]} - {parts[1]} грн\n"
        msg = bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(msg, add_client, client_name, phone)
    else:
        msg = bot.send_message(message.chat.id, "Введіть назву тарифу:")
        bot.register_next_step_handler(msg, add_client_final, client_name, phone)

def add_client(message, client_name, phone):
    try:
        tariff_num = int(message.text) - 1
        if 0 <= tariff_num < len(tariffs):
            tariff_parts = tariffs[tariff_num].split(",")
            tariff_name = tariff_parts[0]
            
            client = f"{client_name},{phone},{tariff_name}"
            clients.append(client)
            
            bot.send_message(message.chat.id,
                           f"   Клієнта додано!\n\n"
                           f"👤 {client_name}\n"
                           f"📱 {phone}\n"
                           f"📋 Тариф: {tariff_name}")
        else:
            bot.send_message(message.chat.id, "Неправильний номер!")
    except:
        bot.send_message(message.chat.id, "Помилка! Спробуйте ще раз.")

def add_client_final(message, client_name, phone):
    tariff = message.text
    
    client = f"{client_name},{phone},{tariff}"
    clients.append(client)
    
    bot.send_message(message.chat.id,
                    f"    Клієнта додано!\n\n"
                    f"👤 {client_name}\n"
                    f"📱 {phone}\n"
                    f"📋 Тариф: {tariff}")

def delete_tariff1(message):
    if not tariffs:
        bot.send_message(message.chat.id, "Немає тарифів для видалення!")
        return
    
    text = "Оберіть тариф для видалення (введіть номер):\n\n"
    for i, tariff in enumerate(tariffs, 1):
        parts = tariff.split(",")
        if len(parts) >= 4:
            text += f"{i}. {parts[0]} - {parts[1]} грн\n"
    
    text += "\n Введіть номер тарифу для видалення:"
    msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(msg, delete_tariff)

def delete_tariff(message):
    try:
        tariff_num = int(message.text) - 1
        if 0 <= tariff_num < len(tariffs):
            deleted_tariff = tariffs.pop(tariff_num)
            parts = deleted_tariff.split(",")
            global clients
            clients = [client for client in clients if not client.endswith(f",{parts[0]}")]
            
            bot.send_message(message.chat.id,
                           f"    Тариф видалено!\n\n"
                           f"📋 {parts[0]}\n"
                           f"💰 {parts[1]} грн\n"
                           f"📞 {parts[2]} хв\n"
                           f"📶 {parts[3]} ГБ\n\n"
                           f"Видалено  клієнтів з цим тарифом!")
        else:
            bot.send_message(message.chat.id, "Неправильний номер!")
    except:
        bot.send_message(message.chat.id, "Помилка! Спробуйте ще раз.")

def delete_client1(message):
    if not clients:
        bot.send_message(message.chat.id, "Немає клієнтів для видалення!")
        return
    
    text = "Оберіть клієнта для видалення (введіть номер):\n\n"
    for i, client in enumerate(clients, 1):
        parts = client.split(",")
        if len(parts) >= 3:
            text += f"{i}. {parts[0]}\n"
            text += f"   📱 {parts[1]} | 📞 {parts[2]}\n\n"
    
    text += "Введіть номер клієнта для видалення:"
    msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(msg, delete_client_final)

def delete_client_final(message):
    try:
        client_num = int(message.text) - 1
        if 0 <= client_num < len(clients):
            deleted_client = clients.pop(client_num)
            parts = deleted_client.split(",")
            
            bot.send_message(message.chat.id,
                           f"    Клієнта видалено!\n\n"
                           f"👤 {parts[0]}\n"
                           f"📱 {parts[1]}\n"
                           f"📋 Тариф: {parts[2]}")
        else:
            bot.send_message(message.chat.id, "Неправильний номер!")
    except:
        bot.send_message(message.chat.id, "Помилка! Спробуйте ще раз.")

if __name__ == "__main__":
    print("Бота запущено.")
    bot.polling(none_stop=True)