import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
from random import choice
import os

api = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?api_key=DEMO_KEY&sol=1000"

botToken = "Your Bot API Key"

bot = telebot.TeleBot(botToken)

images = []
req = requests.get(api).json()
for info in req["photos"]:
    infos = {
    'CamName' : info["camera"]["full_name"],
    'image' : info["img_src"],
    'CaptureDate' : info["earth_date"],
    'RoverName' : info["rover"]["name"],
    'RoverLunchDate' : info["rover"]["launch_date"],
    'RoverLandingDate' : info["rover"]["landing_date"],
    'RoverCurrentStatus' : info["rover"]["status"]
    }
    images.append(infos)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    data = call.data
    if data == 'update':
        i1 = [[InlineKeyboardButton(text=f'Check Now',
     callback_data=f'update')]]
        inline_keyboard = InlineKeyboardMarkup(i1)
        imageInfo = choice(images)
        data = f"""Rover Name : {imageInfo['RoverName']}
Rover Lunch Date : {imageInfo['RoverLunchDate']}
Rover Landing Date : {imageInfo['RoverLandingDate']}
Rover Camera Name : {imageInfo['CamName']}
Rover Current Status : {imageInfo['RoverCurrentStatus']}
"""
        photo = open('photo.jpg', 'wb')
        photo.write(requests.get(imageInfo['image']).content)
        photo.close()
        with open('photo.jpg', 'rb') as photo_file:
            #bot.send_photo(message.chat.id, photo_file, caption = data, reply_markup=inline_keyboard)
            media = telebot.types.InputMediaPhoto(media=photo_file, caption=data)
            bot.edit_message_media(
                media=media,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=inline_keyboard
            )
            bot.edit_message_reply_markup(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=inline_keyboard
            )
        os.remove('photo.jpg')

@bot.message_handler(commands=['start'])
def start(message):
    try:
        imageInfo = choice(images)
        i1 = [[InlineKeyboardButton(text=f'Another One',
     callback_data=f'update')]]
        inline_keyboard = InlineKeyboardMarkup(i1)
        data = f"""Rover Name : {imageInfo['RoverName']}
Rover Lunch Date : {imageInfo['RoverLunchDate']}
Rover Landing Date : {imageInfo['RoverLandingDate']}
Rover Camera Name : {imageInfo['CamName']}
Rover Current Status : {imageInfo['RoverCurrentStatus']}
"""
        photo = open('photo.jpg', 'wb')
        photo.write(requests.get(imageInfo['image']).content)
        photo.close()
        with open('photo.jpg', 'rb') as photo_file:
            bot.send_photo(message.chat.id, photo_file, caption=data, reply_markup=inline_keyboard)
        os.remove('photo.jpg')
    except Exception:
        bot.send_message(message.chat.id,
         f"Unable To Generate Image")

bot.infinity_polling()

#https://www.facebook.com/zerocruch/
#https://tiktok.com/@zerocruch
#https://www.youtube.com/@zerocruch
#https://www.instagram.com/zerocruch_
