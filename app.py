import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


sql_pass = os.getenv('SQL_PASSWORD')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:{}@localhost/shas_app'.format(sql_pass)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    u_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))

    def __repr__(self):
        return f'<User: {self.username}>'


class Meseches(db.Model):
    m_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    num_pages = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Meseches: {self.name}>'


class Page(db.Model):
    p_id = db.Column(db.Integer, primary_key=True)
    page_num = db.Column(db.Integer, nullable=False)

    book_id = db.Column(db.Integer, db.ForeignKey('meseches.m_id'), nullable=False)
    meseches = db.relationship('Meseches', backref=db.backref('pages', lazy=True))

    def __repr__(self):
        return f'<Page: m{self.book_id}, num {self.page_num}>'


class Note(db.Model):
    n_id = db.Column(db.Integer, primary_key=True)
    note_title = db.Column(db.String(100), nullable=True)
    note_text = db.Column(db.Text, nullable=False)

    page_id = db.Column(db.Integer, db.ForeignKey(page.p_id), nullable=False)
    page = db.relationship('Page', backref=db.backref('notes', lazy=True))


def create_pages():
    """
    A function for creating all pages of shas
    """
    if Page.query.all() == []:
        ms = Meseches.query.all()
        print(ms)
        for m in ms:
            for i in range(m.num_pages):
                page = Page(page_num = (i + 2), book_id= m.m_id)
                db.session.add(page)
                db.session.commit()
            print(f'Pages for {m.name} created!')
        print('All pages created!')
