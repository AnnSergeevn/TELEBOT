import random


from telebot import types, TeleBot, custom_filters
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup

from BD_engl_rus import World_rus, Add_world, World_engl, Add_trans_world

import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


print('Start telegram bot...')

state_storage = StateMemoryStorage()
token_bot = '67'
bot = TeleBot(token_bot, state_storage=state_storage)

known_users = []
userStep = {}
buttons = []

DSN = "postgresql://postgres:post@localhost:5432/netology_bd"
engine = sqlalchemy.create_engine(DSN)
# сессия
Session = sessionmaker(bind=engine)
session = Session()

n = []

sales_other = Session().query(World_engl).join(World_rus)
sales= Session().query(Add_trans_world).join(Add_world)

for sale in sales_other:
    n.append(sale.target_word)

    '''print(
        f'{sale.world_rus.id} | {sale.world_rus.translate} | {sale.others_world}'
    )'''
#print(n)
for sale in sales:
    n.append(sale.target_add_word)

    '''print(
        f'{sale.world_rus.id} | {sale.world_rus.translate} | {sale.others_world}'
    )'''
print(n)
list_table = []

#sales = Session().query(World_engl).select_from(World_rus)
for sale in sales_other:
    '''print(
        f'{sale.id} | {sale.target_word} | {sale.world_rus.translate}'
    )'''
    list_other = random.sample(n, 4)
    list_table.append(sale.id)
    list_table.append(sale.world_rus.translate)
    list_table.append(sale.target_word)


    '''print(
        f'{sale.id} | {sale.world_rus.translate} | {sale.target_word} | {list_other}'
    )'''
    for i in range(0, 4):
        while list_other[i] == sale.target_word:
            list_other = random.sample(n, 4)
    list_table.append(list_other)

chunk_size = 4
list_data = [list_table[i:i + chunk_size] for i in range(0, len(list_table), chunk_size)]

b= sale.id

for sale in sales:
    list_other = random.sample(n, 4)
    list_table.append(b+sale.id)
    list_table.append(sale.add_world.add_world)
    list_table.append(sale.target_add_word)

    for i in range(0, 4):
        while list_other[i] == sale.target_add_word:
            list_other = random.sample(n, 4)
    list_table.append(list_other)


#print(list_table)


list_data = [list_table[i:i + chunk_size] for i in range(0, len(list_table), chunk_size)]

print(list_data)

b= len(list_data)-1
print(b)

def show_hint(*lines):
    return '\n'.join(lines)


def show_target(data):
    return f"{data['target_word']} -> {data['translate_word']}"


class Command:
    ADD_WORD = 'Добавить слово ➕'
    DELETE_WORD = 'Удалить слово🔙'
    NEXT = 'Дальше ⏭'


class MyStates(StatesGroup):
    target_word = State()
    translate_word = State()
    another_words = State()


def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        known_users.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0


#k=0
@bot.message_handler(commands=['cards', 'start'])
def create_cards(message):

    cid = message.chat.id
    if cid not in known_users:
        known_users.append(cid)
        userStep[cid] = 0
        bot.send_message(cid, '''Привет 👋 Давай попрактикуемся в английском языке. Тренировки можешь проходить в удобном для себя темпе.

У тебя есть возможность использовать тренажёр, как конструктор, и собирать свою собственную базу для обучения. Для этого воспрользуйся инструментами:

добавить слово ➕,
удалить слово 🔙.
Ну что, начнём ⬇️''')
    markup = types.ReplyKeyboardMarkup(row_width=2)

    global buttons

    buttons = []
    k = random.randint(0, b)
    target_word = list_data[k][2]  # брать из БД
    translate = list_data[k][1]  # брать из БД ['Зеленый', 'Белый', 'Привет', 'Машина', 'Мяч', 'Стол', 'Собака', 'Снег', 'Старый', 'Разговор']
    target_word_btn = types.KeyboardButton(target_word)
    buttons.append(target_word_btn)
    others = list_data[k][3]  # брать из БД
    print(k)
    other_words_btns = [types.KeyboardButton(word) for word in others]
    buttons.extend(other_words_btns)
    random.shuffle(buttons)
    next_btn = types.KeyboardButton(Command.NEXT)
    add_word_btn = types.KeyboardButton(Command.ADD_WORD)
    delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
    buttons.extend([next_btn, add_word_btn, delete_word_btn])

    markup.add(*buttons)

    greeting = f"Выбери перевод слова:\n🇷🇺 {translate}"
    bot.send_message(message.chat.id, greeting, reply_markup=markup)
    bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['target_word'] = target_word
        data['translate_word'] = translate
        data['other_words'] = others
    print(data['target_word'])
    print(data['translate_word'])
    '''session.commit()  # фиксируем изменения

    session.close()'''


@bot.message_handler(func=lambda message: message.text == Command.NEXT)
def next_cards(message):
    create_cards(message)


@bot.message_handler(func=lambda message: message.text == Command.DELETE_WORD)
def delete_word(message):

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        hint = show_target(data)
        hint_text = ["Удаляем пару слов", hint]
        hint = show_hint(*hint_text)

        print(f"Удаляемое слово {data['translate_word']}")
        for sale in sales_other:
            if data['translate_word'] == sale.world_rus.translate:
                print(sale.world_rus.translate)
                id_world = sale.id
                session.query(World_engl).filter(World_engl.id_world_rus == id_world).delete()
                session.commit()
                session.query(World_rus).filter(World_rus.id == id_world).delete()
                session.commit()

        for sale in sales:
            if data['translate_word'] == sale.add_world.add_world:
                print(sale.add_world.add_world)
                add_world = sale.add_world.add_world
                #print(id_add_world)


                session.query(Add_trans_world).filter(Add_trans_world.target_add_word == sale.target_add_word).delete()
                session.commit()
                session.query(Add_world).filter(Add_world.add_world == add_world).delete()
                session.commit()

    bot.send_message(message.chat.id, hint)


@bot.message_handler(func=lambda message: message.text == Command.ADD_WORD, content_types=['text'])
def add_word(message):
    cid = message.chat.id
    userStep[cid] = 1
    print(message.text)  # сохранить в БД
    answer1 = bot.send_message(message.chat.id, "Введите слово для добавления в БД")
    bot.register_next_step_handler(answer1, point1)


id_world_add = 0
def point1(message):
    cid = message.chat.id
    text = message.text
    print("Слово", text)
    translate_world1 = Add_world(add_world=text)
    session.add(translate_world1)
    session.commit()  # фиксируем изменения'''
    add_word_translate(message)
    print(translate_world1.id)
    global id_world_add
    id_world_add = translate_world1.id


def add_word_translate(message):
    cid = message.chat.id
    userStep[cid] = 1
    print(message.text)  # сохранить в БД
    answer2 = bot.send_message(message.chat.id, "Введите перевод слова для добавления в БД")
    bot.register_next_step_handler(answer2, point2)


def point2(message):
    cid = message.chat.id
    text = message.text
    print("Перевод", text)
    engl_translate_world1 = Add_trans_world(target_add_word=text, id_add_world = id_world_add)
    session.add(engl_translate_world1)
    session.commit()  # фиксируем изменения

    bot.send_message(message.chat.id,"Добавлено")
    create_cards(message)
    return


@bot.message_handler(func=lambda message: True, content_types=['text'])
def message_reply(message):
    text = message.text
    markup = types.ReplyKeyboardMarkup(row_width=2)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        target_word = data['target_word']
        if text == target_word:
            hint = show_target(data)
            hint_text = ["Отлично!❤", hint]
            next_btn = types.KeyboardButton(Command.NEXT)
            add_word_btn = types.KeyboardButton(Command.ADD_WORD)
            delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
            buttons.extend([next_btn, add_word_btn, delete_word_btn])
            hint = show_hint(*hint_text)

        else:
            for btn in buttons:
                if btn.text == text:
                    btn.text = text + '❌'
                    break
            hint = show_hint("Допущена ошибка!",
                             f"Попробуй ещё раз вспомнить слово 🇷🇺{data['translate_word']}")
    markup.add(*buttons)
    bot.send_message(message.chat.id, hint, reply_markup=markup)



'''DSN = "postgresql://postgres:post@localhost:5432/netology_bd"
engine = sqlalchemy.create_engine(DSN)

# сессия
Session = sessionmaker(bind=engine)
session = Session()


n=[]
id_trans = []

sales_other = Session().query(List).join(World_rus).filter(World_rus.id==1)

for sale in sales_other:
    n.append(sale.others_world)

    print(
        f'{sale.world_rus.id} | {sale.world_rus.translate} | {sale.others_world}'
        )
print(n)
list_table = []

sales = Session().query(World_engl).select_from(List).join(World_rus)
for sale in sales:
    print(
        f'{sale.id} | {sale.target_word} | {sale.world_rus.translate}'
    )
    list_table.append(sale.id)
    list_table.append(sale.world_rus.translate)
    list_table.append(sale.target_word)
    list_table.append(n)



print(list_table)

chunk_size = 4
list_data = [list_table[i:i + chunk_size] for i in range(0, len(list_table), chunk_size)]
print(len(list_data))
create_cards(translate = list_data[0][1], target_word= list_data[0][2],others =list_data[0][3])
session.commit()  # фиксируем изменения

session.close()'''
session.commit()  # фиксируем изменения

session.close()
bot.add_custom_filter(custom_filters.StateFilter(bot))

bot.infinity_polling(skip_pending=True)