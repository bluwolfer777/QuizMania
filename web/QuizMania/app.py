from flask import Flask, render_template_string, request, session, redirect, url_for, render_template
from flask_session import Session
import qrcode
import time

app = Flask(__name__, static_url_path='/static')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def generateQR(link,filename):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save('static/' + filename + '.png')

def generateSessionId(email):
    id = str(time.time())
    id += email
    return id

@app.route('/')
def main_page():  # put application's code here
    return "<img src='/static/qr.png'>"

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
        print(first_name, last_name, email, newsletter)
        session['id'] = generateSessionId(email)
    return render_template("guestForm.html")



if __name__ == '__main__':
    app.run()
