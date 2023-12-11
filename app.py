from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('indexweb.html')

@app.route("/loginadm")
def loginadm():
    return render_template('loginadmin.html')

@app.route("/loginpmh")
def loginpmh():
    return render_template('loginpemohon.html')

@app.route('/registrasipmh')
def registrasipmh():
    return render_template('registrasipemohon.html')

if __name__ == '__main__':
    app.run (debug = True)