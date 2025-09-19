from flask import Flask, render_template

app = Flask(__name__)

users = [
    {"id":1, 
     "nome": "Mauro Ramos", 
     "email":"mauro@gmail.com", 
     "perfil":"Coordenador", 
     "status":"Ativo"
     },
    {"id":2, 
     "nome": "Ana Nígeria", 
     "email":"ana@outlook.com", 
     "perfil":"Desenvolvedor", 
     "status":"Ativo"
     },
    {"id":3, 
     "nome": "Carlos Almeida", 
     "email":"car2024.almeida@hotmail.com", 
     "perfil":"Gerente de Projetos", 
     "status":"Inativo"
     },
    {"id":4, 
     "nome": "Beatriz Mato Grosso", 
     "email":"Bea89@gmail.com", 
     "perfil":"Analista de Dados", 
     "status":"Ativo"
     },
    {"id":5, 
     "nome": "Fernando Pessoa", 
     "email":"fernando.souza@gmail.com", 
     "perfil":"Designer UX/UI", 
     "status":"Ativo"
     },
    {"id":6, 
     "nome": "Juliana Beira", 
     "email":"juju.limas@gmail.com", 
     "perfil":"QA", 
     "status":"Inativo"
     },
    {"id":7, 
     "nome": "Joaquim Ribeiro", 
     "email":"jojo@gmail.com", 
     "perfil":"Suporte Técnico",
     "status":"Ativo"
    } 
]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/users")
def users_render():
    return render_template("users.html", users=users)

@app.route("/login")
def login():
    return render_template("auth/login.html")