from flask import render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from models.treinamento import Treinamento
from models.turma import Turma
from models.user import User
from extensions import db
from datetime import datetime

@login_required
def dashboard():
    """
    Exibe a dashboard principal do coordenador com a lista de todos os treinamentos.
    """
    if current_user.role != 'coordenador':
        abort(403)
    
    treinamentos = Treinamento.query.order_by(Treinamento.data_inicio.desc()).all()
    return render_template("dashboard.html", treinamentos=treinamentos)

@login_required
def listar_turmas(treinamento_id):
    """
    Lista as turmas existentes para um treinamento específico.
    """
    if current_user.role != 'coordenador':
        abort(403)
        
    treinamento = Treinamento.query.get_or_404(treinamento_id)
    return render_template("turma/listar_turmas.html", treinamento=treinamento)

@login_required
def criar_turma(treinamento_id):
    """
    Handle da criação de uma nova turma para um treinamento.
    """
    if current_user.role != 'coordenador':
        abort(403)
        
    treinamento = Treinamento.query.get_or_404(treinamento_id)
    if request.method == "POST":
        nome_turma = request.form.get("nome_turma")
        if not nome_turma:
            flash("O nome da turma é obrigatório.", "warning")
        else:
            nova_turma = Turma(nome=nome_turma, treinamento_id=treinamento.id)
            db.session.add(nova_turma)
            db.session.commit()
            flash("Turma criada com sucesso!", "success")
            return redirect(url_for('treinamento.listar_turmas', treinamento_id=treinamento.id))
            
    return render_template("turma/listar_turmas.html", treinamento=treinamento) 

@login_required
def vincular_alunos(turma_id):
    """
    Exibe a lista de alunos para vincular a uma turma e processa a vinculação.
    """
    if current_user.role != 'coordenador':
        abort(403)

    turma = Turma.query.get_or_404(turma_id)
    
    if request.method == "POST":
        ids_alunos_a_vincular = request.form.getlist("alunos")
        alunos_a_vincular = User.query.filter(User.id.in_(ids_alunos_a_vincular)).all()
        
        turma.alunos = alunos_a_vincular
        db.session.commit()
        
        flash(f"Alunos da turma '{turma.nome}' atualizados com sucesso!", "success")
        return redirect(url_for('treinamento.listar_turmas', treinamento_id=turma.treinamento_id))

    # Apenas usuários com a role 'aluno' são listados para seleção
    alunos_disponiveis = User.query.filter_by(role='aluno').order_by(User.nome).all()
    ids_alunos_na_turma = {aluno.id for aluno in turma.alunos}
    
    return render_template(
        "turma/vincular_alunos.html", 
        turma=turma, 
        alunos_disponiveis=alunos_disponiveis,
        ids_alunos_na_turma=ids_alunos_na_turma
    )

@login_required
def novo():
    if current_user.role != 'coordenador':
        abort(403)  # Forbidden

    if request.method == "POST":
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        data_inicio_str = request.form.get("data_inicio")
        data_fim_str = request.form.get("data_fim")

        if not nome or not data_inicio_str:
            flash("Nome e Data de Início são obrigatórios!", "danger")
            return render_template("treinamento/novo.html", form_data=request.form)

        try:
            data_inicio = datetime.fromisoformat(data_inicio_str)
            data_fim = datetime.fromisoformat(data_fim_str) if data_fim_str else None
        except ValueError:
            flash("Formato de data inválido. Use YYYY-MM-DDTHH:MM.", "danger")
            return render_template("treinamento/novo.html", form_data=request.form)

        treinamento = Treinamento(
            nome=nome,
            descricao=descricao,
            data_inicio=data_inicio,
            data_fim=data_fim,
            coordenador_id=current_user.id
        )
        db.session.add(treinamento)
        db.session.commit()

        flash("Treinamento criado com sucesso!", "success")
        return redirect(url_for("treinamento.dashboard"))

    return render_template("treinamento/novo.html")
