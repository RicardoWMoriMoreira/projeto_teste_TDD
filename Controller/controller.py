from Model import model as md
from datetime import datetime


class Controller:
    def __init__(self, login_required=True):
        self.login_required = login_required

    def adicionar_usuario(self, usuario_data):
        """Adiciona um novo usuário"""
        novo_usuario = md.User(
            id=usuario_data["id"],
            name=usuario_data["name"],
            email=usuario_data["email"],
            type=usuario_data["type"]
        )
        md.adicionar_usuario(novo_usuario)
        return novo_usuario

    def adicionar_livro(self, livro_data):
        """Adiciona um novo livro"""
        novo_livro = md.Book(
            id=livro_data["id"],
            title=livro_data["title"],
            author=livro_data["author"],
            isbn=livro_data["isbn"],
            available=livro_data["available"]
        )
        md.adicionar_livro(novo_livro)
        return novo_livro

    def realizar_emprestimo(self, emprestimo_data):
        """Realiza um empréstimo"""
        novo_emprestimo = md.Loan(
            id=emprestimo_data["id"],
            user_id=emprestimo_data["user_id"],
            book_id=emprestimo_data["book_id"],
            loan_date=datetime.now()
        )
        md.adicionar_emprestimo(novo_emprestimo)

        # Marcar livro como indisponível
        for livro in md.books:
            if livro.id == emprestimo_data["book_id"]:
                livro.available = False
                break

        return novo_emprestimo

    def devolver_livro(self, loan_id):
        """Devolve um livro"""
        md.devolver_livro(loan_id)

    def get_usuarios(self):
        """Retorna todos os usuários"""
        return md.get_usuarios()

    def get_livros(self):
        """Retorna todos os livros"""
        return md.get_livros()

    def get_emprestimos(self):
        """Retorna todos os empréstimos"""
        return md.get_emprestimos()

    def get_livros_disponiveis(self):
        """Retorna livros disponíveis"""
        return md.get_livros_disponiveis()

    def get_emprestimos_por_usuario(self, user_id):
        """Retorna empréstimos de um usuário"""
        return md.get_emprestimos_por_usuario(user_id)

    def get_usuario_por_id(self, user_id):
        """Busca usuário por ID"""
        for usuario in md.users:
            if usuario.id == user_id:
                return usuario
        return None

    def get_livro_por_id(self, book_id):
        """Busca livro por ID"""
        for livro in md.books:
            if livro.id == book_id:
                return livro
        return None

    def get_emprestimo_por_id(self, loan_id):
        """Busca empréstimo por ID"""
        for emprestimo in md.loans:
            if emprestimo.id == loan_id:
                return emprestimo
        return None


# Classe para autenticação (seguindo padrão do projeto de referência)
class Ctrl_User(md.User):
    def __init__(self, user_id, name, email, user_type):
        super().__init__(user_id, name, email, user_type)

    def autenticar(self):
        # Implementação simples - em produção seria mais robusta
        return True
