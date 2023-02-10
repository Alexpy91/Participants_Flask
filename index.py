from flask import Flask, request, redirect, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

site = Flask(__name__)

site.config['SECRET_KEY'] = 'gsghsfuseufhseukfilhsbaf'

site.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///participants.bd'
site.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(site)

class Participants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    theme = db.Column(db.String, nullable=False)
    organization = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    mail = db.Column(db.String, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Participants %r>' % self.id

@site.route('/')
def index():
    return render_template('index.html')


@site.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        if request.form['username'] != '' and request.form['message'] != ' ':
            print(request.form['username'])
            flash("Данные отправлены успешно!", category='success')
        else:
            flash("Ошибка заполните необходимые данные!", category='error')

    return render_template('contact.html')


@site.route('/participants')
def participants_list():
    users = Participants.query.order_by(Participants.date.desc()).all()
    return render_template("participants.html", users=users)


@site.route('/admin')
def admin():
    users = Participants.query.order_by(Participants.date.desc()).all()
    return render_template("admin.html", users=users)


@site.route('/admin/<int:id>')
def user_detail(id):
    user = Participants.query.get(id)
    return render_template("user_detail.html", user=user)


@site.route('/admin/<int:id>/delete')  # delete
def user_delete(id):
    user = Participants.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        return redirect('/admin')
    except:
        return "При удалении пользователя произошла ошибка"


@site.route('/autorization', methods=['POST', 'GET'])
def autorization():
    if request.method == "POST":
        if request.form['login'] == '' and request.form['password'] == '':
            users = Participants.query.order_by(Participants.date.desc()).all()
            return render_template("admin.html", users=users)

        elif request.form['login'] == '':
            return "Поле логин не заполнено"

        elif request.form['password'] == '':
            return "Поле пароль не заполнено"
        else:
            return "Ошибка логин или пароль не верны"

    else:
        return render_template('autorization.html')


@site.route('/reg', methods=['POST', 'GET'])
def reg():
    if request.method == "POST":
        if request.form['name'] == '' or request.form['theme'] == '' or request.form['mail'] == '':
            return "Вы не запонили обязательные поля для регистрации"
        else:
            name = request.form['name']
            theme = request.form['theme']
            mail = request.form['mail']

            if request.form['organization'] == '':
                organization = 'Данные не заполнены'
            else:
                organization = request.form['organization']

            if request.form['phone'] == '':
                phone = 'Данные не заполнены'
            else:
                phone = request.form['phone']

            if request.form['comment'] == '':
                comment = 'Данные не заполнены'
            else:
                comment = request.form['comment']


            participants = Participants(name=name, theme=theme, organization=organization, phone=phone, mail=mail,
                                        comment=comment)
            users = Participants.query.order_by(Participants.date.desc()).all()
            for el in users:
                if el.name == name or el.mail == mail or el.phone == phone:
                    return "Такой пользователь уже зарегистрирован"

            try:
                db.session.add(participants)
                db.session.commit()
                return redirect('participants')
            except:
                return "Регистрация не удалась, во время регистрации произошла ошибка"

    else:
        return render_template('reg.html')


@site.route('/admin/<int:id>/update', methods=['POST', 'GET'])
def user_update(id):
    user = Participants.query.get(id)
    if request.method == "POST":
        if request.form['name'] == '' or request.form['theme'] == '' or request.form['mail'] == '':
            return "Вы не запонили обязательные поля для регистрации"
        else:
            user.name = request.form['name']
            user.theme = request.form['theme']
            user.mail = request.form['mail']

            if request.form['organization'] == '':
                user.organization = 'Данные не заполнены'
            else:
                user.organization = request.form['organization']

            if request.form['phone'] == '':
                user.phone = 'Данные не заполнены'
            else:
                user.phone = request.form['phone']

            if request.form['comment'] == '':
                user.comment = 'Данные не заполнены'
            else:
                user.comment = request.form['comment']

            try:
                db.session.commit()
                return redirect('/admin')

            except:
                return "Ошибка. Не удалось изменить данные пользователя"

    else:

        return render_template('create_user.html', user=user)


if __name__ == '__main__':
    site.run(debug=True)
