import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
DB_PATH = "sqlite:///sochi_athletes.sqlite3"

from datetime import datetime, date, time

# базовый класс моделей таблиц
Base = declarative_base()

class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'
    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    # пол атлета
    gender = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    # дата рождения
    birthdate = sa.Column(sa.Text)
    # рост
    height = sa.Column(sa.REAL)

class Athelete(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей ("id" integer primary key autoincrement, "age" integer,"birthdate" text,"gender" text,"height" real,"name" text,"weight" integer,"gold_medals" integer,"silver_medals" integer,"bronze_medals" integer,"total_medals" integer,"sport" text,"country" text)
    """
    # задаем название таблицы
    __tablename__ = 'athelete'
    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    # возраст атлета
    age = sa.Column(sa.Integer)
    # дата рождения
    birthdate = sa.Column(sa.Text)
    # пол атлета
    gender = sa.Column(sa.Text)
    # рост
    height = sa.Column(sa.REAL)
    # вес
    # имя пользователя
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    # кол-во медалей
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    # вид спорта
    sport = sa.Column(sa.Text)
    # страна
    country = sa.Column(sa.Text)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()

def is_date(date):
    '''
    # Функция принимает на вход строку с датой
    # Возвращает True, еслли дата корректна, False если не корректна
    # Для примера возьмём дату "1995-04-30"
    '''
    # Разбиваем дату разделителем "-", фукнция split возвращает список
    # Если дата корректна, список будет вида ["YYYY","MM","DD"]
    date_splitted = date.split("-")
    # Для начала, длина списка должна быть равной 3
    if len(date_splitted) == 3:
        # Теперь запишем в переменные year, month, day элементы списка date_splitted
        year, month, day = date_splitted
        # Теперь просто проверим, что строка с годом имеет длину 4, строки с месяцем и днём длину 2
        if len(year) == 4 and len(month) == 2 and len(day)==2 and int(month) < 13 and int(month) > 0 and int(day) > 0 and int(day) < 32:
            # Дата нам подходит
            return True
        else:
            # Иначе дата нам не подходит
            return False
    else:
        # Иначе дата не подходит
        return False

def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # выводим приветствие
    print("Привет! Введите данные:")
    # запрашиваем у пользователя данные
    first_name = input("Введи имя: ")
    last_name = input("Введи фамилию: ")
    gender = input("Введите пол: ")
    email = input("Введите адрес электронной почты: ")
    # дата рождения
    while True:
        birthdate = input("Введите дату рождения в формате YYYY-MM-DD: ")
        if is_date(birthdate) == True:
            break
        else:
            print("Неверный формат даты")
    # рост
    height = input("Введите рост в формате М.СС: ")
    # создаем нового пользователя
    user = User(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    # возвращаем созданного пользователя
    return user

def find_user(user_id):
    # Создадим сессию
    session = connect_db()
    # Сделаем запрос
    user = session.query(User).filter(User.id == user_id).first()
    # Закроем сессию
    session.close()
    # Возращаем пользователя
    return user
   
def find_by_height(user_height):
# Функция, которая принимает как аргумент рост юзера
# Возвращает атлета с минимальной разницей в росте с юзером
    # Создадим сессию
    session = connect_db()
    # отфильтруем атлетов с ростом
    atheletes = session.query(Athelete).filter(Athelete.height > 0).all()
    # Закроем сессию
    session.close()
    # Переменная candidate - это атлет-кандидатю. У кандидата минимальная разница в росте с юзером
    # Пусть сначала кандидатом будет первый атлет
    candidate = atheletes[0]
    
    # В цикле пройдем по атлетам
    for athelete in atheletes:
        # Посчитаем разницу роста кандидата и юзера
        candidate_diff = abs(candidate.height - user_height)
        # Теперь посчитаем разницу роста для текущего атлета и юзера
        athelete_diff = abs(athelete.height - user_height)
        
        # Если у текущего атлета разница в росте меньше чем у кандидата
        if athelete_diff < candidate_diff:
            # То теперь этот атлет и есть новый кандидат
            candidate = athelete
    
    # Теперь когда мы просмотрели всех атлетов
    # У кандидата минимальная разница в росте с юзером
    # Поэтому вернем его
    return candidate

# Функция, которая возвращает разность дат
def date_diff(date_1, date_2):
    # Преобразуем строку date_1 в объект datetime
    datetime_1 = datetime.strptime(date_1, "%Y-%m-%d")
    # Аналогично для второй даты
    datetime_2 = datetime.strptime(date_2, "%Y-%m-%d")
    # Считаем модуль разности дат
    diff = abs(datetime_1-datetime_2)
    # Возращаем разность
    return diff

def find_by_date(user_birthdate):
# Поиск по дате рождения
    session = connect_db()
    atheletes1 = session.query(Athelete).all()
    session.close()
    candidate1 = atheletes1[0]

    # В цикле пройдем по атлетам
    for athelete1 in atheletes1:
        diff_age = date_diff(candidate1.birthdate, user_birthdate)
        diff_age_a = date_diff(athelete1.birthdate, user_birthdate)
        if diff_age > diff_age_a:
            candidate1 = athelete1
    return candidate1

def main():
    session = connect_db()
    mode = input("Выбери режим.\n1 - ввести нового пользователя\n2 - поиск в базе атлетов по номеру пользователя\n")
    if mode == "2":
        # выбран режим поиска, запускаем его
        user_id = int(input("Введите ID пользователя: "))
        # Находим юзера по ID
        user = find_user(user_id)
        if user_id:
            # Вызовем фукнцию, чтобы найти атлета с минимальной разницей по росту
            athelete_close_height = find_by_height(user.height)
            # Вызовем функцию поиска атлета по дате рождения
            athelete_close_birthdate = find_by_date(user.birthdate)
            # Выведем результат
            print(f'Найден пользователь {user.id}: {user.first_name} {user.last_name}. Рост - {user.height}, дата рождения - {user.birthdate}.')
            print("Ближайший по росту атлет: {} {}".format(athelete_close_height.name, athelete_close_height.height))
            print("Ближайший по дате рождения атлет: {} {}".format(athelete_close_birthdate.name, athelete_close_birthdate.birthdate))
        else:
            print("Пользователь с таким ID не найден")
    elif mode == "1":
        # запрашиваем данные пользоватлея
        user = request_data()
        # добавляем нового пользователя в сессию
        session.add(user)
        # сохраняем все изменения, накопленные в сессии
        session.commit()
        print("Спасибо, данные сохранены!")
    else:
        print("Некорректный режим:(")

if __name__ == "__main__":
    main()
