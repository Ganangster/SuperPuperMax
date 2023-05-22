import asyncio
import logging
import random
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from aiogram.dispatcher.filters import CommandStart, Command
from datetime import datetime, timedelta
from aiogram.types.message import ContentType
import emoji
import sqlite3 as sq

API_TOKEN = '6137672948:AAGKD2Zivl1g00qOwLG8IFkZBraIqXN1_WQ'
SBERBANK_TOKEN = "401643678:TEST:3b2704a4-6a00-4862-91b4-a8b9fa37e861"
PAYMASTER_TOKEN = "1744374395:TEST:240901a79451fe4a374c"
QKASSA_TOKEN = "381764678:TEST:57493"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)



"######################################################ПЛАТЕЖИ#########################################################"

PRICESS = types.LabeledPrice(label="Деньга на чокопай", amount=100*100)
PRICES = types.LabeledPrice(label="Деньга на чокопай", amount=500*100)
PRICE = types.LabeledPrice(label="Деньга на чокопай", amount=100*100)



@dp.message_handler(commands=['Наш_сайт'], chat_type=['private'])
async def private_command_handler(message: types.Message):
    if SBERBANK_TOKEN.split(':')[1] == 'TEST':
        user_id = message.from_user.id
        if user_id not in user_states or user_states[user_id] != 'started':
            await message.answer('Сперва введите команду /start для начала работы бота!')
            return
        if not await cooldown_handler(message):
            return
        await bot.send_message(message.from_user.id, 'Мы бедные, нету деньга \nна хостинги =(')
        await asyncio.sleep(2)
        await bot.send_message(message.from_user.id, 'Но ты можешь это исправить! Задонать пожалуйста!')
        await asyncio.sleep(2)
        await bot.send_message(message.from_user.id, "Донат Максиму, это тестовый платеж!!!")
        await asyncio.sleep(2)
    await bot.send_invoice(message.chat.id,
                           title="Донат Максиму уровень: скупой",
                           description="Деньга Максиму на чокопай",
                           provider_token=QKASSA_TOKEN,
                           currency="rub",
                           photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           need_email=True,
                           max_tip_amount=5000,
                           suggested_tip_amounts=[500, 1000, 2000, 5000],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")
    await asyncio.sleep(2)
    await bot.send_invoice(message.chat.id,
                           title="Донат Максиму  уровень: щедрый",
                           description="Деньга Максиму на чокопай",
                           provider_token=QKASSA_TOKEN,
                           currency="rub",
                           photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICES],
                           need_email=True,
                           max_tip_amount=5000,
                           suggested_tip_amounts=[500, 1000, 2000, 5000],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")
    await asyncio.sleep(2)
    await bot.send_invoice(message.chat.id,
                           title="Донат Максиму! \nуровень: Богатый",
                           description="Деньга Максиму на чокопай",
                           provider_token=QKASSA_TOKEN,
                           currency="rub",
                           photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICES],
                           need_email=True,
                           max_tip_amount=5000,
                           suggested_tip_amounts=[500, 1000, 2000, 5000],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")



@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


ADMIN_CHAT_ID = "5252216460"
#Сообщает об отправленом платеже
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    email = payment_info.get('order_info')
    amount = payment_info.get('total_amount')
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await bot.send_message(message.chat.id,f"Платёж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")
    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Новая покупка: {email}, {amount} руб.")



b1 = KeyboardButton('/start')
b2 = KeyboardButton('/help')
b3 = KeyboardButton('/info')
b4 = KeyboardButton('/Портфолио')
b5 = KeyboardButton('/Наш_сайт')
b6 = KeyboardButton('/commands')
b7 = KeyboardButton('/menu')
b8 = KeyboardButton('Антоновка'+emoji.emojize(":hear-no-evil_monkey:"))
b9 = KeyboardButton('Макс')
b10 = KeyboardButton('/Секреты_макса')
b11 = KeyboardButton('/Покормить')
b12 = KeyboardButton('Основная')
b13 = KeyboardButton('Макс1')
b14 = KeyboardButton('Отмена')
b15 = KeyboardButton('Макс2')
b16 = KeyboardButton('Далее-->')
b17 = KeyboardButton('<--Назад')
b18 = KeyboardButton('Далее-->>')
b19 = KeyboardButton('<<--Назад')
b20 = KeyboardButton('Макс лох')
b21 = KeyboardButton('Максим мамонт')
b22 = KeyboardButton('Режим разговора')
b23 = KeyboardButton('Максим мамонт')
b24 = KeyboardButton('Максим')
b25 = KeyboardButton('Максим дебил')
b80 = KeyboardButton('Шутка--1')
b81 = KeyboardButton('Шутка--2')
b82 = KeyboardButton('Шутка--3')
b83 = KeyboardButton('Шутка--4')
b84 = KeyboardButton('Шутка--5')
b85 = KeyboardButton('Шутка--6')
b86 = KeyboardButton('Шутка--7')
b87 = KeyboardButton('Шутка--8')
b88 = KeyboardButton('Шутка--9')
b89 = KeyboardButton('Шутка--Бомба')
b90 = KeyboardButton('Шутка-1')
b91 = KeyboardButton('Шутка-2')
b92 = KeyboardButton('Шутка-3')
b93 = KeyboardButton('Шутка-4')
b94 = KeyboardButton('Шутка-5')
b95 = KeyboardButton('Шутка-6')
b96 = KeyboardButton('Шутка-7')
b97 = KeyboardButton('Шутка-8')
b98 = KeyboardButton('Шутка-9')
b99 = KeyboardButton('<Назад>')
b100 = KeyboardButton('Шутка-Бомба')
b101 = KeyboardButton('Чёрный юмор')
b102 = KeyboardButton('Белый юмор')
b103 = KeyboardButton('Шутка-Бомба')
b104 = KeyboardButton('Шутки')
b105 = KeyboardButton('`Назад`')
b106 = KeyboardButton('АУФФ')
b107 = KeyboardButton('Пожиратель чокопаек'+emoji.emojize(":red_envelope:"))
b108 = KeyboardButton('Мамонт'+emoji.emojize(":mammoth:"))
b109 = KeyboardButton('Антоновка')
b110 = KeyboardButton('Позывные Макса')
b111 = KeyboardButton('/Страхи_макса')
b112 = KeyboardButton('Факты')
b113 = KeyboardButton('Стихи')
b114 = KeyboardButton('/ГДЗ')
b115 = KeyboardButton('Линуксоид'+emoji.emojize(":alien:"))
b116 = KeyboardButton('Желток'+emoji.emojize(":full_moon:"))
b117 = KeyboardButton('/Удалить')
b118 = KeyboardButton('/Загрузить')
b119 = KeyboardButton('/Портфолио')
b120 = KeyboardButton('Меню админа')
b121 = KeyboardButton('Панель админа')
b122 = KeyboardButton('Отмена')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.add(b1).row(b2,b6,b3).row(b5,b4).add(b7).add(b16)

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True)

kb_menu.add(b12).row(b13,b15).add(b14)

kb_max1 = ReplyKeyboardMarkup(resize_keyboard=True)

kb_max1.add(b24).row(b106,b9,b113).row(b114).row(b17,b18)

kb_max2 = ReplyKeyboardMarkup(resize_keyboard=True)

kb_max2.add(b110).row(b112,b22,b104).row(b10,b111).row(b19)

kb_menushutka = ReplyKeyboardMarkup(resize_keyboard=True)

kb_menushutka.add(b101,b102).add(b105)

kb_white = ReplyKeyboardMarkup(resize_keyboard=True)

kb_white.add(b99).row(b80,b81,b82).row(b83,b84,b85).row(b86,b87,b88).add(b89)

kb_black = ReplyKeyboardMarkup(resize_keyboard=True)

kb_black.add(b99).row(b90,b91,b92).row(b93,b94,b95).row(b96,b97,b98).add(b100)

kb_pozovnue = ReplyKeyboardMarkup(resize_keyboard=True)

kb_pozovnue.add(b107).add(b115).add(b109).add(b108).add(b116)

kb_admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin_panel.add(b119).row(b117,b118).add(b120)

kb_admin_menu = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin_menu.add(b12).row(b15,b13).add(b121)

kb_admin_redaction = ReplyKeyboardMarkup(resize_keyboard=True)

kb_admin_redaction.add(b122)


user_states = {}                                                #КОМАНДЫ#
used_set = set()
class UserState(StatesGroup):
    name = State()
    years = State()

@dp.message_handler(commands=['start'], chat_type=['private'])
async def private_command_handler(message: types.Message):
    if message.from_user.id in used_set:
        await message.reply("Вы уже начали работу бота!")
    else:
        user_id = message.from_user.id
        user_states[user_id] = 'started'
        await bot.send_message(message.from_user.id, "Дарова огрызок!\nЯ существую для того, чтобы тебя оскорблять! Знай, больше всего я ненавижу тех, кто играет в ПК, те сразу получают по роже костетом.\nОгрызок, как тебя звать то? Чтобы представиться напиши своё имя!", reply_markup=types.ReplyKeyboardRemove())
        used_set.add(message.from_user.id)
        await UserState.name.set()

@dp.message_handler(state=UserState.name)
async def get_username(message: types.Message, state: FSMContext):
        await state.update_data(username=message.text)
        await bot.send_message(message.from_user.id, "Отлично! Теперь введите свой возвраст.")
        await UserState.next() # либо же UserState.adress.set()


@dp.message_handler(lambda message: not message.text.isdigit(), state=UserState.years)
async def process_age_invalid(message: types.Message):
    return await message.reply("Напиши возраст!")


@dp.message_handler(state=UserState.years)
async def get_address(message: types.Message, state: FSMContext):
    await state.update_data(years=message.text)
    data = await state.get_data()
    await bot.send_message(message.from_user.id, f"Имя: {data['username']}\n" f"Возвраст: {data['years']}", reply_markup=kb_client)
    await state.reset_state(with_data=False)

    ###################REG###############

                                        #####АНТИ СПАМ##############

# Отслеживание последнего использования команд
last_used = {}
# Указание времени кулдауна в секундах
cooldown_time = 2

async def cooldown_handler(message: types.Message):
    # получение идентификатора пользователя
    user_id = message.from_user.id
    # получение текущего времени
    current_time = datetime.now()

    if user_id in last_used:
        # вычисление времени, прошедшего с последнего использования команды
        time_diff = current_time - last_used[user_id]
        # проверка, прошло ли время кулдауна
        if time_diff < timedelta(seconds=cooldown_time):
            # отправка сообщения об ожидании
            sent_message = await bot.send_message(message.from_user.id, "Вы используете команды слишком часто, \nподождите пожалуйста!")
            await asyncio.sleep(3)
            await bot.delete_message(sent_message.chat.id, sent_message.message_id)
            return False

    # обновление времени последнего использованной команды для пользователя
    last_used[user_id] = current_time
    return True


# Отслеживание последнего использования команд
last_used = {}
# Указание времени кулдауна в секундах
cooldowns_time = 5

async def cooldowns_handler(message: types.Message):
    # получение идентификатора пользователя
    user_id = message.from_user.id
    # получение текущего времени
    current_time = datetime.now()

    if user_id in last_used:
        # вычисление времени, прошедшего с последнего использования команды
        time_diff = current_time - last_used[user_id]
        # проверка, прошло ли время кулдауна
        if time_diff < timedelta(seconds=cooldowns_time):
            # отправка сообщения об ожидании
            return False

    # обновление времени последнего использованной команды для пользователя
    last_used[user_id] = current_time
    return True


last_useds = {}
# Указание времени кулдауна в секундах
cooldownss_time = 20

async def cooldownss_handler(message: types.Message):
    # получение идентификатора пользователя
    user_id = message.from_user.id
    # получение текущего времени
    current_time = datetime.now()

    if user_id in last_useds:
        # вычисление времени, прошедшего с последнего использования команды
        time_diff = current_time - last_useds[user_id]
        # проверка, прошло ли время кулдауна
        if time_diff < timedelta(seconds=cooldownss_time):
            sent_message = await bot.send_message(message.from_user.id,"Вы уже смотрели гарелею максима, \nподождите пожалуйста для отправки новой команды!")
            await asyncio.sleep(3)
            await bot.delete_message(sent_message.chat.id, sent_message.message_id)
            return False

    # обновление времени последнего использованной команды для пользователя
    last_useds[user_id] = current_time
    return True





@dp.message_handler(commands=['Инфо', 'info','Помощь', 'help','commands', 'команды','Наш_сайт','Портфолио','Покормить','Секретная_Функция','menu','Секреты_макса','Страхи_макса','ГДЗ', 'start'], chat_type=['group', 'supergroup'])
async def group_command_handler(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "Бот работает через ЛС!!! Бот: https://t.me/SuperPuperMax_bot")

@dp.message_handler(commands=['info'], chat_type=['private'])
async def private_command_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    data = await state.get_data()
    await bot.send_message(message.from_user.id, emoji.emojize(f"Привет, {data['username']} :backhand_index_pointing_up: !") + "\nЭтот бот посвещён Максиму Антоновке,\nкто знает тот знает!\n\nВ этом боте ты найдёшь много весёлого, интересного и развлекательного, \nточно незаскучаешь!!! \n\nОтдельную благодарность, \nпо разработке бота, хочу выразить \nМаргарите Сергеевне! \nЛучший препод по питону!\n\nТак же, хочу поблагодарить Максима, \nглавного персанажа этого бота,\nза то что он следит за дисциплиной,\nочень весёлый, короче, с ним не заскучаешь!\n\nСоздатель бота Роман,\nесли тебе что-то непонятно,\nnнапиши /help")

@dp.message_handler(commands=['Помощь', 'help'], chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await bot.send_message(message.from_user.id, 'Привет! Нужна помощь? \n\nДля информации об этом боте, \nнапиши /info \n\nДля помощи с командами, \nнапиши /comands, либо же, \nты можешь воспользоваться клавиатурой! ')

@dp.message_handler(commands=['commands', 'команды'], chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return

    if not await cooldown_handler(message):
        return
    await bot.send_message(message.from_user.id, 'Команды:\n\n/info - информация о боте!\n/help - помощь в боте!\n/menu - меню бота!\n/Наш_сайт - донат!\n/Портфолио - галлерея Максима\n/Покормить - покормить Максима\n/Секретная функция - секретная функция!\n/Секреты_макса - секреты Макса!\n/Страхи_макса - страхи Макса\n/ГДЗ - все вспомогательные шаблоны по python!\n/Режим_разговора -Режим разговора с Максимом!\n\nРеакции:\n\nАУФФ - отправляет ауфф от Максима!\nФакты - интересные факты от Максима!\nПозывные Макса - меню с позывными Максима!\nСтихи - стих от Жеки для Макса\nШутки - меню с шутками!\n\n\nПозыные Максима: Антоновка, Желток,\nПожиратель чокопаек,Мамонт,Линуксоид, Макс, Максим.\n\n\nОбзывные Максима: Максим или Макс лох, даун, бестолочь, тварь\nимбицил, лошара, полудурок, тупой, мамонт, дебил. ')


@dp.message_handler(commands=['Наш_сайт'], chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await bot.send_message(message.from_user.id, 'Мы бедные, нету деньга \nна хостинги =(')

@dp.message_handler(commands=['Портфолио'], chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    await sql_read(message)

@dp.message_handler(commands=['Покормить'], chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await bot.send_message(message.from_user.id,  'Ням ням ням, спасибо! \nВкусная была печенька!')


@dp.message_handler(commands=['Секретная_Функция'], chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await bot.send_message(message.from_user.id,  'Цссссс! Секретная функция!''\nПожалуйста подождите')
    await bot.send_video(message.from_user.id, open('Антоновка.mp4', 'rb'))

@dp.message_handler(commands=['menu'], chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await bot.send_message(message.from_user.id, 'Выбери вспомогательную клавиатуру \nдля удобного пользования бота! \n\nДля отмены /Отменить', reply_markup=kb_menu)



'##################################################!!!!МАШИННОЕ СОСТАЯНИЕ!!!!#########################################################'
"######################################################МАШИННОЕ СОСТАЯНИЕ#########################################################"
'##################################################!!!!МАШИННОЕ СОСТАЯНИЕ!!!!#########################################################'

ID = "5252216460"

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


@dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Что хозяин надо???', reply_markup=kb_admin_panel)
    await message.delete()

@dp.message_handler(commands="Загрузить", state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото', reply_markup=kb_admin_redaction)

@dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Теперь введи название!')

@dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи описание')

@dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь напиши Автора!')

@dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = message.text

    try:
        await sql_add_command(state)
        await message.reply('Вы добавили в /Портфолио новые данные!', reply_markup=kb_admin_panel)
        await state.finish()
    except:
        await message.reply("Подождите!")

@dp.message_handler(state="*", commands='отмена')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Вы отменили действие!')


@dp.message_handler(commands='Удалить')
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nАвтор: {ret[3]} ')
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup(). \
                add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена.', show_alert=True)




'##################################################!!!!БАЗА ДАННЫХ!!!!#########################################################'
"######################################################БАЗА ДАННЫХ#########################################################"
'##################################################!!!!БАЗА ДАННЫХ!!!!#########################################################'


def sql_start():
    global base,cur
    base = sq.connect('Super_Max.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
    base.commit()
async def sql_add_command(state):
    async with state.proxy() as data:
        global base, cur
        base = sq.connect('Super_Max.db')
        cur = base.cursor()
        base.execute('CREATE TABLE IF NOT EXISTS menu(img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)')
        cur.execute('INSERT INTO menu VALUES(?, ?, ?, ?)', tuple(data.values()))
        base.commit()

async def sql_read(message):
    global base, cur
    base = sq.connect('Super_Max.db')
    cur = base.cursor()
    for ret in cur.execute('SELECT * FROM menu').fetchall():
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nАвтор: {ret[3]} ')

async def sql_read2():
    global base, cur
    base = sq.connect('Super_Max.db')
    cur = base.cursor()
    return cur.execute('SELECT * FROM menu').fetchall()

async def sql_delete_command(data):
    global base, cur
    base = sq.connect('Super_Max.db')
    cur = base.cursor()
    cur.execute('DELETE FROM menu WHERE name == ?', (data,))
    base.commit()

'##################################################!!!!ПАНЕЛИ И МЕНЮ!!!!#########################################################'
"######################################################ПАНЕЛИ И МЕНЮ#########################################################"
'##################################################!!!!ПАНЕЛИ И МЕНЮ!!!!#########################################################'





@dp.message_handler(regexp='Панель админа', chat_type=['private'])
async def private_command_handler(message: types.Message):
    if message.from_user.id == ID:
        await message.answer("Вы поменяли клавиатуру, Панель админа", reply_markup=kb_admin_panel)

@dp.message_handler(regexp='Меню админа', chat_type=['private'])
async def private_command_handler(message: types.Message):
    if message.from_user.id == ID:
        await message.answer("Вы поменяли клавиатуру, Панель админа", reply_markup=kb_admin_menu)



'##################################################!!!!ИНЛАЙН КЛАВИАТУРЫ!!!!#########################################################'
"######################################################ИНЛАЙН КЛАВИАТУРЫ#########################################################"
'##################################################!!!!ИНЛАЙН КЛАВИАТУРЫ!!!!#########################################################'

'##################################################!!!!СЕКРЕТЫ МАКСА!!!!#########################################################'

inkb1 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text="`Секрет 1`", callback_data="bk1")).add(InlineKeyboardButton(text="`Секрет 2`", callback_data="bk2")).add(InlineKeyboardButton(text="`Секрет 3`", callback_data="bk3")).add(InlineKeyboardButton(text="`Секрет 4`", callback_data="bk4"))


@dp.message_handler(commands=['Секреты_макса'], chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    with open("SISСекреты.png", "rb") as photo_file:
        await bot.send_photo(chat_id=message.from_user.id, photo=photo_file, caption='Выбери любой секрет макса, который хочешь узнать!', reply_markup=inkb1)



@dp.callback_query_handler(text="bk1")
async def bk1_call(calback: types.CallbackQuery):
    await calback.message.answer("Меня на свидание звал Жека!")
    await calback.answer()

@dp.callback_query_handler(text="bk2")
async def bk1_call(calback: types.CallbackQuery):
    await calback.message.answer("За хорошее поведение, Маргарита Сергеевна подкармливает меня чокопайками! \nЗа это я её уважаю!")
    await calback.answer()

@dp.callback_query_handler(text="bk3")
async def bk1_call(calback: types.CallbackQuery):
    await calback.message.answer("Я храню чай и овсянку в тумбочке, стаящая в хайтеке!")
    await calback.answer()

@dp.callback_query_handler(text="bk4")
async def bk1_call(calback: types.CallbackQuery):
    await calback.message.answer("У меня есть фиолетовый, пластмассовый костет!")
    await calback.answer()


'##################################################!!!!СТРАХИ МАКСА!!!!#########################################################'



inkb2 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text="`Страх 1`", callback_data="bk5")).add(InlineKeyboardButton(text="`Страх 2`", callback_data="bk6")).add(InlineKeyboardButton(text="`Страх 3`", callback_data="bk7")).add(InlineKeyboardButton(text="`Страх 4`", callback_data="bk8"))

@dp.message_handler(commands=['Страхи_макса'], chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    with open("SISСтрахи.png", "rb") as photo_file:
        await bot.send_photo(chat_id=message.from_user.id, photo=photo_file, caption='Выбери любой страх Макса, который хочешь узнать!', reply_markup=inkb2)


@dp.callback_query_handler(text="bk5")
async def bk1_call(calback: types.CallbackQuery):
    await calback.message.answer("Максим очень сильно боиться сисадмина")
    await calback.answer()

@dp.callback_query_handler(text="bk6")
async def bk1_call(calback: types.CallbackQuery):
    await calback.message.answer("Максим очень боиться переделывать платы")
    await calback.answer()

@dp.callback_query_handler(text="bk7")
async def bk1_call(calback: types.CallbackQuery):
    await calback.message.answer("Максим не любит докладных")
    await calback.answer()

@dp.callback_query_handler(text="bk8")
async def bk1_call(calback: types.CallbackQuery):
    await calback.message.answer("Самый главный страх максима! \nОн боиться остаться голодным...")
    await calback.answer()


'##################################################!!!!ГДЗ!!!!#########################################################'




inkb3 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text="`Игры`", callback_data="bk9")).add(InlineKeyboardButton(text="`ТГ боты`", callback_data="bk12")).add(InlineKeyboardButton(text="`Гадалка`", callback_data="bk10")).add(InlineKeyboardButton(text="`Тамагочи`", callback_data="bk11")).add(InlineKeyboardButton(text="`Paint`", callback_data="bk13")).add(InlineKeyboardButton(text="`Вини Пух`", callback_data="bk14"))

@dp.message_handler(commands=['ГДЗ'], chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await bot.send_message(message.from_user.id, 'Выбери тему, на которую тебе нужен скрипт', reply_markup=inkb3)

@dp.callback_query_handler(text="bk9")
async def bk1_call(calback: types.CallbackQuery):
    await calback.message.answer("ГДЗ от максима!\nВыбери какой именно тебе нужен скрипт Игры", reply_markup=inkb5)
    await calback.answer()

@dp.callback_query_handler(text="bk10")
async def bk1_call(calback: types.CallbackQuery):
    await calback.message.answer("ГДЗ от максима!\nВот тебе скрипт Гадалки!")
    gadalka = open (('Gadalka') + '.zip', 'rb')
    await calback.message.reply_document(gadalka)
    await calback.answer()

@dp.callback_query_handler(text="bk11")
async def bk1_call(calback: types.CallbackQuery):
    await calback.message.answer("ГДЗ от максима!\nВот тебе скрипт Тамагочи!")
    tamagotchi = open (('tamagotchi') + '.zip', 'rb')
    await calback.message.reply_document(tamagotchi)
    await calback.answer()

@dp.callback_query_handler(text="bk12")
async def bk1_call(calback: types.CallbackQuery):
    await calback.message.answer("ГДЗ от максима!\nВыбери какой именно тебе нужен скрипт ТГ бота", reply_markup=inkb4)
    await calback.answer()

@dp.callback_query_handler(text="bk13")
async def bk1_call(calback: types.CallbackQuery):
    await calback.message.answer("ГДЗ от максима!\nВот тебе скрипт Paint!")
    paint = open (('paint') + '.zip', 'rb')
    await calback.message.reply_document(paint)
    await calback.answer()

@dp.callback_query_handler(text="bk14")
async def bk1_call(calback: types.CallbackQuery):
    await calback.message.answer("ГДЗ от максима!\nВот тебе скрипт Вини Пуха!")
    Pyh = open (('Wonny-Pyh') + '.zip', 'rb')
    await calback.message.reply_document(Pyh)
    await calback.answer()

'##################################################!!!!ГДЗ БОТЫ!!!!#########################################################'


inkb4 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text="`ТГ Чат-бот`", callback_data="bk15")).add(InlineKeyboardButton(text="`ТГ бот`", callback_data="bk16"))

@dp.message_handler(commands=['ТГ_БОТЫ'], chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    await bot.send_message(message.from_user.id, '', reply_markup=inkb4)

@dp.callback_query_handler(text="bk15")
async def bk1_call(calback: types.CallbackQuery):
    await calback.message.answer("ГДЗ от максима!\nВот тебе скрипт ТГ бота!!")
    tg1 = open (('TG Bot') + '.zip', 'rb')
    await calback.message.reply_document(tg1)
    await calback.answer()


@dp.callback_query_handler(text="bk16")
async def bk1_call(calback: types.CallbackQuery):
    await calback.message.answer("ГДЗ от максима!\nВот тебе скрипт ТГ чат-бота!")
    tg2 = open (('TG Chat-Bot') + '.zip', 'rb')
    await calback.message.reply_document(tg2)
    await calback.answer()

'##################################################!!!!ГДЗ ИГРЫ!!!!#########################################################'


inkb5 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text="`Игра 1`", callback_data="bk17")).add(InlineKeyboardButton(text="`Игра 2`", callback_data="bk18"))

@dp.message_handler(commands=['ИГРЫ'], chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    await bot.send_message(message.from_user.id, 'Выбери любой страх Макса, который хочешь узнать!', reply_markup=inkb5)

@dp.callback_query_handler(text="bk17")
async def bk1_call(calback: types.CallbackQuery):
    await calback.message.answer("ГДЗ от максима!\nВот тебе скрипт Игры1")
    Game1 = open (('Game1') + '.zip', 'rb')
    await calback.message.reply_document(Game1)
    await calback.answer()

@dp.callback_query_handler(text="bk18")
async def bk1_call(calback: types.CallbackQuery):
    await calback.message.answer("ГДЗ от максима!\nВот тебе скрипт Игры2")
    Game2 = open (('Game2') + '.zip', 'rb')
    await calback.message.reply_document(Game2)
    await calback.answer()

'##################################################!!!!ОБЩЕНИЕ!!!!#########################################################'


inkb6 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text="`Да`"+emoji.emojize(":thumbs_up:"), callback_data="bk20")).add(InlineKeyboardButton(text="`Нет`"+emoji.emojize(":thumbs_down:"), callback_data="bk21"))

@dp.message_handler(commands=['Режим_разговора'], chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    await bot.send_message(message.from_user.id, 'Го побазарим?', reply_markup=inkb6)
    await message.delete()
    await bot.send_message(message.from_user.id, '', reply_markup=inkb7)

@dp.callback_query_handler(text="bk20")
async def bk1_call(calback: types.CallbackQuery):
    await bot.delete_message(calback.message.chat.id, calback.message.message_id)
    await calback.message.answer("Вот и отлично, чё, как дела?", reply_markup=inkb7)
    await calback.answer()

@dp.callback_query_handler(text="bk21")
async def bk1_call(calback: types.CallbackQuery):
    await calback.message.answer("НЕТ!?! \nхахахха\nА я всё-равно заставлю!")
    await bot.delete_message(calback.message.chat.id, calback.message.message_id)
    await calback.message.answer("Чё, как дела?", reply_markup=inkb7)
    await calback.answer()

'##################################################!!!!ОБЩЕНИЕ №1!!!!#########################################################'

inkb7 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text="`Супер!`", callback_data="bk22")).add(InlineKeyboardButton(text="`Хорошо`", callback_data="bk23")).add(InlineKeyboardButton(text="`Плохо`", callback_data="bk24"))

@dp.message_handler(commands=['РВР1'], chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    await bot.send_message(message.from_user.id, '', reply_markup=inkb7)
    await message.delete()
    await bot.send_message(message.from_user.id, '', reply_markup=inkb8)

@dp.callback_query_handler(text="bk22")
async def bk1_call(calback: types.CallbackQuery):
    await bot.delete_message(calback.message.chat.id, calback.message.message_id)
    await calback.message.answer("Отлично, у меня тоже всё хорошо,\nВон, вчера Всеволода пранконул,\nНад игроманами поиздевался\nДень просто супер!")
    await calback.message.answer("Чем сейчас занимаешься?", reply_markup=inkb8)
    await calback.answer()

@dp.callback_query_handler(text="bk23")
async def bk1_call(calback: types.CallbackQuery):
    await bot.delete_message(calback.message.chat.id, calback.message.message_id)
    await calback.message.answer("Понятно, хорошо, оно и в африке хороше, так что хорошо что хорошо, а то не хорошо это не хорошо!")
    await calback.message.answer("Чем сейчас занимаешься?", reply_markup=inkb8)
    await calback.answer()

@dp.callback_query_handler(text="bk24")
async def bk1_call(calback: types.CallbackQuery):
    await bot.delete_message(calback.message.chat.id, calback.message.message_id)
    await calback.message.answer("Жалко, у меня тоже всё плохо\nВон вчера в классе интернет отрубил,\nна менядокладную состряпали,")
    await calback.message.answer("Чем сейчас занимаешься?", reply_markup=inkb8)
    await calback.answer()

'##################################################!!!!ОБЩЕНИЕ №2!!!!#########################################################'

inkb8 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text="`Да так...\nНи чем`", callback_data="bk30")).add(InlineKeyboardButton(text="`Играю в ПК`", callback_data="bk31")).add(InlineKeyboardButton(text="`Програмирую`", callback_data="bk32"))

@dp.message_handler(commands=['РВР2'], chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    await bot.send_message(message.from_user.id, '', reply_markup=inkb8)
    await message.delete()
    await bot.send_message(message.from_user.id, '', reply_markup=inkb9)

@dp.callback_query_handler(text="bk30")
async def bk1_call(calback: types.CallbackQuery):
    await bot.delete_message(calback.message.chat.id, calback.message.message_id)
    await calback.message.answer("Понятно всё с тобой, бздельник")
    await calback.message.answer("А в какие игры ты любишь играть??", reply_markup=inkb9)
    await calback.answer()

@dp.callback_query_handler(text="bk31")
async def bk1_call(calback: types.CallbackQuery):
    await bot.delete_message(calback.message.chat.id, calback.message.message_id)
    await calback.message.answer("Аа, круто..\nСтооп!!! Ты чё, на уроке!?!?\n Осуждаю!!!")
    await calback.message.answer("В что играешь хоть то?", reply_markup=inkb9)
    await calback.answer()

@dp.callback_query_handler(text="bk32")
async def bk1_call(calback: types.CallbackQuery):
    await bot.delete_message(calback.message.chat.id, calback.message.message_id)
    await calback.message.answer("Вооо, уважаю! Респект!")
    await calback.message.answer("Слушай, тебе бы отдохнуть,\nв игру бы какую нибудь поиграл? \nКста, в какие игры ты любишь играть??", reply_markup=inkb9)
    await calback.answer()

'##################################################!!!!ОБЩЕНИЕ №3!!!!#########################################################'

inkb9 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text="`Майнкрафт`", callback_data="bk33")).add(InlineKeyboardButton(text="`Геншин Импакт`", callback_data="bk34")).add(InlineKeyboardButton(text="`ГТА5`", callback_data="bk35")).add(InlineKeyboardButton(text="`КС`", callback_data="bk36")).add(InlineKeyboardButton(text="`БРАВЛ СТАРС`", callback_data="bk37"))

@dp.message_handler(commands=['РВР3'], chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    await bot.send_message(message.from_user.id, '', reply_markup=inkb9)
    await message.delete()
    await bot.send_message(message.from_user.id, '', reply_markup=inkb10)

@dp.callback_query_handler(text="bk33")
async def bk1_call(calback: types.CallbackQuery):
    await bot.delete_message(calback.message.chat.id, calback.message.message_id)
    await calback.message.answer("А, понятно, норм")
    await calback.message.answer("Ладно, мне пора идти...", reply_markup=inkb10)
    await calback.answer()

@dp.callback_query_handler(text="bk34")
async def bk1_call(calback: types.CallbackQuery):
    await bot.delete_message(calback.message.chat.id, calback.message.message_id)
    await calback.message.answer("Ага, ага,\nвсё понятно с тобой, \nгеншин имактер хренов, осуждаю!")
    await calback.message.answer("Ладно, мне пора идти...", reply_markup=inkb10)
    await calback.answer()

@dp.callback_query_handler(text="bk35")
async def bk1_call(calback: types.CallbackQuery):
    await bot.delete_message(calback.message.chat.id, calback.message.message_id)
    await calback.message.answer("Чёёё, круто конешно, \nно ты ещё маленький, \nтебе нельзя ещё, айяйаяй!!!")
    await calback.message.answer("Ладно, мне пора идти...",reply_markup=inkb10)
    await calback.answer()

@dp.callback_query_handler(text="bk36")
async def bk1_call(calback: types.CallbackQuery):
    await bot.delete_message(calback.message.chat.id, calback.message.message_id)
    await calback.message.answer("Вооо, уважаю, легенда!!!")
    await calback.message.answer("Ладно, мне пора идти...",reply_markup=inkb10)
    await calback.answer()

@dp.callback_query_handler(text="bk37")
async def bk1_call(calback: types.CallbackQuery):
    await bot.delete_message(calback.message.chat.id, calback.message.message_id)
    await calback.message.answer("\nХвхахвхах, \nбравлстарсер хренов, \nшколотырь мелкий!")
    await calback.message.answer("Ладно, мне пора идти...",reply_markup=inkb10)
    await calback.answer()

'##################################################!!!!ОБЩЕНИЕ №4!!!!#########################################################'

inkb10 = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text="`Пока! Удачи!`", callback_data="bk40")).add(InlineKeyboardButton(text="`ББ`", callback_data="bk41")).add(InlineKeyboardButton(text="`Поке!`", callback_data="bk42"))

@dp.message_handler(commands=['РВР4'], chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    await bot.send_message(message.from_user.id, '', reply_markup=inkb10)
    await message.delete()
    await bot.send_message(message.from_user.id, '')

@dp.callback_query_handler(text="bk40")
async def bk1_call(calback: types.CallbackQuery):
    await bot.delete_message(calback.message.chat.id, calback.message.message_id)
    await calback.message.answer("И тебе пока!")
    await calback.answer()

@dp.callback_query_handler(text="bk41")
async def bk1_call(calback: types.CallbackQuery):
    await bot.delete_message(calback.message.chat.id, calback.message.message_id)
    await calback.message.answer("ББ")
    await calback.answer()

@dp.callback_query_handler(text="bk42")
async def bk1_call(calback: types.CallbackQuery):
    await bot.delete_message(calback.message.chat.id, calback.message.message_id)
    await calback.message.answer("Поке давай!")
    await calback.answer()



'##################################################!!!!РЕАКЦИИ!!!!#########################################################'
"######################################################РЕАКЦИИ#########################################################"
'##################################################!!!!РЕАКЦИИ!!!!#########################################################'



'##################################################!!!!АУФФ!!!!#########################################################'


ayf = ["Если девушка достойная, \n  она шарит в мемах!", "Тишина - тоже музыка.\n    Когда ты глухой...", "Настоящий волк идёт по жизни \n  или за майонезом \n         Или за пивом", "Красиво по жизни идёт только тот, \n    кто умеет ходить...", "Никогда не поздно, \n  никогда не рано - \nпоменять всё поздно \n    Если это рано...", "Каждый думает\n\n Но я не думаю,\n Я - не каждый, \nЯ - не шакал", "Я буду падать,\n но когда я встану,\nупадут все!", "Запомни, лучше посрать и опоздать,\n чем прийти и обосраться...", "Запомни, в жизни есть две фразы, которые помогут открыть любую дверь\n\n ~На себя~\n и  \n\n~От себя себя~", "Запомни, каждый может кинуть камень в волка,\n Но не каждый сможет кинуть волка в камень...", "Настоящий волк...\nне укусит за бочок, \n\nнастоящий волк..\nсмоет за собой толчок..."]


@dp.message_handler(regexp='(^АУФФ)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldowns_handler(message):
        return
    await message.answer("АУФФ от Максима!")
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, random.choice(ayf))
    await asyncio.sleep(4)
    await bot.send_animation(message.chat.id,r"https://tenor.com/ru/view/ауф-auf-безумноможнобытьпервым-безумноможно-gif-18523355")


facts = ["На самом первом логотипе Apple был изображен сидящий под яблоней сэр Исаак Ньютон. Над ним нависает вот-вот готовое упасть яблоко.", "В 2009 году корпорация Google арендовала у компании California Grazing… \nкоз! \nЗачем? \nОни очень эффективны в борьбе с сорняками на разбитом вокруг штаб-квартиры «корпорации добра» газоне.", "Основатель Microsoft Билл Гейтс – недоучившийся студент, он был отчислен из Гарварда. Что, впрочем, не помешало ему создать самую популярную в мире ОС для компьютеров и одну из богатейших IT-компаний Земли.", "Слово «робот» произошло от чешского «robota» («работа»).", "Пальцы наборщика текста в среднем за день «пробегают» 20 км.", "Первый в мире будильник умел звонить только в 4 часа утра", "30 ноября каждого года отмечается Всемирный день компьютерной безопасности («Computer Security Day“)", "1 апреля 2005 года NASA поведала миру о том, что нашла воду на поверхности Марса. Троллинг удался.", "Снимок, сделанный самой первой фотокамерой в мире, пришлось бы ждать 8 часов.", "Создатели формата фото PNG хотели, чтобы его называли «пинг».", "Skype официально заблокирован в Китае.", "Компьютер Apple II получил жесткий диск объемом 5 МБ.", "Текст с экрана читается на 10% медленнее, чем с бумаги.", "По статистике, 86% людей пытаются вставить USB-кабель «вверх ногами».", "Средний возраст геймера в США – 35 лет.", "Хирурги, выросшие на видеоиграх, делают на 37% ошибок меньше.", "По данным Message Anti-Abuse Working Group, от 88 до 92% всех электронных писем, отправленных в первой половине 2010 года, являются спамом. Сегодня присутствие спама в онлайн-переписке выросло до 97%."]


@dp.message_handler(regexp='(^Факты)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldowns_handler(message):
        return
    await message.reply('IT факты от максима!')
    time.sleep(1)
    await message.reply('А вы знали чтооо...')
    time.sleep(2)
    await bot.send_message(message.chat.id, random.choice(facts))


@dp.message_handler(regexp='(Позывные Макса)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Выбери любую позывную максима", reply_markup=kb_pozovnue)


@dp.message_handler(regexp='(Стихи)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Вот стих, который написал Жека, для Максима!")
    time.sleep(1)
    await message.answer("Максим Максим, По жизни мамонт.....")


'##################################################!!!!ШУТКИ БЕЛЫЙ ЮМОР!!!!#########################################################'


@dp.message_handler(regexp='(^Белый юмор)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Выберите любой анегдот, они обозначены цифрой для удобства!", reply_markup=kb_white)



@dp.message_handler(regexp='(^Шутка--Бомба)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    await message.answer("Американец, немец и русский поспорили у кого в стране кинг-конги больше.\n\nАмериканец:\n— Наш кинг-конг такой большой, что он достает руками до крыши самого многоэтажного небоскреба в США.\n\nНемец:\n— Это ерунда,вот наш кинг-конг такой большой,что он достает руками в космосе две неизвестные планеты.\n\nРусский:\n— Ох и дураки же вы, эти две неизвестные планеты,яйца нашего кинг-конга.")



@dp.message_handler(regexp='(^Шутка--1)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Разбился самолет. Выжили американец, немец и русский. Поймал их вождь аборигенов и приказал:\n— Кто покажет мне кайф, того отпущу с миром, кто не покажет — тех съедим.\n\nАмериканец достал с борта самолета виски, кубинские сигары, позвал баб, вождь говорит:\n— Ну и в чем здесь кайф? Я это каждый день делаю!\nСъели американца. \n\nНемец достал с борта самолета ноутбук, показал вождю игры, суперскоростной интернет, прочие прибамбасы. Вождь говорит:\n— Ну и в чем здесь кайф? у нас шаманы и то быстрее, а игры каждый день…\nСъели немца. \n\nРусский достал с борта самолета ящик пива. Вождь выпил, спрашивает:\n— Ну и в чем здесь кайф?\nРусский:\n— Подожди, это не все!\nДостал еще два ящика пива. Вождь выпил.\n— Ну и в чем здесь кайф?\n— Да погоди ты! Будет тебе кайф!\nРусский принес еще два ящика водки, вождь выпил, говорит:\n— Да в чем же здесь кайф?\n— Ну погоди ты! Выпей еще эту маленькую бутылку минералки!\nВ вождя уже не влезает, но он какими-то усилиями выпивает. Встает, идет в кусты, ссыт и говорит:\n— Ух, каааайффф!!!")


@dp.message_handler(regexp='(^Шутка--2)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Проходит соревнование «кто больше выпьет». \nСоревнуются русский, немец и американец. Ведущий:\n\n— Первый американец! Он будет пить виски стопками. \nОдна… две… пять… десять… \nВсё! Сломался американский спортсмен!\n\n— Второй немец! Он будет пить пиво кружками. \nОдна… две… пять… десять… пятнадцать… \nВсё! Сломался, сломался немецкий спортсмен!\n\n— Теперь русский! Он пьёт водку ковшами. \nОдин… два… пять… десять… двадцать… тридцать… \nВсё, сломался! Сломался ковш у русского спортсмена!")


@dp.message_handler(regexp='(^Шутка--3)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Американец, немец и русский попали в ад.\n\n— Американец \n— какой здесь ужас!\n\n— Немец \n— какой здесь кошмар!\n\n— Русский \n— да, действительно хреново, но не хуже чем в нашем санатории")


@dp.message_handler(regexp='(^Шутка--4)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("— Если надо что-то сделать — зовите китайцев.\n\n— Если надо сделать что-то невозможное — зовите русских.\n\n— Если надо чтобы оно работало — зовите немцев.\n\n— А американцев?\n\n— А американцев звать не надо — они сами приходят.")


@dp.message_handler(regexp='(^Шутка--5)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Попали на необитаемый остров: немец, американец и русский. Сделали невод, поймали золотую рыбку. \nРыбка говорит:\n— Отпустите, а я каждому по три желания исполню.\n\nНемец говорит:\n— Хочу счет в банке, Мерседес и верни меня домой.\n\nАмериканец говорит:\n— Хочу большой дом, жену верную и верни меня домой.\n\nА русский говорит:\n— Хочу ящик водки, ящик закуски и верни всех моих друзей обратно!")


@dp.message_handler(regexp='(^Шутка--6)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Приходят к царю свататься к царевне русский, немец и американец. \nЦарь говорит им:\n— Вот вам по собаке и по мешку сухарей. Кто за месяц большему собаку научит, за того царевну и выдам.\n\nЧерез месяц приходят они снова к царю. \n\nВперед выходит тощий немец и жирная собака. \nЦарь его спрашивает:\n— Ну, чему собаку научил?\n\nНемец говорит:\n— Сидеть, лежать.\n\nВыходят англичанин и его собака, царь спрашивает:\n— Чему научил собаку?\n\nАмериканец говорит:\n— Сидеть, лежать, апорт, рядом.\n\nВыходит толстый русский и тощая собака. \nЦарь его спрашивает:\n— А ты чему научил?\n\nРусский поворачивается к собаке и говорит:\n— Рекс, голос!\n— Вань, дай сухарик, а?")


@dp.message_handler(regexp='(^Шутка--7)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Террористы похитили работников оборонных предприятий: \nамериканца, немца и русского.\n После часовой пытки американец объяснил устройство крылатой ракеты. \nПосле двухчасовых пыток немец выдал схему новейшего истребителя. \nПосле недельных пыток русский нарисовал гайку в трех проекциях.")


@dp.message_handler(regexp='(^Шутка--8)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Спорят американец, немец и русский, чья нация быстрее строит.\n\nАмериканец:\n— Мы начнем строить мост 1 января и 31 декабря по нему поедет первая машина.\n\nНемец:\n— А мы начнем строить больничный комплекс 1 января и 31 января уже сможем принимать первых больных.\n\nРусский:\n— Ерунда! Вот мы в понедельник в 9 утра начнем строить пивзавод и в 10 все уже пьяные.")


@dp.message_handler(regexp='(^Шутка--9)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Захватили как-то инопланетяне троих: русского, американца и немца. \nПосадили в абсолютно пустые комнаты, дали по два титановых шарика и сказали:\n— Кто из вас завтра нас больше удивит, того и отпустим.\n\nНа завтра заходят к немцу. \n\Тот поет, шариками жонглирует.\n— Ну, удивил.\n\nЗаходят к американцу — тот поет, жонглирует и степ выбивает.\n— Ну, совсем удивил. Наверно тебя выпустим. Хотя, надо к русскому зайти.\n\nВыходят от русского и говорят:\n— Все, выпускаем его.\n— Почему?\n— Он нас капитально удивил — он один шарик сломал, а другой потерял.")


'##################################################!!!!ШУТКИ ЧЁРНЫЙ ЮМОР!!!!#########################################################'


@dp.message_handler(regexp='(^Чёрный юмор)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Выберите любой анегдот, они обозначены цифрой для удобства!", reply_markup=kb_black)


@dp.message_handler(regexp='(^Шутка-Бомба)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Купил жене разводной ключ, а она не развелась!")


@dp.message_handler(regexp='(^Шутка-1)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Прикинь, мужик решил покончить с собой. \nЗавязал на шее петлю, привязал веревку к дереву на утесе, выпил пузырек с ядом, прыгнул с утеса в море, и в воздухе выстрелил себе в голову из пистолета. \n— Вот это гарантия! \n— Как бы не так! \nОн выстрелом перебил веревку, упал в воду, от испуга и холода его резко затошнило и он отрыгнул весь яд, осталась одна надежда, что удасться утонуть, но какой-то катер зацепил его за одежду и вытащил из воды. \n— Ух ты! Надеюсь, после такого он идею о самоубийстве выкинул из головы? \n— Не знаю, умер он. От простуды")


@dp.message_handler(regexp='(^Шутка-2)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Одна девочка так сильно боялась прыгать с парашютом, что прыгнула без него.")


@dp.message_handler(regexp='(^Шутка-3)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Соседский пацан вызвал меня на бой из водяных пистолетов.\nЯ просто пишу это сообщение, пока вода в кастрюле закипает.")


@dp.message_handler(regexp='(^Шутка-4)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Я копал яму в саду и вдруг откопал целый сундук с золотом. \nЯ уж было побежал домой, чтобы рассказать жене о ценной находке. \nПотом вспомнил, зачем я копал яму.")


@dp.message_handler(regexp='(^Шутка-5)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Аня вышла замуж за механика и родила шестерню!")


@dp.message_handler(regexp='(^Шутка-6)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Если вам постоянно звонят с угрозами, не отчаивайтесь. \nГлавное, что вас помнят, и вы кому-то нужны.")


@dp.message_handler(regexp='(^Шутка-7)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("— Вчера я хотел утопить все свои проблемы! \nНо жена отказалась идти купаться...")


@dp.message_handler(regexp='(^Шутка-8)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Слепой заходит в магазин, берет собаку-поводыря и начинает раскручивать ее над головой. \n— Что вы делаете?! \n— Да так, осматриваюсь")


@dp.message_handler(regexp='(^Шутка-9)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Мама, а почему ты говорила, что нельзя есть жёлтый снег? \n Потому что он солёный?")

'##################################################!!!!ШУТКИ!!!!#########################################################'


@dp.message_handler(regexp='(^Шутки)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Выберите какой жанр шуток вам интересен.", reply_markup=kb_menushutka)


'##################################################!!!!МЕНЮ ДЛЯ КЛАВИАТУР!!!!#########################################################'



@dp.message_handler(regexp='(^<Назад>)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    await message.answer("Вы вернулись к выбору!", reply_markup=kb_menushutka)


@dp.message_handler(regexp='(^`Назад`)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    await message.answer("Вы вернулись обратно, Макс2!", reply_markup=kb_max2)


@dp.message_handler(regexp='(^Отмена)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    await message.answer("Вы отменили действие", reply_markup=kb_client)


@dp.message_handler(regexp='(^Основная)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    await message.answer("Вы отменили действие", reply_markup=kb_client)


@dp.message_handler(regexp='Далее-->>', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    await message.answer("Вы поменяли клавиатуру, Макс2", reply_markup=kb_max2)


@dp.message_handler(regexp='Далее-->', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    await message.answer("Вы поменяли клавиатуру, Макс1", reply_markup=kb_max1)


@dp.message_handler(regexp='<<--Назад', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    await message.answer("Вы поменяли клавиатуру, Макс1", reply_markup=kb_max1)


@dp.message_handler(regexp='<--Назад', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    await message.answer("Вы поменяли клавиатуру, Основная", reply_markup=kb_client)


@dp.message_handler(regexp='(^Назад)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    await message.answer("Вы вернулись обратно", reply_markup=kb_max2)


@dp.message_handler(regexp='(^Макс1)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    await message.answer("Вы выбрали клавиатуру Макс1", reply_markup=kb_max1)


@dp.message_handler(regexp='(^Макс2)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    await message.answer("Вы выбрали клавиатуру Макс2", reply_markup=kb_max2)


'##################################################!!!!ПОЗЫВНЫЕ!!!!#########################################################'



@dp.message_handler(regexp='(^Антоновка)'+emoji.emojize(":hear-no-evil_monkey:"), chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    with open('SISotvetka.png', 'rb') as photo:
        await bot.send_photo(message.chat.id, photo, f'Неназывай меня так! Ещё раз, и вилкай в ж@пy!!!', reply_markup=kb_max2)


@dp.message_handler(regexp='(^Антоновка)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    with open('SISotvetka.png', 'rb') as photo:
        await bot.send_photo(message.chat.id, photo, f'Неназывай меня так! Ещё раз, и вилкай в ж@пy!!!')



@dp.message_handler(regexp='(^Желток)'+emoji.emojize(":full_moon:"), chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    with open('SISotvetka.png', 'rb') as photo:
        await bot.send_photo(message.chat.id, photo, f'Ты чё охренел? Тебе Problems надо?!?!?!', reply_markup=kb_max2)



@dp.message_handler(regexp='(^Желток)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    with open('SISotvetka.png', 'rb') as photo:
        await bot.send_photo(message.chat.id, photo, f'Ты чё охренел? Тебе Problems надо?!?!?!')



@dp.message_handler(regexp='(Пожиратель чокопаек)'+emoji.emojize(":red_envelope:"), chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Всмысле?")
    await message.answer("Подумаешь, одну коропку в день у Маргариты Киприяновы съедаю...", reply_markup=kb_max2)


@dp.message_handler(regexp='(Пожиратель чокопаек)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Всмысле?")
    await message.answer("Подумаешь, одну коропку в день у Маргариты Киприяновы съедаю...")


@dp.message_handler(regexp='(Мамонт)'+emoji.emojize(":mammoth:"), chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Мамонт не тот кто большой,\nа тот кто сильнее... ", reply_markup=kb_max2)


@dp.message_handler(regexp='(Мамонт)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer("Мамонт не тот кто большой,\nа тот кто сильнее... ")


@dp.message_handler(regexp='(^Линуксоид)'+emoji.emojize(":alien:"), chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    with open('SISotvetka.png', 'rb') as photo:
        await bot.send_photo(message.chat.id, photo, f'Я не поняла?!? Ты на Линукс?!?', reply_markup=kb_max2)


@dp.message_handler(regexp='(^Линуксоид)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    with open('SISotvetka.png', 'rb') as photo:
        await bot.send_photo(message.chat.id, photo, f'Я не поняла?!? Ты на Линукс?!?')


'##################################################!!!!ОБЗЫВНЫЕ МАКСА!!!!#########################################################'



mat = ["Сам(а) такой(ая)! Ещё раз, и костетом в глаз!", "Ты чё охренел? Тебе проблемы нужны?", "Кто обзываеться, сам так называеться!"]


@dp.message_handler(regexp='(^Максим лох|Максим даун|Максим бестолочь|Максим тварь|Максим имбицил|Максим лошара|Максим полудурок|Максим тупой|Максим мамонт|Максим дебил|Макс лох|Макс даун|Макс бестолочь|Макс тварь|Макс имбицил|Макс лошара|Макс полудурок|Макс тупой|Макс мамонт|Макс дебил)')
async def cats(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    with open('SISotvetka.png', 'rb') as photo:
        await bot.send_photo(message.chat.id, photo, random.choice(mat))


'##################################################!!!!ОКЛИКАБЕЛЬНЫЕ!!!!#########################################################'



@dp.message_handler(regexp='(^Максим|Макс)')
async def cats(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await bot.send_message(message.chat.id, f'Чо те надо, {message.from_user.first_name}')


'##################################################!!!!РЕЖИМ РАЗГОВОРА!!!!#########################################################'



@dp.message_handler(regexp='(^Режим разговора)', chat_type=['private'])
async def private_command_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    if not await cooldown_handler(message):
        return
    await message.answer(f"{message.from_user.first_name}, Го побазарим?", reply_markup=inkb6)


'##################################################!!!!РЕАКЦИИ НА ЛЮБЫЕ НЕИЗВЕСТНЫЕ КОМАНДЫ!!!!#########################################################'


@dp.message_handler(chat_type=['group', 'supergroup'])
async def group_command_handler(message: types.Message):
    await asyncio.sleep(0)
@dp.message_handler(chat_type=['private'])
async def private_command_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id not in user_states or user_states[user_id] != 'started':
        await message.answer('Сперва введите команду /start для начала работы бота!')
        return
    data = await state.get_data()
    await bot.send_message(message.chat.id, f"{data['username']}, данного сообщения я непонял, напишите /help ")

dp.register_message_handler(group_command_handler)
dp.register_message_handler(private_command_handler)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)