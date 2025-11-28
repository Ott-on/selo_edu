from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .turma import turma_alunos  # Importa a tabela de associação

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="aluno")
    ativo = db.Column(db.Boolean, default=True)

    profile = db.relationship('Profile', uselist=False, back_populates='user')

    # Relacionamento Muitos-para-Muitos com Turma
    # Um aluno pode estar em várias turmas, e uma turma tem vários alunos.
    turmas = db.relationship('Turma', secondary=turma_alunos, lazy='subquery',
                             back_populates='alunos')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)