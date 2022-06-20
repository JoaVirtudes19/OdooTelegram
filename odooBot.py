#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
from telebot import types
import time
import os

### BOT TOKEN 
TOKEN = ""
 
knownUsers = [] ## Id de los usuarios autorizados a utilizar el bot
 
commands = { # Descripción de los comandos
             'start': 'Iniciar el bot',
             'ayuda': 'Información sobre los comandos disponibles',
             'exec': 'Ejecuta un comando',
             'reiniciar': 'Reinicia el sistema',
             'rOdoo' : 'Reiniciar Odoo',
             'parar' : 'Parar Odoo',
             'iniciar' : 'Iniciar Odoo',
             'estado' : 'Mostrar estado del servicio'
}
 
hideBoard = types.ReplyKeyboardRemove() # if sent as reply_markup, will hide the keyboard
 
# Función de debug, para mostrar el nombre,id y mensaje del usuario.
def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print (str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)
 
 
bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener) # register listener

for id in knownUsers:
    bot.send_message(id,"Servidor iniciado ⚡️")
 
# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id #Id del usuario
    if str(cid) not in knownUsers:
        #knownUsers.append(cid) 
        #userStep[cid] = 0
        bot.send_message(cid, "Lo siento, no estás autorizado para usar este bot")
    else:
        command_help(m) # show the new user the help page
 
# help page
@bot.message_handler(commands=['ayuda'])
def command_help(m):
    cid = m.chat.id
    if str(cid) not in knownUsers:
        bot.send_message(cid, "Lo siento, no estás autorizado para usar este bot")
    else:
        help_text = "Estos son los comandos disponibles: \n"
        for key in commands:
            help_text += "/" + key + ": "
            help_text += commands[key] + "\n"
        bot.send_message(cid, help_text)
 
# Reinicia servidor
@bot.message_handler(commands=['reiniciar'])
def command_long_text(m):
    cid = m.chat.id
    if str(cid) not in knownUsers:
        bot.send_message(cid, "Lo siento, no estás autorizado para usar este bot")
    else:
        bot.send_chat_action(cid, 'typing')
        bot.send_message(cid, "🔄 Reiniciando el servidor")
        bot.send_message(cid,"Apagando 🧰")
        time.sleep(1)
        os.system("sudo shutdown -r now")
 
# Ejecuta un comando
@bot.message_handler(commands=['exec'])
def command_long_text(m):
    cid = m.chat.id
    if str(cid) not in knownUsers:
        bot.send_message(cid, "Lo siento, no estás autorizado para usar este bot")
    else:
        bot.send_message(cid, "Ejecutando: "+m.text[len("/exec"):])
        f = os.popen(m.text[len("/exec"):])
        result = f.read()
        bot.send_message(cid, "Resultado: "+result)
 

def mostrarEstado(m):
    cid = m.chat.id
    if str(cid) not in knownUsers:
        bot.send_message(cid, "Lo siento, no estás autorizado para usar este bot")
        return None
    else:
        mensaje = "Estado : "
        f = os.popen("sudo systemctl status odoo.service")
        result = f.read()
        if "Active: active" in result:
            bot.send_message(cid,mensaje + " ACTIVO ✅")
        elif "Active: inactive" in result:
            bot.send_message(cid,"INACTIVO 🔴")
        else:
            bot.send_message(cid,"DESCONOCIDO 😵‍💫")
        return result

@bot.message_handler(commands=['rOdoo'])
def command_long_text(m):
    cid = m.chat.id
    if str(cid) not in knownUsers:
        bot.send_message(cid, "Lo siento, no estás autorizado para usar este bot")
    else:
        mostrarEstado(m)
        bot.send_message(cid,"🔄 Reiniciando Odoo...")
        r = os.popen("sudo systemctl restart odoo.service").read()
        mostrarEstado(m)

@bot.message_handler(commands=['iniciar'])
def command_long_text(m):
    cid = m.chat.id
    if str(cid) not in knownUsers:
        bot.send_message(cid, "Lo siento, no estás autorizado para usar este bot")
    else:
        estado = mostrarEstado(m)
        if "Active: active" in estado:
            bot.send_message(cid,"⚠️ADVERTENCIA, SOLO USAR ESTE COMANDO SI ESTÁ TOTALMENTE SEGUR@ DE QUE ODOO ESTÁ INACTIVO⚠️")
            bot.send_message(cid,"👷🏼 CANCELANDO OPERACIÓN")
        else:
            bot.send_message(cid,"Iniciando Odoo 🚦")
            r = os.popen("sudo systemctl start odoo.service").read()
            mostrarEstado(m)

@bot.message_handler(commands=['parar'])
def command_long_text(m):
    cid = m.chat.id
    if str(cid) not in knownUsers:
        bot.send_message(cid, "Lo siento, no estás autorizado para usar este bot")
    else:
        estado = mostrarEstado(m)
        if "Active: inactive" in estado:
            bot.send_message(cid,"⚠️ADVERTENCIA, SOLO USAR ESTE COMANDO SI ESTÁ TOTALMENTE SEGUR@ DE QUE ODOO ESTÁ ACTIVO")
            bot.send_message(cid,"👷🏼 CANCELANDO OPERACIÓN")
        else:
            bot.send_message(cid,"Parando Odoo 🚦")
            r = os.popen("sudo systemctl stop odoo.service").read()
            mostrarEstado(m)

@bot.message_handler(commands=['Fbot'])
def command_long_text(m):
    cid = m.chat.id
    if str(cid) not in knownUsers:
        bot.send_message(cid, "Lo siento, no estás autorizado para usar este bot")
    else:
        bot.send_message(cid, "F")
        exit()

@bot.message_handler(commands=['estado'])
def command_long_text(m):
    cid = m.chat.id
    result = mostrarEstado(m)
    bot.send_message(cid,result)



# filter on a specific message
@bot.message_handler(func=lambda message: message.text == "Hola")
def command_text_hi(m):
    bot.send_message(m.chat.id, "Buenas, soy OdooAJ, un bot diseñado para el mantenimiento de servidores de Odoo sobre Debian 🐧")
 
 #Mensaje default para el tipo texto.
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "No te entiendo, prueba con /ayuda")
 
def run():
    bot.infinity_polling()

run()