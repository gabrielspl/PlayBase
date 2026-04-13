# dao.py
import os
import mysql.connector
from .models import Jogo, Usuario
from werkzeug.security import check_password_hash

# ----------------- CLASSE JOGODAO -----------------
class JogoDAO:
    def __init__(self):
        self.db_config = {
            'host': os.getenv("MYSQL_HOST"),
            'user': os.getenv("MYSQL_USER"),
            'password': os.getenv("MYSQL_PASSWORD"),
            'database': os.getenv("MYSQL_DATABASE"),
            'port': int(os.getenv("MYSQL_PORT"))
        }

    def __get_connection(self):
        return mysql.connector.connect(**self.db_config)

    def carregar_jogos(self):
        conn = self.__get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT j.id, j.nome, j.desenvolvedora, j.dataLancamento, j.genero, j.sinopse, 
                    j.plataformas, j.imagem, j.categoria_id,
                    j.tag_lancamento, j.tag_destaque, j.tag_promocao,
                    c.nome AS categoria_nome
                FROM jogos j
                JOIN categorias c ON j.categoria_id = c.id
            """)
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def salvar_jogo(self, jogo):
        sql = """INSERT INTO jogos
                (nome, desenvolvedora, dataLancamento, genero, sinopse, plataformas, imagem, categoria_id,
                 tag_lancamento, tag_destaque, tag_promocao)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        valores = [
            jogo.nome, jogo.desenvolvedora, jogo.dataLancamento, jogo.genero,
            jogo.sinopse, jogo.plataformas, jogo.imagem, jogo.categoria_id,
            jogo.tag_lancamento, jogo.tag_destaque, jogo.tag_promocao
        ]
        conn = self.__get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, valores)
            conn.commit()
            jogo.id = cursor.lastrowid
            return jogo.id
        finally:
            cursor.close()
            conn.close()

    def buscar_jogo_por_id(self, id_jogo):
        conn = self.__get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM jogos WHERE id=%s", [id_jogo])
            linha = cursor.fetchone()
            if linha:
                return Jogo(
                    nome=linha["nome"],
                    desenvolvedora=linha["desenvolvedora"],
                    dataLancamento=linha["dataLancamento"],
                    genero=linha["genero"],
                    sinopse=linha["sinopse"],
                    plataformas=linha["plataformas"],
                    id=linha["id"],
                    imagem=linha["imagem"],
                    categoria_id=linha["categoria_id"],
                    tag_lancamento=linha["tag_lancamento"],
                    tag_destaque=linha["tag_destaque"],
                    tag_promocao=linha["tag_promocao"]
                )
            return None
        finally:
            cursor.close()
            conn.close()

    def atualizar_jogo(self, jogo):
        sql = """UPDATE jogos
                 SET nome=%s, desenvolvedora=%s, dataLancamento=%s, genero=%s, sinopse=%s,
                     plataformas=%s, imagem=%s, categoria_id=%s,
                     tag_lancamento=%s, tag_destaque=%s, tag_promocao=%s
                 WHERE id=%s"""
        valores = [
            jogo.nome, jogo.desenvolvedora, jogo.dataLancamento, jogo.genero,
            jogo.sinopse, jogo.plataformas, jogo.imagem, jogo.categoria_id,
            jogo.tag_lancamento, jogo.tag_destaque, jogo.tag_promocao,
            jogo.id
        ]
        conn = self.__get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, valores)
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def remover_jogo(self, id_jogo):
        conn = self.__get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM jogos WHERE id=%s", [id_jogo])
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def buscar_jogos_por_nome(self, termo):
        conn = self.__get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            consulta = """
                SELECT j.id, j.nome, j.desenvolvedora, j.dataLancamento, j.genero, j.sinopse,
                    j.plataformas, j.imagem, j.categoria_id, c.nome AS categoria_nome,
                    j.tag_lancamento, j.tag_destaque, j.tag_promocao
                FROM jogos j
                JOIN categorias c ON j.categoria_id = c.id
                WHERE j.nome LIKE %s
            """
            cursor.execute(consulta, [f"%{termo}%"])
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()


# ----------------- CLASSE USUARIODAO -----------------
class UsuarioDAO:
    def __init__(self):
        self.db_config = {
            'host': os.getenv("MYSQL_HOST"),
            'user': os.getenv("MYSQL_USER"),
            'password': os.getenv("MYSQL_PASSWORD"),
            'database': os.getenv("MYSQL_DATABASE"),
            'port': int(os.getenv("MYSQL_PORT"))
        }

    def __get_connection(self):
        return mysql.connector.connect(**self.db_config)

    def adicionar_usuario(self, usuario):
        if self.verificar_cadastrado(usuario.email):
            return "email"
        sql = "INSERT INTO usuarios(nome,email,senha,foto,is_admin) VALUES (%s, %s, %s, %s, %s)"
        valores = [usuario.nome, usuario.email, usuario.senha, usuario.foto, usuario.is_admin]
        conn = self.__get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, valores)
            conn.commit()
            return True
        finally:
            cursor.close()
            conn.close()

    def verificar_cadastrado(self, email):
        conn = self.__get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM usuarios WHERE email=%s", [email])
            return cursor.fetchone() is not None
        finally:
            cursor.close()
            conn.close()

    def verificar_login(self, usuario):
        conn = self.__get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM usuarios WHERE email=%s", [usuario.email])
            linha = cursor.fetchone()
            if not linha:
                return None
            if not check_password_hash(linha["senha"], usuario.senha):
                return "senhaErrada"
            return "senhaCorreta"
        finally:
            cursor.close()
            conn.close()

    def buscar_nome(self, email):
        conn = self.__get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT nome FROM usuarios WHERE email=%s", [email])
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def buscar_usuario(self, email):
        conn = self.__get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM usuarios WHERE email=%s", [email])
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def listar_usuarios(self):
        conn = self.__get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT email, nome, foto, is_admin FROM usuarios ORDER BY nome")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def definir_admin(self, email, valor):
        conn = self.__get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE usuarios SET is_admin = %s WHERE email = %s", [valor, email])
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def excluir_usuario(self, email):
        conn = self.__get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM usuarios WHERE email = %s", [email])
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def atualizar_usuario(self, nome, senha, foto, email):
        sql = "UPDATE usuarios SET nome=%s, senha=%s, foto=%s WHERE email=%s"
        conn = self.__get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, [nome, senha, foto, email])
            conn.commit()
        finally:
            cursor.close()
            conn.close()


    def salvar_token_reset(self, email, token):
        conn = self.__get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE usuarios SET reset_token=%s WHERE email=%s",
                [token, email]
            )
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def buscar_usuario_por_token(self, token):
        conn = self.__get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM usuarios WHERE reset_token=%s", [token])
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def atualizar_senha(self, email, nova_senha_hash):
        conn = self.__get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE usuarios SET senha=%s, reset_token=NULL WHERE email=%s",
                [nova_senha_hash, email]
            )
            conn.commit()
        finally:
            cursor.close()
            conn.close()



class CategoriaDAO:
    def __init__(self):
        self.db_config = {
            'host': os.getenv("MYSQL_HOST"),
            'user': os.getenv("MYSQL_USER"),
            'password': os.getenv("MYSQL_PASSWORD"),
            'database': os.getenv("MYSQL_DATABASE"),
            'port': int(os.getenv("MYSQL_PORT"))
        }

    def __get_connection(self):
        return mysql.connector.connect(**self.db_config)

    def listar_categorias(self):
        conn = self.__get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM categorias")
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def adicionar_categoria(self, nome):
        conn = self.__get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO categorias(nome) VALUES (%s)", [nome])
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def remover_categoria(self, id):
        conn = self.__get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM categorias WHERE id=%s", [id])
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def atualizar_categoria(self, id, nome):
        conn = self.__get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE categorias SET nome=%s WHERE id=%s", [nome, id])
            conn.commit()
        finally:
            cursor.close()
            conn.close()
