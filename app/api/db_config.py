'''
Psycopg is a PostgreSQL adapter for Python
several threads can share the same connection
It was designed for heavily multi-threaded applications
that create and destroy lots of cursors and make a large
number of concurrent “INSERT”s or “UPDATE”s
'''
import os

import psycopg2 as p
import psycopg2.extras
from werkzeug.security import generate_password_hash

# from app.api.v2.users.models import UserModel

DATABASE_URL = os.getenv('DATABASE_URL')
DATABASE_URL_TEST = os.getenv('DATABASE_URL_TEST')

def connection(url):
    conn = p.connect(url)
    return conn

def create_tables():
    '''A database cursor is an object that points to a
    place in the database where we want to create, read,
    update, or delete data.'''
    conn = connection(DATABASE_URL)
    cursor = conn.cursor()
    queries = tables()

    try:
        for query in queries:
            cursor.execute(query)
        conn.commit()
        print('Creating Tables.....Done')
    except Exception as e:
        print(e)
          
def destroy_tables():
    conn = connection(DATABASE_URL_TEST)
    cursor = conn.cursor()
    users = "DROP TABLE IF EXISTS users CASCADE"
    questions = "DROP TABLE IF EXISTS questions CASCADE"
    answers = "DROP TABLE IF EXISTS answers CASCADE"
    queries = [questions, users, answers]
    try:
        for query in queries:
            cursor.execute(query)
        conn.commit()
        print('Destroying test tables...Done ')
    except Exception as e:
        print(e)


def tables():
    tbl1 = """CREATE TABLE IF NOT EXISTS questions (
    question_id serial PRIMARY KEY NOT NULL,
    user_id int NOT NULL,
    title character varying(200) NOT NULL,
    question character varying(1000),
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL
    )"""

    tbl2 = """create table IF NOT EXISTS users (
     user_id serial PRIMARY KEY NOT NULL,
     user_name character(50) NOT NULL,
     first_name character(50),
     last_name character(50),
     email varchar(50) NOT NULL,
     isAdmin boolean NOT NULL,  
     registered timestamp with time zone DEFAULT ('now'::text)::date NOT NULL, 
     password varchar(500) NOT NULL
     )"""

    tbl3 = """CREATE TABLE IF NOT EXISTS answers (
    answer_id serial PRIMARY KEY NOT NULL,
    question_id int NOT NULL,
    user_id int NOT NULL,
    answer character varying(1000) NOT NULL,
    up_votes int DEFAULT 0,
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL,
    user_preferred boolean DEFAULT false
    )"""

    queries = [tbl1, tbl2,tbl3]
    return queries

def check_user(user_name):
        query = """SELECT * from users WHERE user_name='{0}'""".format(user_name)
        conn = connection(DATABASE_URL)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query)
        row = cursor.fetchone()

        if cursor.rowcount == 0:
            return None
        return row    



def super_user():
    password = generate_password_hash("hello123")

    user_admin = {
        "user_name":"mzito",
        "first_name": "jonte",
        "last_name": "mdoe",
        "email": "johndoe@example.com",
        "phone": "0707741793",
        "isAdmin": True,
        "registered": "Thu, 13 Dec 2018 21:00:00 GMT",
        "password": password
    }
  

    user_by_username = check_user(user_admin['user_name'])
    if user_by_username != None:
        print('super user already created')    
  
    query = """INSERT INTO users (user_name,first_name,last_name,email,password,isAdmin,registered) VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}');""".format(
        user_admin['user_name'], user_admin['first_name'], user_admin['last_name'], user_admin['email'], user_admin['password'], user_admin['isAdmin'], user_admin['registered'])
    conn = connection(DATABASE_URL)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
        print('super user created')
    except:
        print('failed to create super user')
