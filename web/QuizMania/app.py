import qrcode, socket
from flask import Flask, render_template_string, request, session, redirect, url_for, render_template, jsonify
from flask_session import Session
import time
import mysql.connector
import random

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = '123456789'

quizManiaDB = mysql.connector.connect(
    host = "192.168.2.2",
    user = "esteban",
    password = "admin",
    database = "quizmania"
)

def insertUserData(): #deprecated
    mycursor = quizManiaDB.cursor()
    sql = "INSERT INTO user (name,surname,email,newsletter,type_text) VALUES (%s, %s,%s,%s,%s)"
    val = ("Leon","Rosamilia","leon.rosamili@gmail.com",1,"altro")
    mycursor.execute(sql, val)
    quizManiaDB.commit()

def insert(name,surname,email,newsletter,job,room):
    try:
        if request.method == 'POST':
            mycursor = quizManiaDB.cursor()
            sql = "INSERT INTO player (session_id,timestamp,room) VALUES (%s, %s, %s)"
            val = (session['id'], time.time(), int(room))
            mycursor.execute(sql, val)
            quizManiaDB.commit()
    except:
        print("Errore di inserimento nel db: " + str(session['id']) + " " + str(time.time()) + " " + room)
    try:
        if request.method == 'POST':
            mycursor = quizManiaDB.cursor()
            sql = "INSERT INTO user (name,surname,email,newsletter,type_text,user_session_id) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (name, surname, email, newsletter, job, session['id'])
            mycursor.execute(sql, val)
            quizManiaDB.commit()
    except:
        print("Errore di inserimento nel db: " + name + " " + surname + " " + email + " " + str(newsletter) + " " + job)

def generate_random_code():
    return "{:04d}".format(random.randint(0, 9999))

def generateQR(link,filename):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save('static/' + filename + '.png')
def getCurrentIP():
    #local_hostname = socket.gethostname()
    #ip_addresses = socket.gethostbyname_ex(local_hostname)[2]
    #filtered_ips = [ip for ip in ip_addresses if not ip.startswith("127.")]
    #first_ip = filtered_ips[:1]
    #return first_ip[0]
    return "192.168.2.11"

def generateSessionId(email):
    id = str(time.time())
    id += email
    return hash(id)

@app.route('/')
def main_page():  # put application's code here
    return "temporary"

@app.route('/play/')
def play_page():  # put application's code here
    room = request.args.get('room', '0000')
    name = ""
    surname = ""
    try:
        if session['id'] == None:
            return redirect('/guestForm', code=302)
        else:
            mycursor = quizManiaDB.cursor()
            mycursor.execute("SELECT name,surname FROM user WHERE player_session_id = %s", (session['id'],))
            myresult = mycursor.fetchall()
            for x in myresult:
                name = x
    except:
        return redirect('/guestForm/?room=' + str(room), code=302)
    return render_template('waiting_room.html', username=(name))

@app.route('/host/')
def host_page():  # put application's code here
    room_code = generate_random_code()
    generateQR('http://'+getCurrentIP()+'/play/?room=' + room_code, "qr")
    session['id'] = generateSessionId("0")
    try:
        if request.method == 'POST':
            mycursor = quizManiaDB.cursor()
            sql = "INSERT INTO host (session_id) VALUES (%s)"
            val = (session['id'])
            mycursor.execute(sql, val)
            quizManiaDB.commit()
    except:
        print("Errore di inserimento nel db: ")
    try:
        if request.method == 'POST':
            mycursor = quizManiaDB.cursor()
            sql = "INSERT INTO room (id,host_session_id) VALUES (%s, %s)"
            val = (id, session['id'])
            mycursor.execute(sql, val)
            quizManiaDB.commit()
    except:
        print("Errore di inserimento nel db: ")
    return render_template('index.html', qrcode="../static/qr.png", room_code=room_code)

@app.route('/mobile-answer')
def get_question():
    try:
        # Esegui una query per ottenere una domanda casuale
        mycursor = quizManiaDB.cursor()
        mycursor.execute("SELECT question.text FROM question JOIN belongs ON question_id WHERE question.id = belongs.question_id AND belongs.topic_id = 1 LIMIT 1")
        question = mycursor.fetchone()[0]
        return render_template('mobile-answer.html', question=question)
    except Exception as e:
        return str(e), 500

@app.route('/guestForm/', methods=["POST", "GET"])
def guestForm():
    room = request.args.get('room', '0000')
    if request.method == "POST":
        first_name = request.form.get("name")
        last_name = request.form.get("surname")
        email = request.form.get("email")
        newsletter = request.form.get("newsletter")
        job = request.form.get("type")
        if newsletter == "True":
            newsletter = 1
        else:
            newsletter = 0
        session['id'] = generateSessionId(email)
        insert(first_name,last_name,email,newsletter,job,room)
        return redirect("/play/?room=" + str(room), code=302)
    tmp = "/play/?room=" + str(room)
    return render_template("guestForm.html",tmp=tmp)

@app.route('/host/ingame/', methods=["POST", "GET"])
def inGame():
    return "no"


if __name__ == '__main__':
    tmp = getCurrentIP()
    app.run(host=tmp, port=80)
