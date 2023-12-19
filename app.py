from flask import Flask, request, render_template, redirect, url_for, session
from database import initialize_database, get_database_cursor, create_database, insert_admins, check_admin_credentials

app = Flask(__name__)
app.secret_key = 'ISILAKAFT'

db = initialize_database()
cursor = get_database_cursor()
create_database()
insert_admins()

@app.route("/")
def home():
    return render_template('indexweb.html')


@app.route('/indexadm') #index
def indexadm():
    return render_template('indexadm.html')

@app.route("/loginadm", methods=['GET', 'POST'])
def loginadm():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if check_admin_credentials(username, password):
            return redirect(url_for('indexadm'))
        else:
            return render_template('loginadmin.html', error="Username atau password salah")

    else:
        return render_template('loginadmin.html')

@app.route("/loginpmh")
def loginpmh():
    return render_template('loginpemohon.html')

@app.route('/registrasipmh')
def registrasipmh():
    return render_template('registrasipemohon.html')

if __name__ == '__main__':
    app.run (debug = True)