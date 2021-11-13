# -*- coding: utf-8 -*-
__author__ = "SirHades696"
__email__ = "djnonasrm@gmail.com"

from telegram import InlineKeyboardButton, InlineKeyboardMarkup 
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
import telegram
import logging
import os
import random
import pyshorteners
import json
from unidecode import unidecode
import re
import math
from ast import literal_eval
import sys
# Local 
from data.emojis_and_stickers import data
from web_scraping.anime import Anime_Search
from data.ptb_firebase_persistence import FirebasePersistence


class Anime_Bot:
    def __init__(self):
        self.__TOKEN = os.getenv('TOKEN')
        self.__mod = os.getenv("MODE")
        self.__two, self.__three, self.__four, self.__five, self.__six = range(2,7)
        self.s = pyshorteners.Shortener()
        self.__anime = Anime_Search()
        self.__data = data
        self.__start_logger()
        self.__start_bot()
    
    def __start_logger(self):
        """
        Set logger
        """
        #Logging, display the process in console
        logging.basicConfig(
            level=logging.INFO, 
            format="%(asctime)s | %(message)s")
        self.logger = logging.getLogger()
    
    def __commandHandler_start(self, update, context):
        user_id = update.effective_user['id'] 
        username = update.effective_user['username']
        f_name = update.effective_user['first_name'] 
        l_name = update.effective_user['last_name']
        
        if username != None and f_name != None and l_name != None:
            full_name = f_name + " " + l_name
            cadena = full_name + "/" + username
        elif username != None and f_name != None:
            cadena = f_name + "/" + username
        elif username == None and  f_name != None:
            cadena = f_name
            
        self.logger.info(f"El usuario {username}/{user_id}, ha inicado el bot...")
        
        fb = self.s.dagd.short(r"https://www.facebook.com/armyanime/")
        tw = self.s.dagd.short(r"https://twitter.com/ArmyAnime_")
        ins = self.s.dagd.short(r"https://www.instagram.com/animearmy.jp/")
        
        # Sticker 
        context.bot.send_sticker(chat_id=user_id, 
                                sticker = self.__data['Welcome'][random.randrange(0,4)])
        self.__text =  (f"<b> Bienvenido(a): \n\n{self.__data['fire']} <i><u>{cadena}</u></i> {self.__data['hand']} \n\n"
                 f"Mi objetivo es proporcionarte los links de descarga de algún episodio, OVA o película almacenado en AnimeFLV.\n"
                 f"\nPuntos Importantes:"
                 f"\n{self.__data['check']} No soy un bot oficial de la página."
                 f"\n{self.__data['check']} La disponibilidad de los episodios, OVA’s o películas esta sujeto al sitio web."
                 f"\n\nContactos oficiales del sitio:"
                 f"\n{self.__data['check']} Facebook: {fb}"
                 f"\n{self.__data['check']} Twitter: {tw}"
                 f"\n{self.__data['check']} Instagram: {ins}"
                 f"\n\n{self.__data['check']}Para más información visitar la sección de <u><i>\"Ayuda\"</i></u>{self.__data['help']}"
                 f"\n\n<i><u>D I S F R U T A L O </u></i></b>\n\n\n"
                )
        #send msg 
        update.message.reply_text(
                                text=self.__text,
                                parse_mode="HTML",
                                reply_markup=self.__main_menu_btns(),disable_web_page_preview=True)

    def __main_menu_btns(self):
        btns = [[InlineKeyboardButton(text=f"{self.__data['dragon']} Buscar Anime {self.__data['magnifying_glass']}", callback_data='SEARCH'), 
                 InlineKeyboardButton(text=f"Ayuda {self.__data['help']}", callback_data='HELP')],
                [InlineKeyboardButton(text=f"Acerca de... {self.__data['index']}", callback_data='ABOUT')],
                ] 
        #json type 
        reply = InlineKeyboardMarkup(inline_keyboard=btns)
        line_btns = json.dumps(reply.to_dict())  
        
        return line_btns
    
    def __unknow_command_handler(self, update, context):
        user_id = update.effective_user['id'] 
        username = update.effective_user['username']
        # Sticker 
        context.bot.send_sticker(chat_id=user_id, 
                                sticker = self.__data['Sad_s'][random.randrange(0,4)])         
        update.message.reply_text(parse_mode="HTML", 
                                text=f"<b>{self.__data['sad']} {self.__data['sad']} Lo siento, no entendí el comando...</b>",
                                reply_markup=self.__main_menu_btns())
        self.logger.info(f"El usuario {username}/{user_id}, ingreso un comando desconocido...")

    def __about(self, update, context):
        user_id = update.effective_user['id'] 
        username = update.effective_user['username']
                
        query = update.callback_query
        if query != None:
            query.answer(timeout=25, cache_time=25)
            
        url="https://www.paypal.com/donate?hosted_button_id=EBUAN5V9ZYENS"
        new_url = self.s.tinyurl.short(url)
        context.bot.send_sticker(chat_id=user_id, 
                                sticker = self.__data['About'][random.randrange(0,4)])
        
        txt = (f"{self.__data['monkey']} <b>Espero que este sencillo bot te haya resultado muy útil. </b> {self.__data['monkey2']}\n"
                f"<b>Gracias por usarlo. </b> {self.__data['fire']}\n"
                f"<u><i><b> Versión 1.0</b></i></u> {self.__data['smiling']}\n"
                f"{self.__data['alien']} <b> @SirHades696 </b> {self.__data['trex']}\n"
                f"<i><b><u>Para apoyar este proyecto: </u></b></i>\n"
                f"{new_url}")
        
        context.bot.sendMessage(chat_id = user_id, 
                                parse_mode="HTML", 
                                text=txt,
                                reply_markup=self.__main_menu_btns(),disable_web_page_preview=True)
        self.logger.info(f"El usuario {username}/{user_id}, solicito acerca de...")
        
    
    def __help(self, update, context):
        user_id = update.effective_user['id'] 
        username = update.effective_user['username']
        query = update.callback_query
        if query != None:
            query.answer(timeout=25, cache_time=25)
            
        context.bot.send_sticker(chat_id=user_id, 
                                sticker = self.__data['Help'][random.randrange(0,4)])
        txt = (f"{self.__data['robot']}<b>Este bot ha sido alojado en un servidor gratuito, por lo que, después de 30 min de inactividad el bot dormirá. {self.__data['robot2']}\n\n"
               f"{self.__data['robot']}Si deseas seguir interactuando después del limite de tiempo, el bot tardará un aproximado de 5 min en responder, una vez activo, el bot funcionará con normalidad.{self.__data['robot2']}\n\n"
               f"{self.__data['smiling']}Muchas gracias por tu comprensión.{self.__data['hand']}\n\n"
               f"Si deseas contribuir con este proyecto, por favor visita la sección de <i><u>\"Acerca de...\"{self.__data['index']}</u></i></b>"
               )
        context.bot.sendMessage(chat_id = user_id, 
                                parse_mode="HTML", 
                                text=txt,
                                reply_markup=self.__main_menu_btns(),disable_web_page_preview=True)
        self.logger.info(f"El usuario {username}/{user_id}, solicito ayuda...")
    
    def __search_msg(self, update, context):
        username = update.effective_user['username']
        user_id = update.effective_user['id'] 
        
        query = update.callback_query
        if query != None:
            query.answer(timeout=25, cache_time=25) 
        
        self.logger.info(f"El usuario {username}/{user_id}, ha creado una solicitud de búsqueda...")
        cadena = f"{self.__data['dragon']}<b> Escribe el nombre del Anime que deseas buscar </b>{self.__data['magnifying_glass']}"
        context.bot.sendMessage(chat_id=user_id, parse_mode="HTML", text=cadena)
        return self.__two

    
    def __search_titles(self,update, context):
        username = update.effective_user['username']
        user_id = update.effective_user['id']   
        title =  unidecode(re.sub(r'[^ \w+]', '',update.message.text))
        if title == '':
            self.logger.info(f"El usuario {username}/{user_id}, no encontro resultados...")
            # Sticker 
            context.bot.send_sticker(chat_id=user_id, 
                                sticker = self.__data['Sad_s'][random.randrange(0,4)]) 
            cadena = f"<b>{self.__data['sad']} Por favor, realiza una búsqueda correcta {self.__data['sad']}</b>"
            update.message.reply_text( 
                                    parse_mode="HTML", 
                                    text=cadena,
                                    reply_markup=self.__main_menu_btns())
        else:      
            # If contains \n
            self.__title = title.replace("\n", " ")
            self.logger.info(f"El usuario {username}/{user_id}, ha introducido una búsqueda...")
            #Typing 
            cadena = f"<b>Buscando el Anime: \n{self.__data['magnifying_glass']} <i><u>{self.__title}</u></i></b> {self.__data['magnifying_glass']}"
            update.message.reply_text(parse_mode="HTML", text=cadena)
            # web scraping      
            anime_titles, self.__pages = self.__anime.search_titles(self.__title)
            self.logger.info(f"El usuario {username}/{user_id}, esta recibiendo los resultados...")
            
            tam = len(anime_titles)
            if tam == 0:
                self.logger.info(f"El usuario {username}/{user_id}, no encontro resultados...")
                # Sticker 
                context.bot.send_sticker(chat_id=user_id, 
                                    sticker = self.__data['Sad_s'][random.randrange(0,4)]) 
                cadena = f"<b>{self.__data['sad']} No se encontraron resultados para el Anime: \n{self.__data['cross_mark']} <i><u>{self.__title}</u></i> {self.__data['cross_mark']}</b>"
                update.message.reply_text( 
                                        parse_mode="HTML", 
                                        text=cadena,
                                        reply_markup=self.__main_menu_btns())
            else:
                self.__result_titles(update,context,self.__title,self.__pages)
                return self.__three
        
        
    def __display_titles(self, update, context):
        username = update.effective_user['username']
        user_id = update.effective_user['id']
        query = update.callback_query
        if query != None:
            query.answer(timeout=25, cache_time=25) 
        
        self.__titles_txt = self.persistence.get_chat_data_(user_id,'titles_txt')
        self.__btns_titles =  literal_eval(self.persistence.get_chat_data_(user_id,'btns_title'))  
        self.logger.info(f"El usuario {username}/{user_id}, solicito los resultados anteriores...")
        query.edit_message_text(parse_mode="HTML", 
                                text=self.__titles_txt,
                                reply_markup=self.__btns_titles)
        self.logger.info(f"El usuario {username}/{user_id}, recibio los titulos...")
        return self.__three   
            
    def __result_titles(self, update, context, anime_title, page):
        username = update.effective_user['username']
        user_id = update.effective_user['id'] 
        if len(page) > 1: 
            anime_titles1, pages = self.__anime.search_titles(anime_title, page[0])
            anime_titles2, pages = self.__anime.search_titles(anime_title, page[1])
            self.__titles = []
            
            for title in anime_titles1:
                self.__titles.append([anime_titles1[title]['Title'], anime_titles1[title]['Type'], anime_titles1[title]['Ranking'], anime_titles1[title]['Description'], anime_titles1[title]['URL']])
            
            for title in anime_titles2:
                self.__titles.append([anime_titles2[title]['Title'], anime_titles2[title]['Type'], anime_titles2[title]['Ranking'], anime_titles2[title]['Description'], anime_titles2[title]['URL']])
                
            self.__titles_txt = f"<b>Excelente búsqueda {self.__data['smirk']}{self.__data['fingers']}</b>\n\n"
            tam = len(self.__titles)
            
            for i in range(0,tam):
                self.__titles_txt += "<b>Título " + str(i+1) + ": </b><i>" + self.__titles[i][0] + "</i>\n"
            
            self.__titles_txt += f"\nElige una opción {self.__data['winking']}{self.__data['winking']}"
            btns_titles = []
            for i in range(0, tam):
                if i == 0:
                    j = i
                else:
                    j = j + 4
                    
                if j + 1 == tam:
                    aux = [InlineKeyboardButton(text=f"{str(j+1)}",callback_data=str(j+1))]
                    btns_titles.append(aux)
                    break
                elif j + 2 == tam:
                    aux = [InlineKeyboardButton(text=f"{str(j+1)}",callback_data=str(j+1)),
                           InlineKeyboardButton(text=f"{str(j+2)}",callback_data=str(j+2))]
                    btns_titles.append(aux)
                    break
                elif j + 3 == tam:
                    aux = [InlineKeyboardButton(text=f"{str(j+1)}",callback_data=str(j+1)),
                           InlineKeyboardButton(text=f"{str(j+2)}",callback_data=str(j+2)),
                           InlineKeyboardButton(text=f"{str(j+3)}",callback_data=str(j+3))]
                    btns_titles.append(aux)
                    break
                elif j + 4 == tam:
                    aux = [InlineKeyboardButton(text=f"{str(j+1)}",callback_data=str(j+1)),
                           InlineKeyboardButton(text=f"{str(j+2)}",callback_data=str(j+2)),
                           InlineKeyboardButton(text=f"{str(j+3)}",callback_data=str(j+3)),
                           InlineKeyboardButton(text=f"{str(j+4)}",callback_data=str(j+4))]
                    btns_titles.append(aux)
                    break
                else:
                    aux = [InlineKeyboardButton(text=f"{str(j+1)}",callback_data=str(j+1)),
                           InlineKeyboardButton(text=f"{str(j+2)}",callback_data=str(j+2)),
                           InlineKeyboardButton(text=f"{str(j+3)}",callback_data=str(j+3)),
                           InlineKeyboardButton(text=f"{str(j+4)}",callback_data=str(j+4))]
                    btns_titles.append(aux)    
            #json type 
            btns_titles.append([InlineKeyboardButton(text=f"{self.__data['dragon']} Nueva búsqueda {self.__data['magnifying_glass']}", callback_data='SEARCH')])  
            reply = InlineKeyboardMarkup(inline_keyboard=btns_titles)
            self.__btns_titles = json.dumps(reply.to_dict())
            
        elif len(page) == 1:
            anime_titles1, pages = self.__anime.search_titles(anime_title, page[0])
            self.__titles = []
            
            for title in anime_titles1:
                self.__titles.append([anime_titles1[title]['Title'], anime_titles1[title]['Type'], anime_titles1[title]['Ranking'], anime_titles1[title]['Description'], anime_titles1[title]['URL']])
                
            self.__titles_txt = f"<b>Excelente búsqueda {self.__data['smirk']}{self.__data['fingers']}</b>\n\n"
            tam = len(self.__titles)
            
            for i in range(0,tam):
                self.__titles_txt += "<b>Título " + str(i+1) + ": </b><i>" + self.__titles[i][0] + "</i>\n"
            
            self.__titles_txt += f"\n<b>Elige una opción </b>{self.__data['winking']}{self.__data['winking']}"
            btns_titles = []
            for i in range(0, tam):
                if i == 0:
                    j = i
                else:
                    j = j + 4
                    
                if j + 1 == tam:
                    aux = [InlineKeyboardButton(text=f"{str(j+1)}",callback_data=str(j+1))]
                    btns_titles.append(aux)
                    break
                elif j + 2 == tam:
                    aux = [InlineKeyboardButton(text=f"{str(j+1)}",callback_data=str(j+1)),
                           InlineKeyboardButton(text=f"{str(j+2)}",callback_data=str(j+2))]
                    btns_titles.append(aux)
                    break
                elif j + 3 == tam:
                    aux = [InlineKeyboardButton(text=f"{str(j+1)}",callback_data=str(j+1)),
                           InlineKeyboardButton(text=f"{str(j+2)}",callback_data=str(j+2)),
                           InlineKeyboardButton(text=f"{str(j+3)}",callback_data=str(j+3))]
                    btns_titles.append(aux)
                    break
                elif j + 4 == tam:
                    aux = [InlineKeyboardButton(text=f"{str(j+1)}",callback_data=str(j+1)),
                           InlineKeyboardButton(text=f"{str(j+2)}",callback_data=str(j+2)),
                           InlineKeyboardButton(text=f"{str(j+3)}",callback_data=str(j+3)),
                           InlineKeyboardButton(text=f"{str(j+4)}",callback_data=str(j+4))]
                    btns_titles.append(aux)
                    break
                else:
                    aux = [InlineKeyboardButton(text=f"{str(j+1)}",callback_data=str(j+1)),
                           InlineKeyboardButton(text=f"{str(j+2)}",callback_data=str(j+2)),
                           InlineKeyboardButton(text=f"{str(j+3)}",callback_data=str(j+3)),
                           InlineKeyboardButton(text=f"{str(j+4)}",callback_data=str(j+4))]
                    btns_titles.append(aux) 

            btns_titles.append([InlineKeyboardButton(text=f"{self.__data['dragon']} Nueva búsqueda {self.__data['magnifying_glass']}", callback_data='SEARCH')])            
            #json type 
            reply = InlineKeyboardMarkup(inline_keyboard=btns_titles)
            self.__btns_titles = json.dumps(reply.to_dict())
        
        context.bot.send_sticker(chat_id=user_id, 
                    sticker = self.__data['Uff'][random.randrange(0,4)]) 
        update.message.reply_text( 
                                parse_mode="HTML", 
                                text=self.__titles_txt,
                                reply_markup=self.__btns_titles)              
        self.logger.info(f"El usuario {username}/{user_id}, recibio los titulos...")
        
        dc = {'titles': self.__titles, 'titles_txt': self.__titles_txt, 'btns_title': self.__btns_titles}
        self.persistence.update_chat_data_(user_id,dc)
        return self.__three   
              
    def __view_full_desc_anime(self, update, context):
        username = update.effective_user['username']
        user_id = update.effective_user['id']
        query = update.callback_query
        
        self.__titles = self.persistence.get_chat_data_(user_id, 'titles')
        self.__index = self.persistence.get_chat_data_(user_id, 'index')
        
        if query != None:
            query.answer(timeout=25, cache_time=25) 

        if query.data == 'EPISODES_RANGE':
            btns = [[InlineKeyboardButton(text=f"Títulos {self.__data['back']}", callback_data='BACK'), 
                    InlineKeyboardButton(text=f"Ver episodios {self.__data['eyes']}", callback_data=self.__index)],
                    [InlineKeyboardButton(text=f"{self.__data['dragon']} Nueva búsqueda {self.__data['magnifying_glass']}", callback_data='SEARCH')]
                    ] 
            
            reply = InlineKeyboardMarkup(inline_keyboard=btns)
            menu = json.dumps(reply.to_dict())
                
            text = (f"<b>Título: </b><i>{self.__titles[self.__index][0]}</i>\n"
                    f"<b>Tipo: </b><i>{self.__titles[self.__index][1]}</i>\n"
                    f"<b>Valoración: </b><i>{self.__titles[self.__index][2]}</i> {self.__data['star']}\n"
                    f"<b>Descripción: </b><i>{self.__titles[self.__index][3]}</i>")

            query.edit_message_text(parse_mode="HTML", 
                                    text=text,
                                    reply_markup=menu) 
                    
            self.logger.info(f"El usuario {username}/{user_id}, recibio desc del anime y sus episodios...")
            
            return self.__four
        else: 
            self.__index = int(query.data) - 1
            dc = {'index': self.__index}
            self.persistence.update_chat_data_(user_id,dc)
            btns = [[InlineKeyboardButton(text=f"Títulos {self.__data['back']}", callback_data='BACK'), 
                    InlineKeyboardButton(text=f"Ver episodios {self.__data['eyes']}", callback_data=self.__index)],
                    [InlineKeyboardButton(text=f"{self.__data['dragon']} Nueva búsqueda {self.__data['magnifying_glass']}", callback_data='SEARCH')]
                    ] 
            
            reply = InlineKeyboardMarkup(inline_keyboard=btns)
            menu = json.dumps(reply.to_dict())
                
            text = (f"<b>Título: </b><i><u>{self.__titles[self.__index][0]}</u></i>\n"
                    f"<b>Tipo: </b><i><u>{self.__titles[self.__index][1]}</u></i>\n"
                    f"<b>Valoración: </b><i>{self.__titles[self.__index][2]}</i> {self.__data['star']}\n"
                    f"<b>Descripción previa: </b><i>{self.__titles[self.__index][3]}</i>")

            query.edit_message_text(parse_mode="HTML", 
                                    text=text,
                                    reply_markup=menu) 
                    
            self.logger.info(f"El usuario {username}/{user_id}, recibio desc del anime y sus episodios...")
            return self.__four

    def __episodes_range(self, update, context):
        username = update.effective_user['username']
        user_id = update.effective_user['id']
        query = update.callback_query
        if query != None:
            query.answer(timeout=25, cache_time=25)
        
        if query.data == 'LIST_EP':
            index = self.persistence.get_chat_data_(user_id, 'index')
        else: 
            index = int(query.data)
    
        self.__titles = self.persistence.get_chat_data_(user_id, 'titles') 
        url_episode = self.__titles[index][4]
        self.__episodes = self.__anime.search_episodes(url_episode)
        dc = {'episodes': self.__episodes}
        self.persistence.update_chat_data_(user_id, dc)

        val = 95
        num_btns = list(range(0,math.ceil(len(self.__episodes)/val)))
        btns = []
        for i in range(0, len(num_btns)):
            if i == 0:
                j = i
            else:
                j = j + 2
            
            if len(num_btns) == 1:
                aux = [InlineKeyboardButton(text=f"{val*j+1} - {val*(j+1)} {self.__data['monkey']}",callback_data=j+1)]
                btns.append(aux)
                break                
            elif j + 1 == len(num_btns):
                aux = [InlineKeyboardButton(text=f"{val*j+1} - {val*(j+1)} {self.__data['monkey']}",callback_data=j+1)]
                btns.append(aux)
                break
            elif j + 2 == len(num_btns):
                aux = [InlineKeyboardButton(text=f"{val*j+1} - {val*(j+1)} {self.__data['monkey']}",callback_data=j+1), 
                    InlineKeyboardButton(text=f"{val*(j+1)+1} - {val*(j+2)} {self.__data['monkey']}",callback_data=j+2)]
                btns.append(aux)
                break
            elif j == 0:
                aux = [InlineKeyboardButton(text=f"1 - {val} {self.__data['monkey']}",callback_data=j+1), 
                    InlineKeyboardButton(text=f"{val+1} - {val*2} {self.__data['monkey']}",callback_data=j+2)]
                btns.append(aux)               
            else:
                aux = [InlineKeyboardButton(text=f"{val*j+1} - {val*(j+1)} {self.__data['monkey']}",callback_data=j+1), 
                    InlineKeyboardButton(text=f"{val*(j+1)+1} - {val*(j+2)} {self.__data['monkey']}",callback_data=j+2)]
                btns.append(aux)
        
        #json type 
        btns.append([InlineKeyboardButton(text=f"Descripción {self.__data['back']}", callback_data='EPISODES_RANGE'), 
                    InlineKeyboardButton(text=f"Títulos {self.__data['back']}", callback_data='BACK')])
        btns.append([InlineKeyboardButton(text=f"{self.__data['dragon']} Nueva búsqueda {self.__data['magnifying_glass']}", callback_data='SEARCH')])
        reply = InlineKeyboardMarkup(inline_keyboard=btns)
        line_btns = json.dumps(reply.to_dict())
        
        epi_txt = ( f"<b>Título elegido: </b> <i><u>{self.__titles[index][0]}</u></i>\n\n"
                    f"<b>Número de Episodios: </b><i><u>{len(self.__episodes)}</u></i>\n\n"
                    f"<b>Aquí tienes todos los Episodios encontrados {self.__data['monkey2']}{self.__data['monkey2']}</b>\n\n"
                    f"<b>Nota:</b> <i>Los episodios/películas/Especiales/OVA’s se encuentran clasificados en rangos de 95, sin embargo, esto no significa que habrá 95 episodios para una película, por ejemplo.</i>")
        query.edit_message_text( 
                                parse_mode="HTML", 
                                text=epi_txt,
                                reply_markup=line_btns)
        self.logger.info(f"El usuario {username}/{user_id}, solicito rangos de episodios...")
        return self.__five
    
    def __get_number_range_episodes(self, update, context):
        username = update.effective_user['username']
        user_id = update.effective_user['id']
        query = update.callback_query
        if query != None:
            query.answer(timeout=25, cache_time=25) 
            
        if query.data == 'RANGE':
            self.__index_r = self.persistence.get_chat_data_(user_id, 'index_r')
        else: 
            self.__index_r = int(query.data) - 1
            dc = {'index_r' : self.__index_r}
            self.persistence.update_chat_data_(user_id,dc)
        
        self.__groups_epi = []
        
        self.__episodes = self.persistence.get_chat_data_(user_id, 'episodes')
        self.__titles = self.persistence.get_chat_data_(user_id, 'titles')
        self.__index = self.persistence.get_chat_data_(user_id, 'index')

        val = 95
        for i in range(0, len(self.__episodes), val):
            self.__groups_epi.append(self.__episodes[i:i+val])
            
        dc = {'groups_epi': self.__groups_epi}
        self.persistence.update_chat_data_(user_id,dc)
        
        btns = []
        tam = len(self.__groups_epi[self.__index_r])
        for i in range(0, tam):
            if i == 0:
                j = i
            else:
                j = j + 3
            if self.__index_r == 0:
                if j + 1 == tam:
                    aux = [InlineKeyboardButton(text=f"Episodio {j+1}",callback_data=str(self.__index_r) + "-" + str(j+1))]
                    btns.append(aux)
                    break
                elif j + 2 == tam:
                    aux = [InlineKeyboardButton(text=f"Episodio {j+1}",callback_data=str(self.__index_r) + "-" + str(j+1)),
                           InlineKeyboardButton(text=f"Episodio {j+2}",callback_data=str(self.__index_r) + "-" + str(j+2))]
                    btns.append(aux)
                    break
                elif j + 3 == tam:
                    aux = [InlineKeyboardButton(text=f"Episodio {j+1}",callback_data=str(self.__index_r) + "-" + str(j+1)),
                           InlineKeyboardButton(text=f"Episodio {j+2}",callback_data=str(self.__index_r) + "-" + str(j+2)),
                           InlineKeyboardButton(text=f"Episodio {j+3}",callback_data=str(self.__index_r) + "-" + str(j+3))]
                    btns.append(aux)
                    break
                else:
                    aux = [InlineKeyboardButton(text=f"Episodio {j+1}",callback_data=str(self.__index_r) + "-" + str(j+1)),
                           InlineKeyboardButton(text=f"Episodio {j+2}",callback_data=str(self.__index_r) + "-" + str(j+2)),
                           InlineKeyboardButton(text=f"Episodio {j+3}",callback_data=str(self.__index_r) + "-" + str(j+3))]
                    btns.append(aux)
            else:
                if j + 1 == tam:
                    aux = [InlineKeyboardButton(text=f"Episodio {(val*self.__index_r)+(j+1)}",callback_data=str(self.__index_r) + "-" + str(j+1))]
                    btns.append(aux)
                    break
                elif j + 2 == tam:
                    aux = [InlineKeyboardButton(text=f"Episodio {(val*self.__index_r)+(j+1)}",callback_data=str(self.__index_r) + "-" + str(j+1)),
                           InlineKeyboardButton(text=f"Episodio {(val*self.__index_r)+(j+2)}",callback_data=str(self.__index_r) + "-" + str(j+2))]
                    btns.append(aux)
                    break
                elif j + 3 == tam:
                    aux = [InlineKeyboardButton(text=f"Episodio {(val*self.__index_r)+(j+1)}",callback_data=str(self.__index_r) + "-" + str(j+1)),
                           InlineKeyboardButton(text=f"Episodio {(val*self.__index_r)+(j+2)}",callback_data=str(self.__index_r) + "-" + str(j+2)),
                           InlineKeyboardButton(text=f"Episodio {(val*self.__index_r)+(j+3)}",callback_data=str(self.__index_r) + "-" + str(j+3))]
                    btns.append(aux)
                    break
                else:
                    aux = [InlineKeyboardButton(text=f"Episodio {(val*self.__index_r)+(j+1)}",callback_data=str(self.__index_r) + "-" + str(j+1)),
                           InlineKeyboardButton(text=f"Episodio {(val*self.__index_r)+(j+2)}",callback_data=str(self.__index_r) + "-" + str(j+2)),
                           InlineKeyboardButton(text=f"Episodio {(val*self.__index_r)+(j+3)}",callback_data=str(self.__index_r) + "-" + str(j+3))]
                    btns.append(aux)
                    
        btns.append([InlineKeyboardButton(text=f"Lista de Episodios {self.__data['back']}", callback_data='LIST_EP'), 
                    InlineKeyboardButton(text=f"Títulos {self.__data['back']}", callback_data='BACK')])
        btns.append([InlineKeyboardButton(text=f"{self.__data['dragon']} Nueva búsqueda {self.__data['magnifying_glass']}", callback_data='SEARCH')])
        reply = InlineKeyboardMarkup(inline_keyboard=btns)
        line_btns = json.dumps(reply.to_dict())

        epi_txt = ( f"<b>Título elegido: </b> <i><u>{self.__titles[self.__index][0]}</u></i>\n\n"
                    f"<b>Aquí tienes todos los episodios</b> {self.__data['smiling']}")
        query.edit_message_text( 
                                parse_mode="HTML", 
                                text=epi_txt,
                                reply_markup=line_btns)
        self.logger.info(f"El usuario {username}/{user_id}, solicito episodios por rango...") 
        
        return self.__six       
        
    def __download_links(self, update, context):
        username = update.effective_user['username']
        user_id = update.effective_user['id']
        query = update.callback_query
        if query != None:
            query.answer(timeout=25, cache_time=25) 
        
        data = query.data
        index = int(data.split("-")[0])
        epi = int(data.split("-")[1]) -1 
        self.__groups_epi = self.persistence.get_chat_data_(user_id, 'groups_epi')
        self.__index = self.persistence.get_chat_data_(user_id, 'index')
        self.__titles = self.persistence.get_chat_data_(user_id, 'titles')
        url = self.__groups_epi[index][epi]
        links, formats = self.__anime.download_links(url)
        
        text = f"<b>Título elegido: </b> <i><u>{self.__titles[self.__index][0]}</u></i>\n"
        text += f"<b>Episodio: <u><i>{(index*95) + (epi+1)}</i></u></b>\n\n"
        text += f"<b>Aquí tienes los links de descarga {self.__data['star-struck']}{self.__data['star-struck']}</b>\n\n"
        
        for i in range(0,len(links)):
            text +=f"{self.__data['check']}<b>Link {i+1} - {formats[i]}:</b> {links[i]}\n"
            
        btns = []
        btns.append([InlineKeyboardButton(text=f"Episodios {self.__data['back']}", callback_data='RANGE'), 
                    InlineKeyboardButton(text=f"Títulos {self.__data['back']}", callback_data='BACK')])
        btns.append([InlineKeyboardButton(text=f"{self.__data['dragon']} Nueva búsqueda {self.__data['magnifying_glass']}", callback_data='SEARCH')])
        reply = InlineKeyboardMarkup(inline_keyboard=btns)
        line_btns = json.dumps(reply.to_dict())        
        query.edit_message_text( 
                                parse_mode="HTML", 
                                text=text,
                                reply_markup=line_btns,disable_web_page_preview=True)
        self.logger.info(f"El usuario {username}/{user_id}, solicito los links...") 
    
    def __start_bot(self):
        anime_bot = telegram.Bot(token = self.__TOKEN)
        
        self.persistence = FirebasePersistence.from_environment()
        updater = Updater(anime_bot.token, persistence=self.persistence)
        # dispatcher 
        dp = updater.dispatcher
        dp.add_handler(ConversationHandler(
            entry_points=[CommandHandler("start",callback = self.__commandHandler_start),
                          CallbackQueryHandler(pattern='SEARCH', callback=self.__search_msg),
                          CallbackQueryHandler(pattern='ABOUT', callback=self.__about),
                          CallbackQueryHandler(pattern='HELP', callback=self.__help),
                           MessageHandler(filters=Filters.command | Filters.text, callback=self.__unknow_command_handler)
                          ],
            states = {                
                
                self.__two: [
                    CallbackQueryHandler(pattern='BACK', callback=self.__display_titles),
                    CallbackQueryHandler(pattern='SEARCH', callback=self.__search_msg),
                    CallbackQueryHandler(pattern='ABOUT', callback=self.__about),
                    CallbackQueryHandler(pattern='HELP', callback=self.__help),
                    MessageHandler(Filters.text, self.__search_titles)
                                    ],
                
                self.__three: [
                    CallbackQueryHandler(pattern='BACK', callback=self.__display_titles),
                    CallbackQueryHandler(pattern='SEARCH', callback=self.__search_msg),
                    CallbackQueryHandler(pattern='ABOUT', callback=self.__about),
                    CallbackQueryHandler(pattern='HELP', callback=self.__help),
                    CallbackQueryHandler(self.__view_full_desc_anime),
                                    ],
                
                self.__four: [
                    CallbackQueryHandler(pattern='BACK', callback=self.__display_titles),
                    CallbackQueryHandler(pattern='SEARCH', callback=self.__search_msg),
                    CallbackQueryHandler(pattern='ABOUT', callback=self.__about),
                    CallbackQueryHandler(pattern='HELP', callback=self.__help),
                    CallbackQueryHandler(pattern='EPISODES_RANGE', callback=self.__view_full_desc_anime),
                    CallbackQueryHandler(callback=self.__episodes_range),
                              ],
                
                self.__five: [
                    CallbackQueryHandler(pattern='BACK', callback=self.__display_titles),
                    CallbackQueryHandler(pattern='SEARCH', callback=self.__search_msg),
                    CallbackQueryHandler(pattern='ABOUT', callback=self.__about),
                    CallbackQueryHandler(pattern='HELP', callback=self.__help),
                    CallbackQueryHandler(pattern='LIST_EP', callback=self.__episodes_range),
                    CallbackQueryHandler(pattern='EPISODES_RANGE', callback=self.__view_full_desc_anime),
                    CallbackQueryHandler(self.__get_number_range_episodes),
                ],
                
                self.__six : [
                    CallbackQueryHandler(pattern='BACK', callback=self.__display_titles),
                    CallbackQueryHandler(pattern='SEARCH', callback=self.__search_msg),
                    CallbackQueryHandler(pattern='ABOUT', callback=self.__about),
                    CallbackQueryHandler(pattern='HELP', callback=self.__help),
                    CallbackQueryHandler(pattern='RANGE', callback=self.__get_number_range_episodes),
                    CallbackQueryHandler(pattern='LIST_EP', callback=self.__episodes_range),
                    CallbackQueryHandler(self.__download_links),
                    ]
                },
            fallbacks = [CommandHandler("start",callback = self.__commandHandler_start)],
            name="my_conversation",
            persistent=True
        ))
        
        
        if self.__mod == "dev":
            #get request from telegram 
            updater.start_polling()
            print("::::::::::::::::::::::::::::::::::::Starting BOT::::::::::::::::::::::::::::::::::::::")
            #close with CTRL + C
            updater.idle()
            
        elif self.__mod == "prod": 
            __HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
            PORT = int(os.environ.get('PORT', '8443'))
            
            updater.start_webhook(
                listen="0.0.0.0",
                port = PORT, 
                url_path = self.__TOKEN,
                webhook_url=f"https://{__HEROKU_APP_NAME}.herokuapp.com/{self.__TOKEN}",
                bootstrap_retries=5  
            )
            
            print("::::::::::::::::::::::::::::::::::::Starting BOT::::::::::::::::::::::::::::::::::::::")
            updater.idle()
        else:
            self.logger.info("No se especificó ningún modo de trabajo")
            sys.exit()
        
if __name__ == "__main__":
    Anime_Bot()        