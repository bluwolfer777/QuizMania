from flask import Flask,render_template_string, request, session, redirect, url_for
import qrcode, socket

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'chiaveSegretaDaCambiare'
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


@app.route('/')
def main_page():  # put application's code here
    generateQR("https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUXbmV2ZXIgZ29ubmEgZ2l2ZSB5b3UgdXA%3D","coso")
    print("Hello World!")
    return "<img src='/static/qr.png'>"

@app.route('/play/')
def play_page():  # put application's code here
    session['gameNumber'] = request.form['gameNumber']
    return "play page"

@app.route('/host/')
def host_page():  # put application's code here
    print("Hello World!")
    return "host page"


if __name__ == '__main__':
    tmp = getCurrentIP()
    app.run(host=tmp)
