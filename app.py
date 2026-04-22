import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def init_db():
    with sqlite3.connect('citas.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mascota TEXT NOT NULL,
                propietario TEXT NOT NULL,
                especie TEXT,
                fecha TEXT NOT NULL
            )
        ''')
        conn.commit()

# Inicializar la base de datos
init_db()

@app.route('/')
def index():
    with sqlite3.connect('citas.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pacientes ORDER BY fecha')
        citas = cursor.fetchall()
    return render_template('index.html', citas=citas)

@app.route('/nueva', methods=['GET', 'POST'])
def nueva_cita():
    if request.method == 'POST':
        mascota = request.form['mascota']
        propietario = request.form['propietario']
        especie = request.form['especie']
        fecha = request.form['fecha']
        with sqlite3.connect('citas.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO pacientes (mascota, propietario, especie, fecha)
                VALUES (?, ?, ?, ?)
            ''', (mascota, propietario, especie, fecha))
            conn.commit()
        return redirect(url_for('index'))
    return render_template('nueva.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_cita(id):
    with sqlite3.connect('citas.db') as conn:
        cursor = conn.cursor()
        if request.method == 'POST':
            mascota = request.form['mascota']
            propietario = request.form['propietario']
            especie = request.form['especie']
            fecha = request.form['fecha']
            cursor.execute('''
                UPDATE pacientes
                SET mascota=?, propietario=?, especie=?, fecha=?
                WHERE id=?
            ''', (mascota, propietario, especie, fecha, id))
            conn.commit()
            return redirect(url_for('index'))
        else:
            cursor.execute('SELECT * FROM pacientes WHERE id = ?', (id,))
            cita = cursor.fetchone()
    return render_template('editar.html', cita=cita)

@app.route('/eliminar/<int:id>')
def eliminar_cita(id):
    with sqlite3.connect('citas.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM pacientes WHERE id = ?', (id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    