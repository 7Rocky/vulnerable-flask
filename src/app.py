import base64
import os

from flask import abort, flash, Flask, redirect, render_template, request, url_for

from flask_login import current_user, LoginManager, login_required, login_user, logout_user
from flask_session import Session

from werkzeug.security import generate_password_hash, check_password_hash

import db

from config import Config
from forms import LoginForm, RegisterForm, UploadForm


app = Flask(__name__, static_folder='static', static_url_path='')

app.config.from_object(Config)

Session(app)

db.init_db()

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id: str):
    return db.get_user_by_user_id(int(user_id))


@app.route('/')
@login_required
def index():
    return render_template('index.html', books=db.get_books_by_owner(current_user.user_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if (form := RegisterForm()).validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data
        password_hash = generate_password_hash(password)
        user = db.create_user(username, password_hash)
        login_user(user)
        return redirect(url_for('index'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if (form := LoginForm()).validate_on_submit():
        user, err = db.get_user_by_username(form.username.data.strip())

        if user.user_id == -1:
            flash(f'Usuario no encontrado', 'danger')
            return render_template('login.html', form=form), 200

        if err:
            abort(err)

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))

        flash('Contraseña incorrecta', 'danger')

    return render_template('login.html', form=form), 200


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if (form := UploadForm()).validate_on_submit():
        f = form.cover.data
        try:
            stored_name = f.filename
            upload_folder = app.config["UPLOAD_FOLDER"]
            os.makedirs(upload_folder, exist_ok=True)
            path = os.path.join(upload_folder, stored_name)
            f.save(path)
        except ValueError as e:
            flash(str(e), 'danger')
            return render_template('upload.html', form=form)

        db.create_book(form.title.data.strip(), form.author.data.strip(), stored_name, current_user.user_id)
        flash('Libro subido correctamente', 'success')

        return redirect(url_for('index'))

    return render_template('upload.html', form=form)


@app.route('/delete/<int:book_id>')
@login_required
def delete(book_id: int):
    book = db.get_book_by_id(book_id)

    # if book.owner_id != current_user.user_id:
    #     abort(403)

    db.delete_book_by_id(book_id)

    path = book.cover
    os.system(f'rm uploads/{path}')
    return redirect(url_for('index'))


@app.route('/cover')
@login_required
def cover():
    path = request.args.get('path', '').replace('../', '')

    try:
        with open(f'uploads/{path}', 'rb') as f:
            return 'data:image/png;base64,' + base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        abort(404)


@app.route('/search')
@login_required
def search():
    results = []

    if (q := request.args.get('q', '').strip()):
        results, err = db.search_books(q, current_user.user_id)

        if err:
            abort(500)

    return render_template('search.html', results=results, q=q)


@app.cli.command('init-db')
def init_db():
    db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
