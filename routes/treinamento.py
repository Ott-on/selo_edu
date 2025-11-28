from flask import Blueprint
from flask_login import login_required
from views import treinamento as treinamento_views

treinamento_bp = Blueprint('treinamento', __name__, url_prefix="/dashboard")

treinamento_bp.add_url_rule(
    "/",
    view_func=login_required(treinamento_views.dashboard),
    endpoint="dashboard"
)

treinamento_bp.add_url_rule(
    "/treinamento/<int:treinamento_id>/turmas",
    view_func=login_required(treinamento_views.listar_turmas),
    endpoint="listar_turmas",
    methods=["GET"]
)

treinamento_bp.add_url_rule(
    "/treinamento/<int:treinamento_id>/turmas/criar",
    view_func=login_required(treinamento_views.criar_turma),
    endpoint="criar_turma",
    methods=["GET", "POST"]
)

treinamento_bp.add_url_rule(
    "/turma/<int:turma_id>/alunos",
    view_func=login_required(treinamento_views.vincular_alunos),
    endpoint="vincular_alunos",
    methods=["GET", "POST"]
)
