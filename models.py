from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    senha = db.Column(db.String(100))
    nivel = db.Column(db.String(20))  # admin ou recepção

class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    colaborador = db.Column(db.String(100))
    empresa = db.Column(db.String(100))
    soc = db.Column(db.String(20))
    tipo_exame = db.Column(db.String(100))
    exames = db.Column(db.String(200))
    data = db.Column(db.String(20))
    hora = db.Column(db.String(10))
    compareceu = db.Column(db.String(10))
    entrada = db.Column(db.String(10))
    saida = db.Column(db.String(10))