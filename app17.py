from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from model_bd import db, User
from form1 import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_database.db'
db.init_app(app)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('OK')


@app.cli.command("del-alex")
def del_user():
    user = User.query.filter_by(name='Александр').first()
    db.session.delete(user)
    db.session.commit()
    print('Delete Alex from DB!')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        name = form.name.data
        family_name = form.family_name.data
        email = form.email.data
        password = form.password.data
        user = User(name, family_name, email, password)
        db.session.add(user)
        db.session.commit()
        print(name, family_name, email, password)
    return render_template('register.html', form=form)


@app.route('/')
def index():
    return 'Hi'


if __name__ == '__main__':
    app.run(debug=True)
