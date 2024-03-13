import qrcode, socket
from flask import Flask, render_template_string, request, session, redirect, url_for, render_template
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

def insert(name,surname,email,newsletter,job):
    try:
        if request.method == 'POST':
            mycursor = quizManiaDB.cursor()
            sql = "INSERT INTO user (name,surname,email,newsletter,type_text) VALUES (%s, %s,%s,%s,%s)"
            val = (name, surname, email, newsletter, job)
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
    local_hostname = socket.gethostname()
    ip_addresses = socket.gethostbyname_ex(local_hostname)[2]
    filtered_ips = [ip for ip in ip_addresses if not ip.startswith("127.")]
    first_ip = filtered_ips[:1]
    return first_ip[0]

def generateSessionId(email):
    id = str(time.time())
    id += email
    return hash(id)

@app.route('/')
def main_page():  # put application's code here
    try:
        if session['id'] == None:
            return redirect('/guestForm', code=302)
    except:
        return redirect('/guestForm', code=302)
    room_code = generate_random_code()
    generateQR(room_code, "qr")

    return render_template('index.html', qrcode="../static/qr.png", room_code=room_code)

@app.route('/play/')
def play_page():  # put application's code here
    return "play page"

@app.route('/host/')
def host_page():  # put application's code here
    print("Hello World!")
    return "host page"

@app.route('/guestForm/', methods=["POST", "GET"])
def guestForm():
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
        insert(first_name,last_name,email,newsletter,job)
        return redirect("/", code=302)
    return render_template("guestForm.html")


if __name__ == '__main__':
    tmp = getCurrentIP()
    app.run(host=tmp, port=80)
