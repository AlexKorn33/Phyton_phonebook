import sqlite3 as sl
from easygui import *

conn = sl.connect('Phone_book_demo_1.db')  # подключение к БД
cur = conn.cursor()

# SQL запрос
cur.execute("""
            CREATE TABLE IF NOT EXISTS contact_list
            (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            tel_nunb_1 TEXT,
            tel_numb_2 TEXT,
            email TEXT
            );
            """)


# # Добавление контакта
def add_contact():
    first_name = enterbox("Введите имя контакта:")
    last_name = enterbox("Введите фамилию контакта:")
    tel_nunb_1 = enterbox("Введите основной номер телефона:")
    tel_numb_2 = enterbox("Введите дополнительный номер телефона:")
    email = enterbox("Введите адрес электронной почты:")
    cur.execute("INSERT INTO contact_list(first_name,last_name,tel_nunb_1,tel_numb_2,email) VALUES(?,?,?,?,?)", (first_name,last_name,tel_nunb_1,tel_numb_2,email))
    conn.commit()
    msgbox("Контакт успешно добавлен!")

# # Вывести весь список контактов
def select_all():
    cur.execute("SELECT * FROM contact_list;")
    output=''
    for row in cur.fetchall():
        output+=str(row)
    msgbox(output, 'Существующие контакты')

# # Поиск контакта

def search_contact():
    key = enterbox("Введите параметр поиска")
    cur.execute('SELECT * FROM contact_list WHERE first_name LIKE ? OR last_name LIKE ? OR tel_nunb_1 LIKE ? OR tel_numb_2 LIKE ? OR email LIKE ?', ('%' + key + '%', '%' + key + '%', '%' + key + '%', '%' + key + '%', '%' + key + '%'))
    output=''
    for row in cur.fetchall():
        output+=str(row)
    msgbox(output, 'Найдены контакты')
    
    conn.commit()

# # Удаление контакта по телефонному номеру или email

def del_contact():
    key = enterbox("Введите телефонный номер или email для удаления контакта")
    cur.execute('DELETE FROM contact_list WHERE first_name LIKE ? OR last_name LIKE ? OR tel_nunb_1 LIKE ? OR tel_numb_2 LIKE ? OR email LIKE ?', ('%' + key + '%', '%' + key + '%', '%' + key + '%', '%' + key + '%', '%' + key + '%'))
    conn.commit()
    msgbox('Контакт удалён!')
    
# Удалить весь справочник

def del_all():
    var = ccbox("Вы действительно хотите удолить весь справочнтк ?")
    if var == 1:
        cur.execute('DELETE FROM contact_list')
        msgbox('Справочник удалён!')
    elif var== 0:
        msgbox('Справочник остался без изменений')

    conn.commit()

def main():
    while True:
        choice = choicebox("Выберите действие", "Телефонный справочник", ['Просмотр контактов', 'Добавить контакт', 'Поиск контакта','Удалить контакт','Удалить всё'])
        if choice == "Просмотр контактов":
            select_all()
        elif choice == "Добавить контакт":
            add_contact()
        elif choice == "Поиск контакта":
            search_contact()   
        elif choice == "Удалить контакт":
            del_contact()
        elif choice == "Удалить всё":
            del_all()
        else:
            break
    conn.close()

if __name__=='__main__':
    main()
