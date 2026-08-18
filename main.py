import telegram
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update, InlineKeyboardMarkup, \
    InlineKeyboardButton
from telegram.ext import Application, CommandHandler, InlineQueryHandler, CallbackContext, MessageHandler, filters, \
    CallbackQueryHandler
from text import dictionary
from sql import *
import random
import asyncio
import xlwt
import os
from dotenv import load_dotenv
load_dotenv()
CAPTCHA = ['🍐', '🍏', '🍊', '🍌', '🍉', '🍇', '🍓', '🍅', '🥝', '🥥', '🍍', '🥭', '🍑', '🥦', '🥬', '🌶', '🌽', '🍒', '🍈', '🥑']
CHANNEL_ID = -1002125713131
DEVELOPER_ID = 6503537991


def button(type: str = None, **kwargs) -> InlineKeyboardMarkup:
    btn = []
    if type == 'language':
        btn.append([InlineKeyboardButton('O\'zbek tili', callback_data='uz'),
                    InlineKeyboardButton('Русский язык', callback_data='ru')])
    elif type == 'captcha':
        btn = [[InlineKeyboardButton(i, callback_data=f"captcha_{i}") for i in kwargs.get('captcha')]]

    elif type == 'search':
        language = get_user(kwargs.get('user_id'))[3]
        genres = dictionary(language, 'movie_ctg')
        for i in range(0, len(genres) - 1, 2):
            btn.append(
                [
                    InlineKeyboardButton(genres[i][0], switch_inline_query_current_chat=genres[i][1]),
                    InlineKeyboardButton(genres[i + 1][0], switch_inline_query_current_chat=genres[i + 1][0])
                ]
            )

        btn.append([InlineKeyboardButton('Poisk🔍', switch_inline_query_current_chat='')])
    elif type == 'admin_button':
        btn = [[InlineKeyboardButton("Ha", callback_data='ha'), InlineKeyboardButton("Yo'q", callback_data="yo'q")]]
    elif type == 'watch':
        language = get_user(kwargs.get('user_id'))[3]
        btn = [[InlineKeyboardButton(dictionary(language, 'watch'), callback_data=kwargs.get('id'))]]
    return InlineKeyboardMarkup(btn)


async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    old_user = get_user(user.id)
    if old_user is None:
        create_user(user.id)
    try:
        if old_user[2] == '1':
            language = old_user[3]
            update_user(user_id=user.id, state=0)
            await update.message.reply_text(dictionary(language, 'greeting'), parse_mode='HTML',
                                            reply_markup=button(type='search', user_id=user.id))
        else:
            random_captcha = random.sample(CAPTCHA, 3)
            chosen_captcha = random.choice(random_captcha)
            await update.message.reply_text(dictionary(old_user[3], 'captcha') + chosen_captcha,
                                            reply_markup=button(type='captcha', captcha=random_captcha),
                                            parse_mode='HTML')
    except (KeyError, TypeError):
        await update.message.reply_text("🇺🇿 - Tilni tanlang!\n\n🇷🇺 - Выберите язык!",
                                        reply_markup=button(type='language'))


async def message_handler(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    old_user = get_user(user.id)
    message = update.message.text

    if old_user is None or old_user[3] is None:
        create_user(user.id) if old_user is None else get_user(user.id)
        await update.message.reply_text("🇺🇿 - Tilni tanlang!\n\n🇷🇺 - Выберите язык!",
                                        reply_markup=button(type='language'))
        return None
    elif user.id == DEVELOPER_ID and old_user[4] == 5:
        if old_user[4] == 5:
            global MESSAGE_ID
            MESSAGE_ID = update.message.message_id
            await update.message.reply_text("Barcha foydalanuchilarga jo'natishni xoxlaysizmi?",
                                            reply_markup=button(type='admin_button'), reply_to_message_id=MESSAGE_ID)
            return
    if message.isdigit() and old_user[2] == '1':
        movie_id = search_movie_by_id(int(message))
        try:
            await context.bot.copyMessage(chat_id=user.id, from_chat_id=CHANNEL_ID, message_id=movie_id[0])
        except Exception as e:
            print(e)
            await update.message.reply_text(dictionary(old_user[3], 'code_error'))
    elif message.startswith(dictionary(old_user[3], 'click_watching')) or old_user[2] is None:
        random_captcha = random.sample(CAPTCHA, 3)
        chosen_captcha = random.choice(random_captcha)
        await update.message.reply_text(dictionary(old_user[3], 'captcha') + chosen_captcha,
                                                reply_markup=button(type='captcha', captcha=random_captcha),
                                                parse_mode='HTML') if old_user[2] is None else None
    else:
        await update.message.reply_text(dictionary(old_user[3], 'not_int'))


async def inline_handler(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    old_user = get_user(user.id)
    query = update.callback_query
    if query.data in ['uz', 'ru']:
        old_user = update_user(user.id, language=query.data)
        random_captcha = random.sample(CAPTCHA, 3)
        chosen_captcha = random.choice(random_captcha)
        await query.edit_message_text(dictionary(old_user[3], 'captcha') + chosen_captcha,
                                      reply_markup=button(type='captcha', captcha=random_captcha), parse_mode='HTML')
    elif query.data.startswith('captcha'):
        splitted_data = query.data.split('_')
        if splitted_data[1] == query.message.text[-1]:
            await query.delete_message()
            update_user(user.id, is_user=True)
            await query.message.reply_text(dictionary(old_user[3], 'greeting'), parse_mode='HTML',
                                           reply_markup=button(type='search'))
        else:
            random_captcha = random.sample(CAPTCHA, 3)
            chosen_captcha = random.choice(random_captcha)
            await query.edit_message_text('❌' + dictionary(old_user[3], 'captcha') + chosen_captcha,
                                          reply_markup=button(type='captcha', captcha=random_captcha),
                                          parse_mode='HTML')
    elif query.data.isdigit():
        await context.bot.copy_message(chat_id=user.id, from_chat_id=CHANNEL_ID, message_id=int(query.data))
    elif query.data == 'category':
        pass
    elif update.effective_user.id == DEVELOPER_ID and old_user[4] == 5:
        await query.delete_message()
        if update.callback_query.data == 'ha':
            asyncio.create_task(msg_to_users(update, context))
            update_user(user.id, state=1)
        elif update.callback_query.data == 'yo\'q':
            await update.callback_query.message.reply_text("Jarayon bekor qlindi.")
            update_user(user_id=user.id, state=1)


async def inline_query(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    user = update.effective_user
    old_user = get_user(user.id)
    if not query:
        movies = get_movies()
    else:
        movies = search_movie_by_name(query)
        if movies == []:
            movies = search_movie_by_ctg(query)
    results = [
        InlineQueryResultArticle(
            id=movie[0],
            title=movie[1],
            input_message_content=InputTextMessageContent(
                message_text=f"{dictionary(old_user[3], 'click_watching')}\n\n{movie[5]}"),
            description=movie[5],
            thumbnail_url=movie[6],
            reply_markup=button(type='watch', user_id=user.id, id=movie[2]),
        ) for movie in movies
    ]

    await update.inline_query.answer(results, cache_time=5, auto_pagination=True)


async def bot_info(update: Update, context: CallbackContext):
    await update.message.delete()
    if update.effective_user.id != DEVELOPER_ID:
        return 0
    if update.message.text == '/excel':
        response = f'users.xls'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Users')

        # Sheet header, first row
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        columns = ['user_id', 'reequests', 'is_user', 'language', 'state', 'created_at', 'updated_at']
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()
        rows = get_user()[0]
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        dr = wb.add_sheet('Movies')
        dr_row_num = 0
        dr_colums = ['ID', 'video_id', 'created_at', 'updated_at', 'description']
        for col_num in range(len(dr_colums)):
            dr.write(dr_row_num, col_num, dr_colums[col_num], font_style)

        dr_row = get_movies()
        for row in dr_row:
            dr_row_num += 1
            for col_num in range(len(row)):
                dr.write(dr_row_num, col_num, row[col_num], font_style)

        wb.save(response)
        user = update.effective_user
        await context.bot.send_document(chat_id=user.id, document=open(f'{response}', 'rb'))
    elif update.message.text == '/stats':
        users = get_user()
        text = f"Umumiy Obunachilar: {users[1][0][0]}\nBot emas: {users[2][0][0]}\nBugun qo'shildi: {users[3][0][0]}\nBu hafta qo'shildi: {users[4][0][0]}\nBu oy qo'shildi: {users[5][0][0]}\nSo'rovlar soni: {users[6][0][0]}"
        await update.message.reply_text(text)
    elif update.message.text == '/ads':
        update_user(update.effective_user.id, state=5)
        await update.message.reply_text('Reklamani jo\'natishingiz mumkin!')


async def msg_to_users(update: Update, context: CallbackContext):
    receivers, deactivated, blocks = 0, 0, 0
    await update.callback_query.message.reply_text(
        "Jarayon boshlandi, javob qaytmagunicha boshqa reklama jo'natmang!!!")
    users = get_user()
    for user in users[0]:
        try:
            await context.bot.copyMessage(chat_id=user[0], from_chat_id=DEVELOPER_ID,
                                          message_id=MESSAGE_ID,
                                          read_timeout=1000, write_timeout=1000, connect_timeout=1000)
            receivers += 1
        except telegram.error.Forbidden as e:
            if 'Forbidden: bot was blocked by the user' in str(e):
                blocks += 1
            elif 'Forbidden: user is deactivated' in str(e):
                deactivated += 1
            await context.bot.send_message(chat_id=DEVELOPER_ID,
                                           text=f"Yetkazildi: {receivers} da foydalanuvchiga\n{e}",
                                           read_timeout=1000, write_timeout=1000, connect_timeout=1000)
        await asyncio.sleep(0.1)
    await context.bot.send_message(chat_id=DEVELOPER_ID,
                                   text=f"JARAYON: Tugadi!\n\n Xabar Yetkazildi: {receivers}/{users[1][0][0]} da foydalanuvchiga\n\nBloklar soni: {blocks}\n\nDeactivated: {deactivated}",
                                   read_timeout=1000, write_timeout=1000, connect_timeout=1000)


async def help(update: Update, context: CallbackContext):
    user = update.effective_user
    old_user = get_user(user.id)
    if old_user is None:
        create_user(user.id)
    try:
        if old_user[2] == '1':
            language = old_user[3]
            update_user(user_id=user.id, state=0)
            await update.message.reply_text(dictionary(language, 'help'), parse_mode='HTML',
                                            reply_markup=button(type='search'))
        else:
            random_captcha = random.sample(CAPTCHA, 3)
            chosen_captcha = random.choice(random_captcha)
            await update.message.reply_text(dictionary(old_user[3], 'captcha') + chosen_captcha,
                                            reply_markup=button(type='captcha', captcha=random_captcha),
                                            parse_mode='HTML')
    except KeyError:
        await update.message.reply_text("🇺🇿 - Tilni tanlang!\n\n🇷🇺 - Выберите язык!",
                                        reply_markup=button(type='language'))


async def language(update: Update, context: CallbackContext):
    await update.message.reply_text("🇺🇿 - Tilni tanlang!\n\n🇷🇺 - Выберите язык!",
                                    reply_markup=button(type='language'))


def main() -> None:

    TOKEN = os.getenv("TOKEN")
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ads", bot_info))
    application.add_handler(CommandHandler("excel", bot_info))
    application.add_handler(CommandHandler("stats", bot_info))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("lang", language))
    application.add_handler(InlineQueryHandler(inline_query))
    application.add_handler(MessageHandler(filters.TEXT & ~ filters.COMMAND, message_handler))
    application.add_handler(CallbackQueryHandler(inline_handler))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
