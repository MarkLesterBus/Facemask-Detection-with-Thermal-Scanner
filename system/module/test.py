from flask import Flask, render_template, url_for, flash, request, redirect, session
import sqlite3
import os
import datetime
from werkzeug.utils import secure_filename
from sqlite3 import Error
from PIL import Image
import PIL

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = './static/faces/model/'
UPLOAD_AVATAR = './static/avatar'


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


@app.route('/', methods=['GET', 'POST'])
@app.route('/main', methods=['GET', 'POST'])
def main():
    if session.get('logged_in'):
        if session['logged_in'] == True:
            user = (
            session.get('user_name'), session.get('user_email'), session.get('user_type'), session.get('user_image'))
            log_date = log_dates()
            logs = get_logs()
            return render_template('index.html', user=user, log_date=log_date, logs=logs)
    else:
        return redirect(url_for('login'))


def log_dates():
    try:
        conn = create_connection('database/face_db.sqlite')
        cur = conn.cursor()
        query = """
                SELECT log_date FROM logs GROUP BY log_date
                """
        cur.execute(query)
        log_date = cur.fetchall()
        conn.close()
        return log_date
    except Error as e:
        print(e)


def get_logs():
    try:
        conn = create_connection('database/face_db.sqlite')
        cur = conn.cursor()
        query = """
                SELECT * FROM logs GROUP BY log_image
                """
        cur.execute(query)
        logs = cur.fetchall()
        conn.close()
        return logs
    except Error as e:
        print(e)


@app.route('/users', methods=['GET'])
@app.route('/users/show', methods=['GET'])
def show_users():
    user = (session.get('user_name'), session.get('user_email'), session.get('user_type'), session.get('user_image'))
    try:
        conn = create_connection('database/face_db.sqlite')
        cur = conn.cursor()
        query = """
                SELECT * FROM users 
                """
        cur.execute(query)
        users = cur.fetchall()
        conn.close()
    except Error as e:
        print(e)

    return render_template('users/index.html', users=users, user=user)


@app.route('/users/create', methods=['GET', 'POST'])
def create_users():
    conn = create_connection('database/face_db.sqlite')
    user = (session.get('user_name'), session.get('user_email'), session.get('user_type'), session.get('user_image'))
    path = os.path.join(APP_ROOT, UPLOAD_AVATAR)

    if request.method == "POST":
        try:
            name = request.form['name']
            email = request.form['email']
            password = request.form['pass']
            utype = request.form['utype']

            cur = conn.cursor()
            if request.files['file'].filename == '':
                query = """
                        INSERT INTO users(`user_name`,`user_email`,`user_pass`,`user_type`)
                        VALUES(?,?,?,?)
                        """
                cur.execute(query, (name, email, password, utype))
            else:
                image = request.files['file']
                filename = secure_filename(name + ".png")
                image.save(os.path.join(path, filename))
                query = """
                    INSERT INTO users(`user_name`,`user_email`,`user_pass`,`user_type`,`Field6`)
                    VALUES(?,?,?,?,?)
                    """
                cur.execute(query, (name, email, password, utype, filename))

            conn.commit()
            conn.close
            return redirect(url_for('show_users'))
        except Error as e:
            print(e)

    return render_template('users/create.html', user=user)


@app.route('/users/edit/<int:user_id>', methods=['GET', 'post'])
def edit_users(user_id):
    user = (session.get('user_name'), session.get('user_email'), session.get('user_type'), session.get('user_image'))
    conn = create_connection('database/face_db.sqlite')
    if request.method == "POST":
        update_users(user_id)
        return redirect(url_for('show_users'))

    else:
        cur = conn.cursor()
        query = """
                SELECT * FROM users WHERE `user_id` = ? 
                """
        cur.execute(query, (user_id,))
        users = cur.fetchall()
        cur.close()

    return render_template('users/edit.html', users=users, user=user)


def update_users(user_id):
    conn = create_connection('database/face_db.sqlite')
    path = os.path.join(APP_ROOT, UPLOAD_AVATAR)
    if request.method == "POST":
        try:
            name = request.form['name']
            email = request.form['email']
            password = request.form['pass']
            utype = request.form['utype']

            cur = conn.cursor()
            if request.files['file'].filename == '':
                query = """
                        UPDATE users 
                        SET
                            user_name = ?,
                            user_email = ?,
                            user_pass = ?,
                            user_type = ?
                        WHERE user_id = ?
                        """
                cur.execute(query, (name, email, password, utype))
            else:
                image = request.files['file']
                filename = secure_filename(name + ".png")

                if os.path.exists(os.path.join(APP_ROOT, UPLOAD_AVATAR) + filename):
                    os.remove(os.path.join(APP_ROOT, UPLOAD_AVATAR) + filename)

                image.save(os.path.join(path, filename))

                query = """
                        UPDATE users 
                        SET
                            user_name = ?,
                            user_email = ?,
                            user_pass = ?,
                            user_type = ?,
                            user_image = ?
                        WHERE user_id = ?
                        """
                cur.execute(query, (name, email, password, utype, filename))

            conn.commit()
            conn.close()
        except Error as e:
            print(e)


@app.route('/users/delete/<user_id>', methods=['GET', 'post'])
def delete_users(user_id):
    conn = create_connection('database/face_db.sqlite')
    cur = conn.cursor()
    query = """
                    DELETE FROM users
                    WHERE user_id = ?
                """
    cur.execute(query, (user_id,))
    conn.commit()
    cur.close()
    return redirect(url_for('show_users'))


@app.route('/faces', methods=['GET'])
@app.route('/faces/show', methods=['GET'])
def show_faces():
    user = (session.get('user_name'), session.get('user_email'), session.get('user_type'), session.get('user_image'))
    try:
        conn = create_connection('database/face_db.sqlite')
        cur = conn.cursor()
        query = """
                SELECT * FROM faces 
                """
        cur.execute(query)
        faces = cur.fetchall()
        conn.close()
    except Error as e:
        print(e)

    return render_template('faces/index.html', faces=faces, user=user)


@app.route('/faces/create', methods=['GET', 'POST'])
def create_faces():
    main()
    user = (session.get('user_name'), session.get('user_email'), session.get('user_type'), session.get('user_image'))
    conn = create_connection('database/face_db.sqlite')
    path = os.path.join(APP_ROOT, UPLOAD_FOLDER)

    if request.method == "POST":
        try:
            name = request.form['name']
            file = request.files['file']
            date_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            filename = secure_filename(name + ".png")
            file.save(os.path.join(path, filename))

            cur = conn.cursor()
            query = """
                    INSERT INTO faces(`face_name`,`face_image`,`face_status`,`face_created`)
                    VALUES(?,?,?,?)
                    """
            cur.execute(query, (name, filename, "known", date_created))
            conn.commit()
            conn.close
            return redirect(url_for('show_faces'))
        except Error as e:
            print(e)

    return render_template('faces/create.html', user=user)


@app.route('/faces/edit/<face_id>', methods=['GET', 'post'])
def edit_faces(face_id):
    main()
    user = (session.get('user_name'), session.get('user_email'), session.get('user_type'), session.get('user_image'))
    face_id = int(face_id)
    conn = create_connection('database/face_db.sqlite')
    if request.method == "POST":
        update_faces(face_id)
        return redirect(url_for('show_faces'))
    if request.method == "GET":
        try:
            cur = conn.cursor()
            query = """
                    SELECT * FROM faces 
                    WHERE `face_id` = ? 
                    """
            cur.execute(query, (face_id,))
            faces = cur.fetchall()
            cur.close()
        except Error as e:
            print(e)

    return render_template('faces/edit.html', faces=faces, user=user)


def update_faces(face_id):
    conn = create_connection('database/face_db.sqlite')
    path = os.path.join(APP_ROOT, UPLOAD_FOLDER)
    if request.method == "POST":
        try:
            name = request.form['name']
            file = request.files['file']

            filename = secure_filename(name + ".png")
            if os.path.exists(os.path.join(APP_ROOT, UPLOAD_FOLDER) + filename):
                os.remove(os.path.join(APP_ROOT, UPLOAD_FOLDER) + filename)
            cur = conn.cursor()
            file.save(os.path.join(path, filename))
            query = """
                    UPDATE faces
                    SET
                        face_name = ?,
                        face_image = ?
                    WHERE face_id = ?
                    """
            cur.execute(query, (name, filename, face_id))
            conn.commit()
            conn.close()
        except Error as e:
            print(e)


@app.route('/faces/delete/<string:face_image>', methods=['GET', 'post'])
def delete_faces(face_image):
    conn = create_connection('database/face_db.sqlite')
    cur = conn.cursor()
    if os.path.exists(os.path.join(APP_ROOT, UPLOAD_FOLDER) + face_image):
        os.remove(os.path.join(APP_ROOT, UPLOAD_FOLDER) + face_image)
        print("file deleted!")

    query = """
                    DELETE FROM faces
                    WHERE face_image = ?
                """
    cur.execute(query, (face_image,))
    conn.commit()
    cur.close()
    return redirect(url_for('show_faces'))


@app.route('/auth')
@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    conn = create_connection('database/face_db.sqlite')

    if request.method == "POST":
        try:
            email = request.form['email']
            password = request.form['password']

            cur = conn.cursor()
            query = """
                    SELECT * FROM users WHERE user_email = ? AND user_pass = ?
                    """
            cur.execute(query, (email, password))
            users = cur.fetchall()
            if not users:
                print('no records')
            else:
                for user in users:
                    session['logged_in'] = True
                    session['user_name'] = user[1]
                    session['user_email'] = user[2]
                    session['user_type'] = user[4]
                    session['user_image'] = user[5]

            conn.close()
            return redirect(url_for('main'))
        except Error as e:
            print(e)

    return render_template('auth/login.html')


@app.route('/auth/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host="192.168.1.102", port="5000", debug=True)
    # app.run(debug=True)
