from flask import Flask
import qrcode

app = Flask(__name__, static_url_path='/static')
def generateQR(link):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save('static/qr.png')


@app.route('/')
def hello_world():  # put application's code here
    generateQR("https://www.youtube.com/watch?v=dQw4w9WgXcQ&pp=ygUXbmV2ZXIgZ29ubmEgZ2l2ZSB5b3UgdXA%3D")
    print("Hello World!")
    return "<img src='/static/qr.png'>"


if __name__ == '__main__':
    app.run()
