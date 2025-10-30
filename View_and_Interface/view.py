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
            # Filtrar apenas usuários com todos os campos preenchidos e não vazios
            todos_usuarios = controller.get_usuarios()
            usuarios_validos = []

            for u in todos_usuarios:
                # Verificar se todos os campos existem e não são vazios
                id_valido = u.id is not None and str(u.id).strip() != ""
                name_valido = u.name is not None and str(u.name).strip() != ""
                email_valido = u.email is not None and str(u.email).strip() != ""
                type_valido = u.type is not None and str(u.type).strip() != ""

                if id_valido and name_valido and email_valido and type_valido:
                    usuarios_validos.append(u)

            if not usuarios_validos:
                resposta = '<div class="no-users">Nenhum usuário cadastrado com dados completos.</div>'
            else:
                for usuario in usuarios_validos:
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
            # Filtrar apenas livros com todos os campos preenchidos
            livros_validos = [
                l for l in controller.get_livros()
                if l.id and l.title and l.author and l.isbn and
                   str(l.id).strip() and str(l.title).strip() and
                   str(l.author).strip() and str(l.isbn).strip()
            ]

            if not livros_validos:
                resposta = '<div class="no-users">Nenhum livro cadastrado com dados completos.</div>'
            else:
                for livro in livros_validos:
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
            # Filtrar apenas empréstimos com dados válidos
            emprestimos_validos = [
                e for e in controller.get_emprestimos()
                if e.id and e.user_id and e.book_id and e.loan_date and
                   str(e.id).strip() and str(e.user_id).strip() and str(e.book_id).strip()
            ]

            if not emprestimos_validos:
                resposta = '<div class="no-users">Nenhum empréstimo cadastrado com dados completos.</div>'
            else:
                for emprestimo in emprestimos_validos:
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

            # Validar que todos os campos obrigatórios estão preenchidos
            user_id = params.get("id", [""])[0].strip()
            user_name = params.get("name", [""])[0].strip()
            user_email = params.get("email", [""])[0].strip()
            user_type = params.get("type", [""])[0].strip()

            if not user_id or not user_name or not user_email or not user_type:
                self.send_response(400)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(b'{"status": "error", "message": "Todos os campos s\\u00e3o obrigat\\u00f3rios!"}')
                return

            usuario = {
                "id": user_id,
                "name": user_name,
                "email": user_email,
                "type": user_type
            }

            controller.adicionar_usuario(usuario)

            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(b'{"status": "success", "message": "Usu\\u00e1rio cadastrado com sucesso!"}')

        elif self.path == "/cadastrar_livro":
            tamanho = int(self.headers["Content-Length"])
            dados = self.rfile.read(tamanho).decode("utf-8")
            params = parse_qs(dados)

            # Validar que todos os campos obrigatórios estão preenchidos
            book_id = params.get("id", [""])[0].strip()
            book_title = params.get("title", [""])[0].strip()
            book_author = params.get("author", [""])[0].strip()
            book_isbn = params.get("isbn", [""])[0].strip()

            if not book_id or not book_title or not book_author or not book_isbn:
                self.send_response(400)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(b'{"status": "error", "message": "Todos os campos s\\u00e3o obrigat\\u00f3rios!"}')
                return

            livro = {
                "id": book_id,
                "title": book_title,
                "author": book_author,
                "isbn": book_isbn,
                "available": True
            }

            controller.adicionar_livro(livro)

            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(b'{"status": "success", "message": "Livro cadastrado com sucesso!"}')

        elif self.path == "/realizar_emprestimo":
            tamanho = int(self.headers["Content-Length"])
            dados = self.rfile.read(tamanho).decode("utf-8")
            params = parse_qs(dados)

            # Gerar ID único para empréstimo
            import uuid
            emprestimo = {
                "id": f"l{str(uuid.uuid4())[:8]}",
                "user_id": params.get("user_id", [""])[0],
                "book_id": params.get("book_id", [""])[0]
            }

            controller.realizar_emprestimo(emprestimo)

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h3>Empr\xc3\xa9stimo realizado com sucesso!</h3><a href='/menu'>Voltar ao menu</a>")
