from flask import Flask, request, render_template, redirect, url_for, send_file
from database import initialize_database, get_database_cursor, create_database, insert_admins, check_admin_credentials, check_user_credentials, insert_users, id_aj, id_pn
from datetime import date
import os

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


@app.route('/addpengajuan', methods=['GET','POST'])
def addpengajuan():
    next_idpu = id_aj()
    if request.method == 'POST':
        nrp = request.form.get('nrp')
        jabatan = request.form.get('jabatan')
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        path_aju = os.path.join('static', 'pengajuan', request.files['file'].filename)
        tgl_aju = date.today().strftime('%Y-%m-%d')

        cursor.execute('INSERT INTO pengajuan (id_aju, nrp, jabatan, name, age, gender, tgl_aju, path_aju, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (next_idpu, nrp, jabatan, name, age, gender, tgl_aju, path_aju, 'Diajukan'))
        db.commit()

        return redirect (url_for('pengajuanpmh'))
    else:
        return render_template('addpengajuan.html')


@app.route('/cetakpengajuan', methods=['GET'])
def cetakpengajuan():
    file_path = 'static/surat_pengajuan.pdf'

    return send_file(file_path, as_attachment=True)

@app.route('/addpengembalian', methods=['GET','POST'])
def addpengembalian():
    next_idpn = id_pn()
    if request.method == 'POST':
        nrp = request.form.get('nrp')
        jabatan = request.form.get('jabatan')
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        path_png = os.path.join('static', 'pengembalian', request.files['file_pengembalian'].filename)
        tgl_png = date.today().strftime('%Y-%m-%d')
        print(request.files['file_pengembalian'].filename)

        cursor.execute('INSERT INTO pengembalian (id_png, nrp, jabatan, name, age, gender, tgl_png, path_png, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (next_idpn, nrp, jabatan, name, age, gender, tgl_png, path_png, 'Diajukan'))
        db.commit()

        return redirect (url_for('pengembalianpmh'))
    else:
        return render_template('addpengembalian.html')

@app.route('/cetakpengembalian', methods=['GET'])
def cetakpengembalian():
    file_path = 'static/surat_pengembalian.pdf'

    return send_file(file_path, as_attachment=True)

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
    cursor.execute("SELECT * FROM pengajuan")
    pengajuan = cursor.fetchall()
    db.commit()

    return render_template('pengajuanpmh.html', pengajuan=pengajuan)

@app.route('/pengembalianpmh') #index
def pengembalianpmh():
    cursor.execute("SELECT * FROM pengembalian")
    pengembalian = cursor.fetchall()
    db.commit()
    return render_template('pengembalianpmh.html', pengembalian=pengembalian)


if __name__ == '__main__':
    app.run (debug = True)