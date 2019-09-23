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
