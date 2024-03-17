import qrcode, socket
from flask import Flask, render_template_string, request, session, redirect, url_for, render_template
from flask_session import Session
import time
import mysql.connector
import random

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = '123456789'

quizManiaDB = mysql.connector.connect(
    host = "localhost",
    user = "root",
    #password = "admin",
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
            sql = "INSERT INTO player (session_id,timestamp,room_id) VALUES (%s, %s, %s)"
            val = (str(session['id']), str(time.time()), int(room))
            mycursor.execute(sql, val)
            quizManiaDB.commit()
    except Exception as e:
        print("Errore di inserimento nel db: " + str(session['id']) + " " + str(time.time()) + " " + room)
        print(e)
    try:
        if request.method == 'POST':
            mycursor = quizManiaDB.cursor()
            sql = "INSERT INTO user (name,surname,email,newsletter,type_text,player_session_id) VALUES (%s, %s,%s,%s,%s,%s)"
            val = (name, surname, email, newsletter, job, str(session['id']))
            mycursor.execute(sql, val)
            quizManiaDB.commit()
    except:
        print("Errore di inserimento nel db: " + name + " " + surname + " " + email + " " + str(newsletter) + " " + job)
        print(e)

def generate_random_code():
    return "{:04d}".format(random.randint(0, 9999))

def generateQR(link,filename):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save('static/' + filename + '.png')
def getCurrentIP():
    local_hostname = socket.gethostname()
    ip_addresses = socket.gethostbyname_ex(local_hostname)[2]
    filtered_ips = [ip for ip in ip_addresses if not ip.startswith("127.")]
    first_ip = filtered_ips[:1]
    return first_ip[0]

def generateSessionId(email):
    id = str(time.time())
    id += email
    return hash(id)

def getUsersInRoom():
    cursor = quizManiaDB.cursor()
    sql = "SELECT user.name,user.surname FROM user,player,room,host WHERE room.host_session_id ='"+ str(session['id']) +"' AND room.id = player.room_id AND user.id = user.player_session_id ORDER BY player.timestamp"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows

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
            name = myresult[0][0] + " " + myresult[0][1]
    except Exception as e:
        print(e)
        return redirect('/guestForm/?room=' + str(room), code=302)
    return render_template('waiting_room.html', username=(name))

@app.route('/host/')
def host_page():  # put application's code here
    room_code = generate_random_code()
    generateQR('http://'+getCurrentIP()+'/play/?room=' + room_code, "qr")
    session['id'] = generateSessionId("0")
#    try:
    mycursor = quizManiaDB.cursor()
    sql = "INSERT INTO host (session_id) VALUES (%s);"
    tmp = [str(session['id'])]
    print("HOST SESSION  ID _____> "+str(session['id']))
    val = (tmp)
    mycursor.execute(sql, val)
    quizManiaDB.commit()
#    except:
#        print("Errore di inserimento nel db: ")
    try:
        mycursor = quizManiaDB.cursor()
        sql = "INSERT INTO room (id,host_session_id) VALUES (%s, %s);"
        val = (room_code, str(session['id']))
        mycursor.execute(sql, val)
        quizManiaDB.commit()
    except:
        print("Errore di inserimento nel db: ")
    return render_template('index.html', qrcode="../static/qr.png", room_code=room_code)

@app.route('/guestForm/', methods=["POST", "GET"])
def guestForm():
    room = request.args.get('room', '0000')
    if request.method == "POST":
        first_name = request.form.get("name")
        last_name = request.form.get("surname")
        email = request.form.get("email")
        newsletter = request.form.get("newsletter")
        job = request.form.get("type")
        room = request.form.get("room")
        if newsletter == "True":
            newsletter = 1
        else:
            newsletter = 0
        session['id'] = generateSessionId(email)
        insert(first_name,last_name,email,newsletter,job,room)
        return redirect("/play/?room=" + str(room), code=302)
    tmp = str(room)
    return render_template("guestForm.html",tmp=tmp)

@app.route('/host/ingame/', methods=["POST", "GET"])
def inGame():
    return "no"

@app.route('/host/showPlayers/', methods=["POST", "GET"])
def showPlayers():
    users = getUsersInRoom()
    renderedUserIcons = []
    for user in users:
        renderedUserIcons.append(
            "<div class='col'><img src='static/user.png'><br>" + user[0] + " " + user[1] + "</div>")
    out = ""
    for user in renderedUserIcons:
        out += user
    return out


if __name__ == '__main__':
    tmp = getCurrentIP()
    app.run(host=tmp, port=80)
