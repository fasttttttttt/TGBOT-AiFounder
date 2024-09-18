	#########
import telebot
from telebot import types
import shutil
import os
import cv2
import numpy as np
import easyocr



bot = telebot.TeleBot('7138686363:AAEOIslZaOFmShBUUzNbzJ2dg7eXj3PLqQ8')
	#########


def delete_eif(folder_path):
    shutil.rmtree(folder_path)
    os.mkdir(folder_path)

		
@bot.message_handler(content_types=['photo', 'text'])
def handler_file(message):
    from pathlib import Path
    Path(f'files/{message.chat.id}/').mkdir(parents=True, exist_ok=True)
    if message.content_type == 'photo':
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        location = f'files/' + file_info.file_path.replace('photos/', '')
        with open(location, 'wb') as new_file:
            new_file.write(downloaded_file)
            

        
        img = cv2.imread(location)

        #(ai)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        plates = cv2.CascadeClassifier('plates.xml')

        results = plates.detectMultiScale(gray,scaleFactor=1.05, minNeighbors=4)
        print(results)

        textreader = easyocr.Reader(['ru'])

        for (x,y,w,h) in results:
            square = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=3)
            x1,x2,y1,y2 = x,x+w,y,y+h
            just_plate = img[y1:y2,x1:x2]
            text = textreader.readtext(just_plate)
            plate_text = text[0][-2]
            bot.send_message(message.chat.id, plate_text)


    elif message.content_type != 'photo':
    	bot.send_message(message.chat.id, 'Отправь фото!')


bot.polling(none_stop=True)

