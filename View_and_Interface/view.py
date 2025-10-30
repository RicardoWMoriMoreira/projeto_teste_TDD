from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import Controller.controller as ctl
from html import escape
from datetime import datetime


def _esc(v):
    return escape("" if v is None else str(v))


# Instância do controller
controller = ctl.Controller(login_required=False)

# Dados globais para as views
usuarios = controller.get_usuarios()
livros = controller.get_livros()
emprestimos = controller.get_emprestimos()


class BibliotecaController(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.send_response(302)
            self.send_header("Location", "/menu")
            self.end_headers()

        elif self.path == "/menu":
            with open("View_and_Interface/menu.html", "r", encoding="utf-8") as f:
                conteudo = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))

        elif self.path == "/listar_usuarios":
            resposta = ""
            for usuario in usuarios:
                resposta += f"""
                <div class="usuario">
                    <h3>{_esc(usuario.name)}</h3>
                    <p>ID: {_esc(usuario.id)}</p>
                    <p>Email: {_esc(usuario.email)}</p>
                    <p>Tipo: {_esc(usuario.type)}</p>
                </div>
                """
            with open("View_and_Interface/listar_usuarios.html", "r", encoding="utf-8") as f:
                conteudo = f.read()
            conteudo = conteudo.replace("<!--USUARIOS-->", resposta)
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))

        elif self.path == "/listar_livros":
            resposta = ""
            for livro in livros:
                status = "Disponível" if livro.available else "Emprestado"
                resposta += f"""
                <div class="livro">
                    <h3>{_esc(livro.title)}</h3>
                    <p>Autor: {_esc(livro.author)}</p>
                    <p>ISBN: {_esc(livro.isbn)}</p>
                    <p>Status: {status}</p>
                </div>
                """
            with open("View_and_Interface/listar_livros.html", "r", encoding="utf-8") as f:
                conteudo = f.read()
            conteudo = conteudo.replace("<!--LIVROS-->", resposta)
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))

        elif self.path == "/listar_emprestimos":
            resposta = ""
            for emprestimo in emprestimos:
                usuario = controller.get_usuario_por_id(emprestimo.user_id)
                livro = controller.get_livro_por_id(emprestimo.book_id)
                usuario_nome = usuario.name if usuario else "Usuário não encontrado"
                livro_titulo = livro.title if livro else "Livro não encontrado"
                data_devolucao = emprestimo.return_date.strftime("%d/%m/%Y") if emprestimo.return_date else "Não devolvido"

                resposta += f"""
                <div class="emprestimo">
                    <h3>Empréstimo {_esc(emprestimo.id)}</h3>
                    <p>Usuário: {_esc(usuario_nome)}</p>
                    <p>Livro: {_esc(livro_titulo)}</p>
                    <p>Data do empréstimo: {emprestimo.loan_date.strftime("%d/%m/%Y")}</p>
                    <p>Data de devolução: {data_devolucao}</p>
                </div>
                """
            with open("View_and_Interface/listar_emprestimos.html", "r", encoding="utf-8") as f:
                conteudo = f.read()
            conteudo = conteudo.replace("<!--EMPRESTIMOS-->", resposta)
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))

        elif self.path == "/cadastrar_usuario":
            with open("View_and_Interface/cadastrar_usuario.html", "r", encoding="utf-8") as f:
                conteudo = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))

        elif self.path == "/cadastrar_livro":
            with open("View_and_Interface/cadastrar_livro.html", "r", encoding="utf-8") as f:
                conteudo = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))

        elif self.path == "/realizar_emprestimo":
            with open("View_and_Interface/realizar_emprestimo.html", "r", encoding="utf-8") as f:
                conteudo = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(conteudo.encode("utf-8"))

    def do_POST(self):
        if self.path == "/cadastrar_usuario":
            tamanho = int(self.headers["Content-Length"])
            dados = self.rfile.read(tamanho).decode("utf-8")
            params = parse_qs(dados)

            usuario = {
                "id": params.get("id", [""])[0],
                "name": params.get("name", [""])[0],
                "email": params.get("email", [""])[0],
                "type": params.get("type", [""])[0]
            }

            controller.adicionar_usuario(usuario)
            usuarios.append(controller.get_usuario_por_id(usuario["id"]))

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h3>Usu\xc3\xa1rio cadastrado com sucesso!</h3><a href='/menu'>Voltar ao menu</a>")

        elif self.path == "/cadastrar_livro":
            tamanho = int(self.headers["Content-Length"])
            dados = self.rfile.read(tamanho).decode("utf-8")
            params = parse_qs(dados)

            livro = {
                "id": params.get("id", [""])[0],
                "title": params.get("title", [""])[0],
                "author": params.get("author", [""])[0],
                "isbn": params.get("isbn", [""])[0],
                "available": True
            }

            controller.adicionar_livro(livro)
            livros.append(controller.get_livro_por_id(livro["id"]))

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h3>Livro cadastrado com sucesso!</h3><a href='/menu'>Voltar ao menu</a>")

        elif self.path == "/realizar_emprestimo":
            tamanho = int(self.headers["Content-Length"])
            dados = self.rfile.read(tamanho).decode("utf-8")
            params = parse_qs(dados)

            emprestimo = {
                "id": f"l{len(emprestimos) + 1}",
                "user_id": params.get("user_id", [""])[0],
                "book_id": params.get("book_id", [""])[0]
            }

            controller.realizar_emprestimo(emprestimo)
            emprestimos.append(controller.get_emprestimo_por_id(emprestimo["id"]))

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h3>Empr\xc3\xa9stimo realizado com sucesso!</h3><a href='/menu'>Voltar ao menu</a>")
