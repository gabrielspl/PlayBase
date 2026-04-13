from flask import render_template, request, redirect, url_for, flash, session, current_app
from .dao import JogoDAO, UsuarioDAO, CategoriaDAO
from .models import Jogo, Usuario
from extensions import mail
import os
import time
import secrets
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from flask_mail import Message

# ----------------- CONTROLLER DE JOGOS -----------------
class JogosController:

    def __init__(self):
        self.__dao = JogoDAO()
        self.__categoria_dao = CategoriaDAO()

    def listar_jogos(self):
        jogos = self.__dao.carregar_jogos()
        return render_template("jogos.html", jogos=jogos)

    def cadastrar_jogo(self):
        if not session.get("usuarioLogado"):
            flash("Você precisa estar logado!", "error")
            return redirect(url_for("jogos.login"))
        
        nome = request.form.get("nome")
        desenvolvedora = request.form.get("desenvolvedora")
        dataLancamento = request.form.get("dataLancamento")
        genero = request.form.get("genero")
        sinopse = request.form.get("sinopse")
        plataformas = request.form.get("plataformas")
        categoria_id = request.form.get("categoria_id")
        arquivo = request.files.get("imagem")
        tag_lancamento = bool(request.form.get("tag_lancamento"))
        tag_destaque = bool(request.form.get("tag_destaque"))
        tag_promocao = bool(request.form.get("tag_promocao"))

        if not all([nome, desenvolvedora, dataLancamento, genero, sinopse, plataformas, categoria_id]):
            flash("Erro: Todos os campos são obrigatórios!", "error")
            return redirect(url_for("jogos.cadastrar_jogo"))

        caminho_imagem = None
        if arquivo and arquivo.filename != "":
            nome_arquivo = str(time.time()) + "_" + secure_filename(arquivo.filename)
            caminho = os.path.join("static/uploads/jogos", nome_arquivo)
            arquivo.save(caminho)
            caminho_imagem = caminho

        novo_jogo = Jogo(
            nome, desenvolvedora, dataLancamento, genero, sinopse, plataformas,
            categoria_id=categoria_id, imagem=caminho_imagem,
            tag_lancamento=tag_lancamento, tag_destaque=tag_destaque, tag_promocao=tag_promocao
        )
        self.__dao.salvar_jogo(novo_jogo)
        flash(f"Sucesso: O jogo '{nome}' foi cadastrado!", "success")
        return redirect(url_for("jogos.listar_jogos"))

    def preparar_cadastro(self):
        if not session.get("usuarioLogado"):
            flash("Você precisa estar logado!", "error")
            return redirect(url_for("jogos.login"))
        categorias = self.__categoria_dao.listar_categorias()
        return render_template("cadastrar.html", categorias=categorias)

    def preparar_edicao(self, id):
        jogo = self.__dao.buscar_jogo_por_id(id)
        categorias = self.__categoria_dao.listar_categorias()
        if not jogo:
            flash("Erro: Jogo não encontrado!", "error")
            return redirect(url_for("jogos.listar_jogos"))
        return render_template("editar.html", jogo=jogo, categorias=categorias)

    def editar_jogo(self, id):
        if not session.get("usuarioLogado"):
            flash("Você precisa estar logado!", "error")
            return redirect(url_for("jogos.login"))

        nome = request.form.get("nome")
        desenvolvedora = request.form.get("desenvolvedora")
        dataLancamento = request.form.get("data")
        genero = request.form.get("genero")
        sinopse = request.form.get("sinopse")
        plataformas = request.form.get("plataformas")
        categoria_id = request.form.get("categoria_id")
        arquivo = request.files.get("imagem")
        jogo_atual = self.__dao.buscar_jogo_por_id(id)

        if session.get("tipo") == 1:
            tag_lancamento = bool(request.form.get("tag_lancamento"))
            tag_destaque = bool(request.form.get("tag_destaque"))
            tag_promocao = bool(request.form.get("tag_promocao"))
        else:
            tag_lancamento = jogo_atual.tag_lancamento
            tag_destaque = jogo_atual.tag_destaque
            tag_promocao = jogo_atual.tag_promocao

        if arquivo and arquivo.filename != "":
            nome_arquivo = str(time.time()) + "_" + secure_filename(arquivo.filename)
            caminho = os.path.join("static/uploads/jogos", nome_arquivo)
            arquivo.save(caminho)
            caminho_imagem = caminho
        else:
            caminho_imagem = jogo_atual.imagem

        if not all([nome, desenvolvedora, dataLancamento, genero, sinopse, plataformas, categoria_id]):
            flash("Erro: Todos os campos são obrigatórios!", "error")
            return redirect(url_for("jogos.editar_jogo", id=id))

        jogo_atualizado = Jogo(
            nome, desenvolvedora, dataLancamento, genero, sinopse, plataformas,
            categoria_id=categoria_id, id=id, imagem=caminho_imagem,
            tag_lancamento=tag_lancamento, tag_destaque=tag_destaque, tag_promocao=tag_promocao
        )
        self.__dao.atualizar_jogo(jogo_atualizado)
        flash(f"Sucesso: O jogo '{nome}' foi atualizado!", "success")
        return redirect(url_for("jogos.listar_jogos"))

    def remover_jogo(self, id):
        if not session.get("usuarioLogado"):
            flash("Você precisa estar logado!", "error")
            return redirect(url_for("jogos.login"))
        self.__dao.remover_jogo(id)
        flash("Sucesso: Jogo removido com sucesso!", "success")
        return redirect(url_for("jogos.listar_jogos"))

    def buscar_jogos(self):
        termo = request.args.get("busca")
        if termo and termo.strip():
            jogos = self.__dao.buscar_jogos_por_nome(termo)
        else:
            jogos = self.__dao.carregar_jogos()
        return render_template("jogos.html", jogos=jogos, termo=termo)


# ----------------- CONTROLLER DE USUÁRIOS -----------------
class UsuariosController:

    def __init__(self):
        self.__dao = UsuarioDAO()

    def cadastro_usuario(self):
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        confirmar_senha = request.form.get("confirmar_senha")
        arquivo = request.files.get("foto")

        if not all([nome, email, senha]):
            flash("Preencha usuário, nome e senha.", "error")
            return redirect(url_for("jogos.cadastro_usuario"))

        if senha != confirmar_senha:
            flash("Senhas diferentes informadas!", "error")
            return redirect(url_for("jogos.cadastro_usuario"))

        caminho_foto = "static/uploads/usuarios/default.png"
        if arquivo and arquivo.filename != "":
            nome_arquivo = str(time.time()) + "_" + secure_filename(arquivo.filename)
            caminho = os.path.join("static/uploads/usuarios", nome_arquivo)
            arquivo.save(caminho)
            caminho_foto = caminho

        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(nome, email, senha_hash, foto=caminho_foto)
        status = self.__dao.adicionar_usuario(novo_usuario)

        if status == True:
            flash(f"{nome}, seu cadastro foi realizado com sucesso!", "success")
        elif status == "email":
            flash("Email já cadastrado!", "error")
        else:
            flash("Erro no cadastro do usuário!", "error")

        return redirect(url_for("jogos.cadastro_usuario"))

    def preparar_cadastro_usuario(self):
        return render_template("cadastro.html")

    def preparar_login(self):
        return render_template("login.html")

    def login(self):
        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario = Usuario(nome="temp", email=email, senha=senha)
        status = self.__dao.verificar_login(usuario)
        usuario = self.__dao.buscar_usuario(email)

        if status is None:
            flash("Email não cadastrado!", "error")
            return self.preparar_login()
        elif status == "senhaErrada":
            flash("Senha incorreta!", "error")
            return redirect(url_for("jogos.login"))

        if usuario.get("is_admin"):
            session["tipo"] = True

        session["usuarioLogado"] = usuario["nome"]
        session["fotoUsuario"] = usuario["foto"]
        session["usuarioLogadoEmail"] = usuario["email"]

        flash(f"{usuario['nome']}, login realizado com sucesso!", "success")
        return redirect(url_for("jogos.listar_jogos"))

    def logout(self):
        session.clear()
        flash("Logout realizado com sucesso!", "success")
        return redirect(url_for("jogos.login"))

    def preparar_edicao_usuario(self):
        email = session.get("usuarioLogadoEmail")
        usuario = self.__dao.buscar_usuario(email)
        return render_template("perfil.html", usuario=usuario)

    def editar_usuario(self):
        email = session.get("usuarioLogadoEmail")
        nome = request.form.get("nome")
        senha = request.form.get("senha")
        confirmar = request.form.get("confirmar")
        arquivo = request.files.get("foto")
        usuario = self.__dao.buscar_usuario(email)
        caminho_foto = usuario["foto"]

        if arquivo and arquivo.filename != "":
            nome_arquivo = str(time.time()) + "_" + secure_filename(arquivo.filename)
            caminho = os.path.join("static/uploads/usuarios", nome_arquivo)
            arquivo.save(caminho)
            caminho_foto = caminho

        if senha:
            if senha != confirmar:
                flash("Senhas não coincidem!", "error")
                return redirect(url_for("jogos.perfil"))
            senha = generate_password_hash(senha)
        else:
            senha = usuario["senha"]

        if not nome:
            flash("Nome não pode ser vazio!", "error")
            return redirect(url_for("jogos.perfil"))

        self.__dao.atualizar_usuario(nome, senha, caminho_foto, email)
        session["usuarioLogado"] = nome
        session["fotoUsuario"] = caminho_foto
        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for("jogos.perfil"))

    
    def preparar_esqueci_senha(self):
        return render_template("esqueci_senha.html")

    def esqueci_senha(self):
        
        email = request.form.get("email", "").strip()

        usuario = self.__dao.buscar_usuario(email)

       
        if usuario:
            token = secrets.token_urlsafe(32)
            self.__dao.salvar_token_reset(email, token)

            link = url_for("jogos.redefinir_senha", token=token, _external=True)

            msg = Message(
                subject="PlayBase — Redefinição de senha",
                sender=current_app.config["MAIL_USERNAME"],
                recipients=[email]
            )
            msg.html = f"""
            <div style="font-family:sans-serif;max-width:480px;margin:0 auto;background:#141414;
                        color:#efefef;border-radius:12px;padding:36px;border:1px solid #252525;">
                <h2 style="color:#00FF66;margin-bottom:8px;letter-spacing:-0.02em;">PLAYBASE</h2>
                <p style="color:#808080;font-size:14px;margin-bottom:24px;">Recuperação de senha</p>
                <p>Olá, <strong>{usuario['nome']}</strong>!</p>
                <p style="margin-top:12px;color:#aaa;">
                    Recebemos uma solicitação para redefinir a senha da sua conta.
                    Clique no botão abaixo para criar uma nova senha.
                    Este link expira em <strong style="color:#efefef;">30 minutos</strong>.
                </p>
                <a href="{link}"
                   style="display:inline-block;margin-top:28px;padding:13px 28px;
                          background:#00FF66;color:#000;border-radius:8px;
                          font-weight:700;text-decoration:none;letter-spacing:0.05em;
                          font-size:14px;text-transform:uppercase;">
                    Redefinir senha
                </a>
                <p style="margin-top:28px;font-size:12px;color:#555;">
                    Se você não solicitou isso, ignore este email. Sua senha não será alterada.
                </p>
            </div>
            """
            mail.send(msg)

        flash("Se este email estiver cadastrado, você receberá um link em instantes.", "info")
        return redirect(url_for("jogos.esqueci_senha"))

    def preparar_redefinir_senha(self, token):
        usuario = self.__dao.buscar_usuario_por_token(token)
        if not usuario:
            flash("Link inválido ou expirado.", "error")
            return redirect(url_for("jogos.login"))
        return render_template("redefinir_senha.html", token=token)

    def redefinir_senha(self, token):
        usuario = self.__dao.buscar_usuario_por_token(token)
        if not usuario:
            flash("Link inválido ou expirado.", "error")
            return redirect(url_for("jogos.login"))

        nova_senha = request.form.get("senha")
        confirmar = request.form.get("confirmar")

        if not nova_senha or nova_senha != confirmar:
            flash("As senhas não coincidem!", "error")
            return redirect(url_for("jogos.redefinir_senha", token=token))

        if len(nova_senha) < 6:
            flash("A senha deve ter pelo menos 6 caracteres.", "error")
            return redirect(url_for("jogos.redefinir_senha", token=token))

        self.__dao.atualizar_senha(usuario["email"], generate_password_hash(nova_senha))
        flash("Senha redefinida com sucesso! Faça login.", "success")
        return redirect(url_for("jogos.login"))


# ----------------- CONTROLLER DE GERENCIAMENTO DE USUÁRIOS -----------------
class UsuariosAdminController:

    def __init__(self):
        self.__dao = UsuarioDAO()

    def listar_usuarios(self):
        if not session.get("tipo") == 1:
            flash("Página apenas para administradores!", "error")
            return redirect(url_for("jogos.listar_jogos"))
        usuarios = self.__dao.listar_usuarios()
        return render_template("usuarios.html", usuarios=usuarios)

    def tornar_admin(self, email):
        if not session.get("tipo") == 1:
            flash("Acesso negado!", "error")
            return redirect(url_for("jogos.listar_jogos"))
        self.__dao.definir_admin(email, 1)
        flash(f"Usuário {email} agora é administrador!", "success")
        return redirect(url_for("jogos.listar_usuarios"))

    def remover_admin(self, email):
        if not session.get("tipo") == 1:
            flash("Acesso negado!", "error")
            return redirect(url_for("jogos.listar_jogos"))
        if email == session.get("usuarioLogadoEmail"):
            flash("Você não pode remover seus próprios privilégios de admin!", "error")
            return redirect(url_for("jogos.listar_usuarios"))
        self.__dao.definir_admin(email, 0)
        flash(f"Privilégios de admin removidos de {email}!", "success")
        return redirect(url_for("jogos.listar_usuarios"))

    def excluir_usuario(self, email):
        if not session.get("tipo") == 1:
            flash("Acesso negado!", "error")
            return redirect(url_for("jogos.listar_jogos"))
        if email == session.get("usuarioLogadoEmail"):
            flash("Você não pode excluir sua própria conta por aqui!", "error")
            return redirect(url_for("jogos.listar_usuarios"))
        self.__dao.excluir_usuario(email)
        flash(f"Usuário {email} excluído com sucesso!", "success")
        return redirect(url_for("jogos.listar_usuarios"))


# ----------------- CONTROLLER DE CATEGORIAS -----------------
class CategoriasController:

    def __init__(self):
        self.__dao = CategoriaDAO()

    def listar_categorias(self):
        if not session.get("tipo"):
            flash("Página apenas para administradores!", "error")
            return redirect(url_for("jogos.listar_jogos"))
        categorias = self.__dao.listar_categorias()
        return render_template("categorias.html", categorias=categorias)

    def adicionar_categoria(self):
        if not session.get("tipo"):
            flash("Página apenas para administradores!", "error")
            return redirect(url_for("jogos.listar_jogos"))
        nome = request.form.get("nome")
        if not nome:
            flash("Nome não pode ser vazio!", "error")
            return redirect(url_for("jogos.listar_categorias"))
        self.__dao.adicionar_categoria(nome)
        flash("Categoria adicionada!", "success")
        return redirect(url_for("jogos.listar_categorias"))

    def remover_categoria(self, id):
        if not session.get("tipo"):
            flash("Página apenas para administradores!", "error")
            return redirect(url_for("jogos.listar_jogos"))
        self.__dao.remover_categoria(id)
        flash("Categoria removida!", "success")
        return redirect(url_for("jogos.listar_categorias"))

    def editar_categoria(self, id):
        if not session.get("tipo"):
            flash("Página apenas para administradores!", "error")
            return redirect(url_for("jogos.listar_jogos"))
        nome = request.form.get("nome")
        if not nome:
            flash("Nome inválido!", "error")
            return redirect(url_for("jogos.listar_categorias"))
        self.__dao.atualizar_categoria(id, nome)
        flash("Categoria atualizada!", "success")
        return redirect(url_for("jogos.listar_categorias"))
