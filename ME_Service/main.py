from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from query import Data
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton
import time


class Add(StatesGroup):
    name = State()
    phone = State()
    address = State()
    mail = State()


class Usluga(StatesGroup):
    state_ = State()


class Order(StatesGroup):
    type = State()
    service = State()
    dop_info = State()
    go = State()


class EditName(StatesGroup):
    new_name = State()


class EditPhone(StatesGroup):
    new_phone = State()


class EditAddress(StatesGroup):
    new_address = State()


class EditInfo(StatesGroup):
    new_info = State()


class EditMail(StatesGroup):
    new_mail = State()


def get_product_keyboard(spi):
    markup = ReplyKeyboardMarkup()
    for val in spi:
        markup.add(KeyboardButton(val[2]))
    return markup


def get_keyboard(spi):
    markup = ReplyKeyboardMarkup()
    for val in spi:
        markup.add(KeyboardButton(val[0]))
    return markup


TOKEN = "сюда вставить токен"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
group_id = "Сюда вставить груп айди"


@dp.message_handler(state=EditName.new_name)
async def new_name(message: types.Message, state: FSMContext):
    Data("db.db").update_name(str(message.from_user.id), str(message.text))
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Вернуться в главное меню")
    await state.finish()
    await bot.send_message(message.from_user.id, "Имя изменено", reply_markup=markup)


@dp.message_handler(state=EditAddress.new_address)
async def new_address(message: types.Message, state: FSMContext):
    Data("db.db").update_address(str(message.from_user.id), str(message.text))
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Вернуться в главное меню")
    await state.finish()
    await bot.send_message(message.from_user.id, "Адрес изменен", reply_markup=markup)


@dp.message_handler(state=EditMail.new_mail)
async def new_name(message: types.Message, state: FSMContext):
    Data("db.db").update_mail(str(message.from_user.id), str(message.text))
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Вернуться в главное меню")
    await state.finish()
    await bot.send_message(message.from_user.id, "Mail изменен", reply_markup=markup)


@dp.message_handler(state=EditPhone.new_phone)
async def new_phone(message: types.Message, state: FSMContext):
    Data("db.db").update_phone(str(message.from_user.id), str(message.text))
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Вернуться в главное меню")
    await state.finish()
    await bot.send_message(message.from_user.id, "Номер телефона изменен", reply_markup=markup)


@dp.message_handler(commands=['en'])  # edit name
async def edit_name(message: types.Message):
    await bot.send_message(message.from_user.id, "Введите новое имя")
    await EditName.new_name.set()


@dp.message_handler(commands=['ep'])  # edit phone
async def edit_phone(message: types.Message):
    await bot.send_message(message.from_user.id, "Введите новый номер телефона")
    await EditPhone.new_phone.set()


@dp.message_handler(commands=['ea'])  # edit address
async def edit_address(message: types.Message):
    await bot.send_message(message.from_user.id, "Введите новый адрес")
    await EditAddress.new_address.set()


@dp.message_handler(commands=['em'])  # edit mail
async def edit_mail(message: types.Message):
    await bot.send_message(message.from_user.id, "Введите новый mail")
    await EditMail.new_mail.set()


@dp.message_handler(state=Order.type)
async def add_product_category(message: types.Message, state: FSMContext):
    id_type = Data("db.db").get_type_by_name(str(message.text))
    if len(id_type):
        id_type = id_type[0][0]
        async with state.proxy() as data:
            data["type"] = [id_type, str(message.text)]
        await Order.next()
        await bot.send_message(message.from_user.id, "Укажите какую услугу вы хотите получить",
                               reply_markup=get_product_keyboard(Data("db.db").get_products_by_type_id(id_type)).add(
                                   "Вернуться в главное меню"))
    else:
        markup = get_keyboard(Data("db.db").get_type())
        await bot.send_message(message.from_user.id, "Мы пока Вас не понимаем, выберите вариант из списка",
                               reply_markup=markup)


@dp.message_handler(state=Order.service)
async def add_product_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        info = Data("db.db").get_products_by_name_and_type(data["type"][0], str(message.text))
        if len(info):
            data["service"] = str(message.text)
            data["ed"] = info[0][-2]
            data["price"] = info[0][-1]
            await Order.next()
            await bot.send_message(message.from_user.id,
                                   "Если у вас есть какая-то дополнительная информация, которую нам нужно знать, "
                                   "пожалуйста напишите её здесь",
                                   reply_markup=ReplyKeyboardRemove())
        elif str(message.text) == "Вернуться в главное меню":
            await state.finish()
            await Order.type.set()
            markup = get_keyboard(Data("db.db").get_type())
            await bot.send_message(message.from_user.id,
                                   f"Здравствуйте, {message.from_user.first_name}, "
                                   f"пожалуйста, выберите что вас интересует ",
                                   reply_markup=markup)
        else:
            await bot.send_message(message.from_user.id, "Мы пока Вас не понимаем, выберите вариант из списка",
                                   reply_markup=get_product_keyboard(
                                       Data("db.db").get_products_by_type_id(data["type"][0])))


@dp.message_handler(state=Order.dop_info)
async def add_product_category(message: types.Message, state: FSMContext):
    if str(message.text) == "Вернуться в главное меню":
        await state.finish()
        await Order.type.set()
        markup = get_keyboard(Data("db.db").get_type())
        await bot.send_message(message.from_user.id,
                               f"Здравствуйте, {message.from_user.first_name}, пожалуйста, выберите что вас интересует",
                               reply_markup=markup)
    else:
        mes = ""
        async with state.proxy() as data:
            mes += "Тип услуги: " + data["type"][1] + "\n"
            mes += "Услуга: " + data["service"] + "\n"
            mes += "Единица измерения: " + data["ed"] + "\n"
            mes += "Цена: " + str(data["price"]) + "\n"
            mes += "Доп информация: " + str(message.text) + "\n"
            info_user = Data("db.db").is_subscribe(str(message.from_user.id))
            mes += "Имя клиента: " + info_user[0][1] + "\n"
            mes += "Номер телефона: " + info_user[0][2] + "\n"
            mes += "Адрес: " + info_user[0][3] + "\n"
            mes += "Email: " + info_user[0][-1]
            data["go"] = mes
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Отправить заявку")
        markup.add("Отменить заказ")
        await Order.next()
        await bot.send_message(message.from_user.id, mes, reply_markup=markup)


@dp.message_handler(state=Order.go)
async def add_product_category(message: types.Message, state: FSMContext):
    mes = str(message.text)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Отправить заявку")
    markup.add("Отменить заказ")
    if mes != "Отправить заявку" and mes != "Отменить заказ":
        await bot.send_message(message.from_user.id, "Мы пока Вас не понимаем, выберите вариант из списка",
                               reply_markup=markup)
    else:
        if mes == "Отправить заявку":
            await bot.send_message(message.from_user.id, "Ваш заказ отправлен на обработку, скоро с вами свяжутся",
                                   reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                                       "Вернуться в главное меню"))
            async with state.proxy() as data:
                await bot.send_message(group_id, data["go"])

        else:
            await bot.send_message(message.from_user.id, "Ваша заявка отменена",
                                   reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                                       "Вернуться в главное меню"))
        await state.finish()


@dp.message_handler(state=Add.name)
async def add_product_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = str(message.text)
    await Add.next()
    await bot.send_message(message.from_user.id, "Теперь введите Ваш номер телефона")


@dp.message_handler(state=Add.phone)
async def add_product_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["phone"] = str(message.text)
    await Add.next()
    await bot.send_message(message.from_user.id, "Введите адрес дома, где будут выполняться работы")


@dp.message_handler(state=Add.address)
async def add_product_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["address"] = str(message.text)
    await Add.next()
    await bot.send_message(message.from_user.id, "Введите, пожалуйста, ваш email")


@dp.message_handler(state=Usluga.state_)
async def state_usluga(message: types.Message, state: FSMContext):
    if str(message.text) == "Изменить данные":
        mes = "Введите или нажмите на одну из следующих команд, чтобы изменить свои данные:\n" \
              "/ep - отредактировать номер телефона\n" \
              "/em - отредактировать email\n" \
              "/ea - отредактировать адрес\n" \
              "/en - отредактировать имя\n" \
              "/start - Вернуться в главное меню"
        await bot.send_message(message.from_user.id, mes, reply_markup=ReplyKeyboardRemove())
        await state.finish()
    elif str(message.text) == "Сделать заказ":
        markup = get_keyboard(Data("db.db").get_type())
        await bot.send_message(message.from_user.id, "Выберите категорию", reply_markup=markup)
        await Order.type.set()
    else:
        await bot.send_message(message.from_user.id, "Мы пока Вас не понимаем, выберите вариант из списка")


@dp.message_handler(state=Add.mail)
async def add_product_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        Data("db.db").add_user(str(message.from_user.id), data["name"], data["phone"], data["address"],
                               str(message.text))
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Изменить данные")
    markup.add("Сделать заказ")
    await state.finish()
    await Usluga.state_.set()
    await bot.send_message(message.from_user.id,
                           "Вы успешно добавлены в систему.Теперь вы можете заказать услугу", reply_markup=markup)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    if len(Data("db.db").is_subscribe(str(user_id))):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Изменить данные")
        markup.add("Сделать заказ")
        await Usluga.state_.set()
        await bot.send_message(user_id,
                               f"Здравствуйте, {message.from_user.first_name}, пожалуйста, выберите что вас интересует",
                               reply_markup=markup)
    else:
        await Add.name.set()
        await bot.send_message(user_id,
                               f"Здравствуйте, для использования бота Вам необходимо указать контактные данные. В "
                               f"будущем это позволит нам идентифицировать Вас. Для начала введите, пожалуйста, "
                               f"Ваше имя")


@dp.message_handler()
async def izi_message(message: types.Message):
    if str(message.text) == "Вернуться в главное меню":
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Изменить данные")
        markup.add("Сделать заказ")
        await Usluga.state_.set()
        await bot.send_message(message.from_user.id,
                               f"Здравствуйте, {message.from_user.first_name}, пожалуйста, выберите что вас интересует",
                               reply_markup=markup)


if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        time.sleep(3)
        print(e)
