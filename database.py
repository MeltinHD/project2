import mysql.connector
from datetime import datetime

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            port=3306,
            database='testdatabase'
        )
        self.cursor = self.connection.cursor()

        # Create users table if not exists
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY UNIQUE,
                email VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                firstname VARCHAR(255) NOT NULL,
                lastname VARCHAR(255) NOT NULL,
                phonenumber VARCHAR(10) NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                id INT AUTO_INCREMENT PRIMARY KEY UNIQUE,
                email VARCHAR(50) NOT NULL UNIQUE,
                numOfGuests VARCHAR(50) NOT NULL,
                date VARCHAR(255) NOT NULL,
                time VARCHAR(255) NOT NULL
            )
        ''')
        self.connection.commit()

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params)
        self.connection.commit()
        return self.cursor

    # User Table
    def fetch_allUsers(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def fetch_one(self, email):
        self.cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        return self.cursor.fetchone()

    def create_user(self, email, password, firstname, lastname, phonenumber):
        query = 'INSERT INTO users (email, password, firstname, lastname, phonenumber) VALUES (%s, %s, %s, %s, %s)'
        self.execute_query(query, (email, password, firstname, lastname, phonenumber))
    
    def update_user(self, email, password, firstname, lastname, phonenumber):
        query = 'UPDATE users SET password = %s, firstname = %s, lastname = %s WHERE email = %s'
        self.execute_query(query, (password, firstname, lastname, phonenumber))
        
    def delete_user(self, user_name):
        query = 'DELETE FROM users WHERE username = %s'
        self.execute_query(query, (user_name,))

    # Reservations Table
    def fetch_allReservations(self):
        self.cursor.execute('SELECT * FROM reservations')
        return self.cursor.fetchall()
    
    def fetch_oneEmail(self, email):
        self.cursor.execute('SELECT * FROM reservations WHERE email = %s', (email,))
        return self.cursor.fetchone()
    
    def create_reservation(self, email, numOfGuests, date, time):
        query = 'INSERT INTO reservations (email, numOfGuests, date, time) VALUES (%s, %s, %s, %s)'
        self.execute_query(query, (email, numOfGuests, date, time))

    def update_reservation(self, numOfGuests, date, time, email):
        query = 'UPDATE reservations SET numOfGuests = %s, date = %s, time = %s WHERE email = %s'
        self.execute_query(query, (numOfGuests, date, time, email))

    def delete_reservation(self):
        query = 'DELETE FROM reservations'
        self.execute_query(query)    