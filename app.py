from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_user, logout_user, login_required
from datetime import datetime
from models import db, Usuario, Empresa, Agendamento

app = Flask(__name__)
app.secret_key = "segredo"

# PostgreSQL do Render
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://USER:SENHA@HOST:PORT/DB"

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

with app.app_context():
    db.create_all()

# ===== LOGIN =====
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = Usuario.query.filter_by(username=request.form["user"]).first()
        if u and u.senha == request.form["senha"]:
            login_user(u)
            return redirect("/")
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

# ===== STATUS COR =====
def status_cor(a):
    if a.compareceu == "Não":
        return "#f8d7da"
    if a.saida:
        return "#cfe2ff"
    if a.entrada:
        return "#d1e7dd"
    return "#fff3cd"

# ===== DASHBOARD =====
@app.route("/")
@login_required
def index():
    ag = Agendamento.query.all()
    total = len(ag)
    faltas = len([a for a in ag if a.compareceu=="Não"])

    return render_template("index.html",
                           agendamentos=ag,
                           total=total,
                           faltas=faltas,
                           status_cor=status_cor)

# ===== NOVO AGENDAMENTO =====
@app.route("/add", methods=["GET","POST"])
@login_required
def add():
    empresas = Empresa.query.all()

    if request.method=="POST":
        a = Agendamento(
            colaborador=request.form["colaborador"],
            empresa=request.form["empresa"],
            soc=request.form["soc"],
            tipo_exame=request.form["tipo"],
            exames=request.form["exames"],
            data=request.form["data"],
            hora=request.form["hora"],
            compareceu="Sim"
        )
        db.session.add(a)
        db.session.commit()
        return redirect("/")

    return render_template("add.html", empresas=empresas)

# ===== EMPRESAS =====
@app.route("/empresas", methods=["GET","POST"])
@login_required
def empresas():
    if request.method=="POST":
        db.session.add(Empresa(nome=request.form["nome"]))
        db.session.commit()

    lista = Empresa.query.all()
    return render_template("empresas.html", empresas=lista)

# ===== CONTROLE =====
@app.route("/entrada/<int:id>")
@login_required
def entrada(id):
    a = Agendamento.query.get(id)
    a.entrada = datetime.now().strftime("%H:%M")
    db.session.commit()
    return redirect("/")

@app.route("/saida/<int:id>")
@login_required
def saida(id):
    a = Agendamento.query.get(id)
    a.saida = datetime.now().strftime("%H:%M")
    db.session.commit()
    return redirect("/")

@app.route("/falta/<int:id>")
@login_required
def falta(id):
    a = Agendamento.query.get(id)
    a.compareceu="Não"
    db.session.commit()
    return redirect("/")

app.run(host=``0.0.0.´´,  port=5000)