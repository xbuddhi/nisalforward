import os
import psycopg2
import re
# if is in heroku
if "DATABASE_URL" in os.environ:
    DATABASE_URL = os.environ['DATABASE_URL']
else:
    # DATABASE_URL = "postgres://hmqvfyqaymedvw:6ad95cadee89a39c9372e84dfd488a539df3c65c2bc073afbdf071747bde0b2a@ec2-54-155-110-181.eu-west-1.compute.amazonaws.com:5432/d9efgdvlm9ule8"
    DATABASE_URL = "postgres://postgres:1OdWq40K$^vO@localhost:5432/nisalforward"


# create connection
conn = psycopg2.connect(DATABASE_URL, sslmode='require')


# create table channels if not exists
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS channels (channel_id TEXT, channel_type TEXT,footer TEXT,channel_name  TEXT,PRIMARY KEY (channel_id))")
conn.commit()
cur.close()


def add_channel(channel_id, channel_type, footer, channel_name):

    cur = conn.cursor()
    # if channel already exists return false
    cur.execute("SELECT * FROM channels WHERE channel_id = %s", (channel_id,))
    if cur.fetchone() is not None:
        return False
    cur.close()
    # else add channel
    cur = conn.cursor()
    cur.execute("INSERT INTO channels (channel_id, channel_type, footer, channel_name) VALUES (%s, %s, %s, %s)",
                (channel_id, channel_type, footer, channel_name))
    conn.commit()
    cur.close()
    return True


def get_channels():
    cur = conn.cursor()
    cur.execute("SELECT * FROM channels")
    rows = cur.fetchall()
    cur.close()
    return rows


def delete_channel(channel_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM channels WHERE channel_id = %s", (channel_id,))
    conn.commit()
    cur.close()
    return True


def delete_all_channels():
    cur = conn.cursor()
    cur.execute("DELETE FROM channels")
    conn.commit()
    cur.close()


# create table for word blacklist
cur = conn.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS blacklist (word TEXT, PRIMARY KEY (word))")
conn.commit()
cur.close()


def add_word(word):
    cur = conn.cursor()
    # if word already exists return false
    cur.execute("SELECT * FROM blacklist WHERE word = %s", (word,))
    if cur.fetchone() is not None:
        return False
    cur.close()
    # else add word
    cur = conn.cursor()
    cur.execute("INSERT INTO blacklist (word) VALUES (%s)", (word,))
    conn.commit()
    cur.close()
    return True


def get_words():
    cur = conn.cursor()
    cur.execute("SELECT * FROM blacklist")
    rows = cur.fetchall()
    cur.close()
    return rows


def delete_word(word):
    cur = conn.cursor()
    cur.execute("DELETE FROM blacklist WHERE word = %s", (word,))
    conn.commit()
    cur.close()
    return True


def delete_all_words():
    cur = conn.cursor()
    cur.execute("DELETE FROM blacklist")
    conn.commit()
    cur.close()


# delete_channel("-1001446018493"")

# add word replace
cur = conn.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS replace (word TEXT, replace TEXT,PRIMARY KEY (word))")
conn.commit()
cur.close()


def add_replace(word, replace):
    cur = conn.cursor()
    # if word already exists return false
    cur.execute("SELECT * FROM replace WHERE word = %s", (word,))
    if cur.fetchone() is not None:
        cur.execute(
            "UPDATE replace SET replace = %s WHERE word = %s", (replace, word))
        conn.commit()
        cur.close()
        return True
    # else add word
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO replace (word, replace) VALUES (%s, %s)", (word, replace))
    conn.commit()
    cur.close()
    return True


def get_replace():
    cur = conn.cursor()
    cur.execute("SELECT * FROM replace")
    rows = cur.fetchall()
    cur.close()
    return rows


def delete_replace(word):
    cur = conn.cursor()
    cur.execute("DELETE FROM replace WHERE word = %s", (word,))
    conn.commit()
    cur.close()
    return True


def delete_all_replace():
    cur = conn.cursor()
    cur.execute("DELETE FROM replace")
    conn.commit()
    cur.close()


def get_replacements():
    cur = conn.cursor()
    cur.execute("SELECT * FROM replace")
    rows = cur.fetchall()
    # send as dict
    replacements = {}
    for row in rows:
        #if row[0] only a emoji 
        if len(row[0].strip()) == 1:
            replacements[row[0]] = row[1]
        else:
            replacements['(?<![A-z]|#|-|=|_)'+row[0].strip()+'(?![A-z])'] = row[1]

    cur.close()
    return replacements


# create table for server settings
cur = conn.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS settings ( server_name TEXT, value TEXT, PRIMARY KEY (server_name))")
conn.commit()


def add_setting(server_name, value):
    cur = conn.cursor()
    # if word already exists return false
    cur.execute("SELECT * FROM settings WHERE server_name = %s", (server_name,))
    if cur.fetchone() is not None:
        cur.execute(
            "UPDATE settings SET value = %s WHERE server_name = %s", (value, server_name))
        conn.commit()
        cur.close()
        return True
    # else add word
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO settings (server_name, value) VALUES (%s, %s)", (server_name, value))
    conn.commit()
    cur.close()
    return True


def get_setting(server_name):
    cur = conn.cursor()
    cur.execute("SELECT * FROM settings WHERE server_name = %s", (server_name,))
    row = cur.fetchone()
    cur.close()
    return row

# #create table for recepients
# cur = conn.cursor()
# cur.execute("CREATE TABLE IF NOT EXISTS recepients (server_name TEXT, recepient TEXT, PRIMARY KEY (server_name))")
# conn.commit()

# def add_recepient(server_name, recepient):
#     cur = conn.cursor()
#     #if word already exists return false
#     cur.execute("SELECT * FROM recepients WHERE server_name = %s", (server_name,))
#     if cur.fetchone() is not None:
#         cur.execute("UPDATE recepients SET recepient = %s WHERE server_name = %s", (recepient, server_name))
#         conn.commit()
#         cur.close()
#         return True
#     #else add word
#     cur = conn.cursor()
#     cur.execute("INSERT INTO recepients (server_name, recepient) VALUES (%s, %s)", (server_name, recepient))
#     conn.commit()
#     cur.close()
#     return True
