from flask import Flask, request, render_template, redirect, url_for, session
from database import initialize_database, get_database_cursor, create_database, insert_admins, check_admin_credentials, check_user_credentials, insert_users

app = Flask(__name__)
app.secret_key = 'ISILAKAFT'

db = initialize_database()
cursor = get_database_cursor()
create_database()
insert_admins()
insert_users()

@app.route("/")
def home():
    return render_template('indexweb.html')


@app.route('/addpengajuan', methods=['POST'])
def addPengajuan():
    if request.method == 'POST':
        nrp = request.form.get('nrp')
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')

        cursor.execute('INSERT INTO your _table (NRP, Name, Age, Gender, (nrp, name, age, gender, diajukan))')
        db.commit()

        return redirect (url_for('home'))
    return render_template('index.html')


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

@app.route('/pengajuan') #index
def pengajuan():
    return render_template('pengajuanadm.html')

@app.route('/pengembalian') #index
def pengembalian():
    return render_template('pengembalianadm.html')

@app.route('/indexpmh') #index
def indexpmh():
    return render_template('indexpmh.html')

@app.route("/loginpmh", methods=['GET', 'POST'])
def loginpmh():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if check_user_credentials(username, password):
            return redirect(url_for('indexpmh'))
        else:
            return render_template('loginpemohon.html', error="Username atau password salah")

    else:
        return render_template('loginpemohon.html')

@app.route('/pengajuanpmh') #index
def pengajuanpmh():
    return render_template('pengajuanpmh.html')

@app.route('/pengembalianpmh') #index
def pengembalianpmh():
    return render_template('pengembalianpmh.html')

if __name__ == '__main__':
    app.run (debug = True)