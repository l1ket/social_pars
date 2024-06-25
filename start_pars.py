import sqlite3
import asyncio
import datetime

from sheets import get_ids_2


async def start():
    week = datetime.datetime.today().strftime('%d.%m.%Y')
    ret_week = table_create(week=week)
    if ret_week == None:
        new_week = datetime.date.today()
        new_week = new_week - datetime.timedelta(days=7)
        total_week = f'за {new_week.strftime("%d.%m.%Y")} - {week}'
        inst, yt, tt = await get_ids_2(week_stat=total_week, week_tg=week)
        return inst, yt, tt
    else:
        new_week = datetime.datetime.strptime(ret_week, '%d.%m.%Y')
        new_week = new_week + datetime.timedelta(days=7)
        total_week = f'за {ret_week} - {new_week.strftime("%d.%m.%Y")}'
        inst, yt, tt = await get_ids_2(week_stat=total_week, week_tg=new_week.strftime("%d.%m.%Y"))
        change_week(new_date=new_week.strftime("%d.%m.%Y"))
        return inst, yt, tt


def table_create(week):
    connection = sqlite3.connect('dates.db')
    cursor = connection.cursor()
        
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dates (
    id INTEGER PRIMARY KEY,
    date_week TEXT
    )
    ''')
    connection.commit()

    cursor.execute('SELECT date_week FROM dates')
    results = cursor.fetchall()
    if results == []:
        cursor.execute('INSERT INTO dates (date_week) VALUES (?)', (week,))
        connection.commit()
        connection.close()
        return None
    else:
        connection.close()
        return results[0][0]


def table_users_create():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
        
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    us_id INTEGER
    )
    ''')
    connection.commit()
    connection.close()


def add_user(us_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
        
    cursor.execute('INSERT INTO users (us_id) VALUES (?)', (us_id,))
    connection.commit()
    connection.close()


def select_user(us_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute('SELECT us_id FROM users WHERE us_id =?',(us_id,))
    results = cursor.fetchall()
    
    connection.commit()
    connection.close()
    return results


def select_all_user():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute('SELECT us_id FROM users')
    results = cursor.fetchall()
    
    connection.commit()
    connection.close()
    return results


def change_week(new_date):
    connection = sqlite3.connect('dates.db')
    cursor = connection.cursor()

    cursor.execute('UPDATE dates SET date_week = ?', (new_date,))

    connection.commit()
    connection.close()

if __name__ == '__main__':
    # asyncio.run(start())
    print(table_users_create())
    res = select_user(12)    
    print(res)