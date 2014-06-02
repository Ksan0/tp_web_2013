from time import gmtime, strftime
import random, string, os
import MySQLdb


words_title = ["I", "found", "many", "threads", "and", "answers", "on", "how", "to", "make", "a", "Relative", "layout",
               "respond", "to", "click", "event", "I", "have", "implemented", "my", "layout", "according", "to", "them",
               "But", "still", "OnClickListener", "is", "not", "called", "I", "have", "also", "given", "selector",
               "for", "it", "and", "it", "works", "well"]


words_nicks = ["Aaliyah", "Abigail", "Ada", "Adelina", "Agatha", "Alexa", "Alise", "Allison", "Alyssa", "Amanda", "Amber",
               "Amelia", "Angelina", "Anita", "Ann", "Ariana", "Daisy", "Danielle", "Deborah", "Delia", "Destiny",
               "Dorothy", "Geoffrey", "George", "Gerld", "Gilbert"]


def string_gen(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def time_gen():
    t = gmtime()
    result = strftime('%Y-%m-%d %H:%M:%S', t)
    return result


def email_gen(size=5, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size)) + '@mail.ru'


def title_gen():
    str = ""
    for x in range(0, random.randint(3, 5)):
        str += random.choice(words_title) + " "

    return str


def content_gen():
    str = ""
    i = 0
    for x in range(0, random.randint(10, 25)):
        str += random.choice(words_title) + " "
        ++i
        if i == 10:
            i = 0
            str += "\n"

    return str


def nick_gen():
    return random.choice(words_nicks) + "_" + string_gen(6)


def get_1_to_x_chance(x):
    ch = random.randint(1, x)
    return ch == 1 and 1 or 0


def add_user(cursor, id):
    cursor.execute('INSERT INTO auth_user VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (id, nick_gen(), "", "", email_gen(), string_gen(4), 0, 1, 0, time_gen(), time_gen()))


def add_question(cursor, id):
    author = random.randint(1, 10000)
    solved = get_1_to_x_chance(10)
    cursor.execute("INSERT INTO ask_question VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (id, title_gen(), content_gen(), author, time_gen(), solved, 0, random.randint(10, 7000)))


def add_answer(cursor, id):
    author = random.randint(1, 10000)
    question_id = random.randint(1, 100000)
    is_right = get_1_to_x_chance(20)
    cursor.execute("INSERT INTO ask_answer VALUES (%s, %s, %s, %s, %s, %s, %s)", (id, content_gen(), question_id, author, time_gen(), is_right, 0))


def add_que_like(cursor):
    user_id = random.randint(1, 10000)
    question_id = random.randint(1, 100000)
    voice = random.randint(0, 1) == 1 and 1 or -1
    cursor.execute("INSERT INTO ask_question_like(user_id, question_id, voice) VALUES (%s, %s, %s)", (user_id, question_id, voice))


def add_ans_like(cursor):
    user_id = random.randint(1, 10000)
    answer_id = random.randint(1, 1000000)
    voice = random.randint(0, 1) == 1 and 1 or -1
    cursor.execute("INSERT INTO ask_answer_like(user_id, answer_id, voice) VALUES (%s, %s, %s)", (user_id, answer_id, voice))


def add_like(cursor):
    choose = random.randint(0, 1)
    if choose == 1:
        add_que_like(cursor)
    else:
        add_ans_like(cursor)


def calculate_que_rate(cursor, que_id):
    cursor.execute("SELECT author_id FROM ask_question WHERE id=%s", (que_id, ))
    auth_id = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ask_question_like WHERE voice=1 AND question_id=%s", (que_id, ))
    likes = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM ask_question_like WHERE voice=-1 AND question_id=%s", (que_id, ))
    dislikes = cursor.fetchone()[0]
    cursor.execute("UPDATE ask_question SET rate=%s WHERE id=%s", (likes-dislikes, que_id))

    cursor.execute("SELECT rate FROM ask_userrate WHERE user_id=%s", (auth_id, ))
    try_get_rate = cursor.fetchone()
    if try_get_rate is None:
        cursor.execute("INSERT INTO ask_userrate(user_id, rate) VALUE (%s, %s)", (auth_id, likes*3-dislikes*2))
    else:
        cursor.execute("UPDATE ask_userrate SET rate=%s WHERE user_id=%s", (try_get_rate[0]+likes*3-dislikes*2, auth_id))


def calculate_ans_rate(cursor, ans_id):
    cursor.execute("SELECT author_id FROM ask_answer WHERE id=%s", (ans_id, ))
    auth_id = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ask_answer_like WHERE voice=1 AND answer_id=%s", (ans_id, ))
    likes = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM ask_answer_like WHERE voice=-1 AND answer_id=%s", (ans_id, ))
    dislikes = cursor.fetchone()[0]
    cursor.execute("UPDATE ask_answer SET rate=%s WHERE id=%s", (likes-dislikes, ans_id))

    cursor.execute("SELECT rate FROM ask_userrate WHERE user_id=%s", (auth_id, ))
    try_get_rate = cursor.fetchone()
    if try_get_rate is None:
        cursor.execute("INSERT INTO ask_userrate(user_id, rate) VALUE (%s, %s)", (auth_id, likes*5-dislikes*2))
    else:
        cursor.execute("UPDATE ask_userrate SET rate=%s WHERE user_id=%s", (try_get_rate[0]+likes*5-dislikes*2, auth_id))


def percentage(title, curr, max):
    if curr%(max/10) == 0:
        perc = int(float(curr)*100/max)
        print perc, '%'


def calculate_rate(cur):
    cur.execute("DELETE FROM ask_userrate")

    print "filling rate by ques"
    cur.execute("SELECT COUNT(*) FROM ask_question")
    end = cur.fetchone()[0]
    for x in range(1, end):
        if True:
        #try:
            calculate_que_rate(cur, x)
        #except:
            idle = 1
        percentage("ques rate: ", x, end)

    print "filling rate by answs"
    cur.execute("SELECT COUNT(*) FROM ask_answer")
    end = cur.fetchone()[0]
    for x in range(1, end):
        if True:
        #try:
            calculate_ans_rate(cur, x)
        #except:
            idle = 1
        percentage("ques rate: ", x, end)



def fill_all_users(cur):
    print "filling users"
    for x in range(1, 10000+1):
        if True:
        #try:
            add_user(cur, x)
        #except BaseException:
            --x
        percentage("users", x, 10000)


def fill_all_ques(cur):
    print "filling ques"
    for x in range(1, 100000+1):
        if True:
        #try:
            add_question(cur, x)
        #except:
            --x
        percentage("ques", x, 100000)


def fill_all_answs(cur):
    print "filling answs"
    for x in range(1, 1000000+1):
        if True:
        #try:
            add_answer(cur, x)
        #except:
            idle = 1
        percentage("answs", x, 1000000)


def fill_all_likes(cur):
    print "filling likes"
    for x in range(1, 2000000+1):
        add_like(cur)
        percentage("likes", x, 2000000)


con = MySQLdb.connect('localhost', 'ask_user', '', 'askk_db')

with con:
    os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

    from ask.models import *

    print gmtime().tm_hour, gmtime().tm_min, gmtime().tm_sec

    cur = con.cursor()
    #fill_all_users(cur)
    #fill_all_ques(cur)
    #fill_all_answs(cur)
    #fill_all_likes(cur)
    #calculate_rate(cur)

    print gmtime().tm_hour, gmtime().tm_min, gmtime().tm_sec
