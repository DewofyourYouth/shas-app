import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


sql_pass = os.getenv('SQL_PASSWORD')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:{}@localhost/shas_app'.format(sql_pass)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

def create_pages():
    ms = Meseches.query.all()
    print(ms)
    for m in ms:
        for i in range(m.num_pages):
            page = Page(page_num = (i + 2), book_id= m.m_id)
            db.session.add(page)
            db.session.commit()
            print('Page created!')
    print('All pages created!')
