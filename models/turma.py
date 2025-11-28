from extensions import db

# Tabela de associação para o relacionamento Muitos-para-Muitos entre Turma e User (alunos)
turma_alunos = db.Table('turma_alunos',
    db.Column('turma_id', db.Integer, db.ForeignKey('turmas.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

class Turma(db.Model):
    __tablename__ = "turmas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    
    # Chave estrangeira para o treinamento ao qual a turma pertence
    treinamento_id = db.Column(db.Integer, db.ForeignKey("treinamentos.id"), nullable=False)

    # Relacionamento de volta para Treinamento
    treinamento = db.relationship('Treinamento', back_populates='turmas')

    # Relacionamento Muitos-para-Muitos com User (alunos)
    alunos = db.relationship('User', secondary=turma_alunos, lazy='subquery',
                             back_populates='turmas')

    def __repr__(self):
        return f'<Turma {self.nome}>'
