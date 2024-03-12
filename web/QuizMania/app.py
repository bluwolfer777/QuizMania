import qrcode, socket
from flask import Flask, render_template_string, request, session, redirect, url_for, render_template
from flask_session import Session
import time
import mysql.connector

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = '123456789'

mydb = mysql.connector.connect(
    host = "192.168.2.2",
    user = "esteban",
    password = "admin",
    database = "quizmania"
)

def insertUserData():
    mycursor = mydb.cursor()
    sql = "INSERT INTO user (name,surname,email,newsletter,type_text) VALUES (%s, %s,%s,%s,%s)"
    val = ("Leon","Rosamilia","leon.rosamili@gmail.com",1,"altro")
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    mydb.commit()

print(mydb)

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
    return id

@app.route('/')
def main_page():  # put application's code here
    return render_template('index.html', qrcode="../static/qr.png")

@app.route('/play/')
def play_page():  # put application's code here
    insertUserData()
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
        print(first_name, last_name, email, newsletter)
        session['id'] = generateSessionId(email)
    return render_template("guestForm.html")



if __name__ == '__main__':
    tmp = getCurrentIP()
    app.run(host=tmp)

