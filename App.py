from flask import Flask, render_template, request, redirect, url_for, flash #import modulo para framework flask,rutero, request para los post
from flask_mysqldb import MySQL #import modulo para sql

app = Flask(__name__)

#mysql connection
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "flaskcontacts"

mysql = MySQL(app)
app.secret_key = 'mysecretkey'


@app.route('/')
def home():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contatcs')
    data = cursor.fetchall()
    return render_template('home.html', contactos = data)


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO contatcs (fullname, phone, email) VALUES (%s, %s, %s)',(fullname, phone, email))
        mysql.connection.commit()
        flash('Contacto agregado satisfactoriamente')
        return redirect(url_for('home'))


@app.route('/edit_contact/<id>')
def edit_contact(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM contatcs WHERE id=%s", [id])
    data = cursor.fetchall()
    return render_template('edit-contact.html', contacto = data[0])

@app.route('/update_contact/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE contatcs SET fullname = %s, phone = %s, email = %s WHERE id = %s', (fullname, phone, email, id))
        mysql.connection.commit()
        flash('Contacto modificado satisfactoriamente')
        return redirect(url_for('home'))


@app.route('/delete/<string:id>')
def delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM contatcs WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto borrado satisfactoriamente')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(port= 3000, debug=True)
