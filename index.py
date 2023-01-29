from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

site = Flask(__name__)

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


@site.route('/contact')
def contact():
    return render_template('contact.html')


@site.route('/admin')
def admin():
    users = Participants.query.order_by(Participants.date.desc()).all()
    return render_template("admin.html", users=users)


@site.route('/admin/<int:id>')
def user_detail(id):
    user = Participants.query.get(id)
    return render_template("user_detail.html", user=user)


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

            participants = Participants(name=name, theme=theme, organization=organization, phone=phone, mail=mail, comment=comment)

            try:
                db.session.add(participants)
                db.session.commit()
                return redirect('/')
            except:
                return "Регистрация не удалась, во время регистрации произошла ошибка"

    else:
        return render_template('reg.html')


if __name__ == '__main__':
    site.run(debug=True)
