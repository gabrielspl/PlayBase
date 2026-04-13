# jogos/routes.py
from flask import request, render_template
from .controllers import JogosController, UsuariosController, CategoriasController, UsuariosAdminController
from . import jogos_bp

controller = JogosController()
controllerUsuario = UsuariosController()
categorias_controller = CategoriasController()
usuarios_admin_controller = UsuariosAdminController()


# --- ROTA RAIZ ---
@jogos_bp.route("/")
def index():
    return render_template("pagina_inicial.html")


# --- ROTAS DE JOGOS ---
@jogos_bp.route("/cadastrar", methods=["GET", "POST"])
def cadastrar_jogo():
    if request.method == "POST":
        return controller.cadastrar_jogo()
    return controller.preparar_cadastro()

@jogos_bp.route("/jogos")
def listar_jogos():
    return controller.listar_jogos()

@jogos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_jogo(id):
    if request.method == "POST":
        return controller.editar_jogo(id)
    return controller.preparar_edicao(id)

@jogos_bp.route("/excluir/<int:id>", methods=["POST"])
def excluir_jogo(id):
    return controller.remover_jogo(id)

@jogos_bp.route("/jogos/buscar")
def buscar_jogos():
    return controller.buscar_jogos()


# --- ROTAS DE USUÁRIOS ---
@jogos_bp.route("/cadastro_usuario", methods=["GET", "POST"])
def cadastro_usuario():
    if request.method == "POST":
        return controllerUsuario.cadastro_usuario()
    return controllerUsuario.preparar_cadastro_usuario()

@jogos_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return controllerUsuario.login()
    return controllerUsuario.preparar_login()

@jogos_bp.route("/logout")
def logout():
    return controllerUsuario.logout()

@jogos_bp.route("/perfil", methods=["GET", "POST"])
def perfil():
    if request.method == "POST":
        return controllerUsuario.editar_usuario()
    return controllerUsuario.preparar_edicao_usuario()


# --- RECUPERAÇÃO DE SENHA ---
@jogos_bp.route("/esqueci-senha", methods=["GET", "POST"])
def esqueci_senha():
    if request.method == "POST":
        return controllerUsuario.esqueci_senha()
    return controllerUsuario.preparar_esqueci_senha()

@jogos_bp.route("/redefinir-senha/<token>", methods=["GET", "POST"])
def redefinir_senha(token):
    if request.method == "POST":
        return controllerUsuario.redefinir_senha(token)
    return controllerUsuario.preparar_redefinir_senha(token)


# --- ROTA CONTATO ---
@jogos_bp.route("/contato")
def contato():
    return render_template("contato.html")


# --- CATEGORIAS ---
@jogos_bp.route("/categorias")
def listar_categorias():
    return categorias_controller.listar_categorias()

@jogos_bp.route("/categorias/adicionar", methods=["GET", "POST"])
def adicionar_categoria():
    return categorias_controller.adicionar_categoria()

@jogos_bp.route("/categorias/remover/<int:id>", methods=["POST"])
def remover_categoria(id):
    return categorias_controller.remover_categoria(id)

@jogos_bp.route("/categorias/editar/<int:id>", methods=["POST"])
def editar_categoria(id):
    return categorias_controller.editar_categoria(id)


# --- USUÁRIOS (admin) ---
@jogos_bp.route("/usuarios")
def listar_usuarios():
    return usuarios_admin_controller.listar_usuarios()

@jogos_bp.route("/usuarios/tornar_admin/<email>", methods=["POST"])
def tornar_admin(email):
    return usuarios_admin_controller.tornar_admin(email)

@jogos_bp.route("/usuarios/remover_admin/<email>", methods=["POST"])
def remover_admin(email):
    return usuarios_admin_controller.remover_admin(email)

@jogos_bp.route("/usuarios/excluir/<email>", methods=["POST"])
def excluir_usuario(email):
    return usuarios_admin_controller.excluir_usuario(email)
