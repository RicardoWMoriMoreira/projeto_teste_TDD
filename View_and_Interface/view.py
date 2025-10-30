from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import Controller.controller as ctl
from html import escape
from datetime import datetime


def _esc(v):
    return escape("" if v is None else str(v))


# Instância do controller
controller = ctl.Controller(login_required=False)


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
            for usuario in controller.get_usuarios():
                # Define o ícone baseado no tipo de usuário
                if usuario.type == "Professor":
                    icon = "👨‍🏫"
                elif usuario.type == "Funcionário":
                    icon = "👔"
                else:
                    icon = "👨‍🎓"

                resposta += f"""
                <div class="user-card">
                    <div class="user-icon">{icon}</div>
                    <div class="user-name">{_esc(usuario.name)}</div>
                    <div class="user-info">
                        <div class="user-info-item">
                            <span class="user-info-label">ID:</span>
                            <span class="user-info-value">{_esc(usuario.id)}</span>
                        </div>
                        <div class="user-info-item">
                            <span class="user-info-label">Email:</span>
                            <span class="user-info-value">{_esc(usuario.email)}</span>
                        </div>
                        <div class="user-info-item">
                            <span class="user-info-label">Tipo:</span>
                            <span class="user-info-value">{_esc(usuario.type)}</span>
                        </div>
                    </div>
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
            for livro in controller.get_livros():
                status = "Disponível" if livro.available else "Emprestado"
                status_class = "status-available" if livro.available else "status-borrowed"
                icon = "📚" if livro.available else "🔒"

                resposta += f"""
                <div class="book-card">
                    <div class="book-icon">{icon}</div>
                    <div class="book-title">{_esc(livro.title)}</div>
                    <div class="book-info">
                        <div class="book-info-item">
                            <span class="book-info-label">Autor:</span>
                            <span class="book-info-value">{_esc(livro.author)}</span>
                        </div>
                        <div class="book-info-item">
                            <span class="book-info-label">ISBN:</span>
                            <span class="book-info-value">{_esc(livro.isbn)}</span>
                        </div>
                        <div class="book-info-item">
                            <span class="book-info-label">Status:</span>
                            <span class="status-badge {status_class}">{status}</span>
                        </div>
                    </div>
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
            for emprestimo in controller.get_emprestimos():
                usuario = controller.get_usuario_por_id(emprestimo.user_id)
                livro = controller.get_livro_por_id(emprestimo.book_id)
                usuario_nome = usuario.name if usuario else "Usuário não encontrado"
                livro_titulo = livro.title if livro else "Livro não encontrado"
                data_devolucao = emprestimo.return_date.strftime("%d/%m/%Y") if emprestimo.return_date else "Não devolvido"
                status_class = "status-returned" if emprestimo.return_date else "status-active"
                status_text = "Devolvido" if emprestimo.return_date else "Em andamento"
                icon = "✅" if emprestimo.return_date else "📖"

                resposta += f"""
                <div class="loan-card">
                    <div class="loan-icon">{icon}</div>
                    <div class="loan-id">Empréstimo {_esc(emprestimo.id)}</div>
                    <div class="loan-info">
                        <div class="loan-info-item">
                            <span class="loan-info-label">Usuário:</span>
                            <span class="loan-info-value">{_esc(usuario_nome)}</span>
                        </div>
                        <div class="loan-info-item">
                            <span class="loan-info-label">Livro:</span>
                            <span class="loan-info-value">{_esc(livro_titulo)}</span>
                        </div>
                        <div class="loan-info-item">
                            <span class="loan-info-label">Empréstimo:</span>
                            <span class="loan-info-value">{emprestimo.loan_date.strftime("%d/%m/%Y")}</span>
                        </div>
                        <div class="loan-info-item">
                            <span class="loan-info-label">Status:</span>
                            <span class="return-status {status_class}">{status_text}</span>
                        </div>
                    </div>
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

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h3>Livro cadastrado com sucesso!</h3><a href='/menu'>Voltar ao menu</a>")

        elif self.path == "/realizar_emprestimo":
            tamanho = int(self.headers["Content-Length"])
            dados = self.rfile.read(tamanho).decode("utf-8")
            params = parse_qs(dados)

            emprestimo = {
                "id": f"l{len(controller.get_emprestimos()) + 1}",
                "user_id": params.get("user_id", [""])[0],
                "book_id": params.get("book_id", [""])[0]
            }

            controller.realizar_emprestimo(emprestimo)

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h3>Empr\xc3\xa9stimo realizado com sucesso!</h3><a href='/menu'>Voltar ao menu</a>")
