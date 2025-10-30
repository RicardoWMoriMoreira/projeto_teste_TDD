from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: str
    name: str
    email: str
    type: str


@dataclass
class Book:
    id: str
    title: str
    author: str
    isbn: str
    available: bool


@dataclass
class Loan:
    id: str
    user_id: str
    book_id: str
    loan_date: datetime
    return_date: Optional[datetime] = None


# Dados globais para armazenar informações (seguindo padrão do projeto de referência)
users = []
books = []
loans = []

# Dados de exemplo
users.append(User("u1", "João Silva", "joao@email.com", "Estudante"))
users.append(User("u2", "Maria Santos", "maria@email.com", "Professor"))
users.append(User("u3", "Pedro Costa", "pedro@email.com", "Estudante"))

books.append(Book("b1", "Python para Iniciantes", "Alice Brown", "978-1234567890", True))
books.append(Book("b2", "Algoritmos e Estruturas de Dados", "Bob Wilson", "978-0987654321", True))
books.append(Book("b3", "Banco de Dados Relacionais", "Carol Davis", "978-1122334455", False))

loans.append(Loan("l1", "u1", "b1", datetime(2024, 1, 10)))
loans.append(Loan("l2", "u1", "b2", datetime(2024, 1, 15)))


def adicionar_usuario(user):
    """Adiciona um novo usuário ao sistema"""
    users.append(user)


def adicionar_livro(book):
    """Adiciona um novo livro ao sistema"""
    books.append(book)


def adicionar_emprestimo(loan):
    """Adiciona um novo empréstimo ao sistema"""
    loans.append(loan)


def get_usuarios():
    """Retorna lista de todos os usuários"""
    return users


def get_livros():
    """Retorna lista de todos os livros"""
    return books


def get_emprestimos():
    """Retorna lista de todos os empréstimos"""
    return loans


def get_livros_disponiveis():
    """Retorna lista de livros disponíveis"""
    return [book for book in books if book.available]


def get_emprestimos_por_usuario(user_id):
    """Retorna empréstimos de um usuário específico"""
    return [loan for loan in loans if loan.user_id == user_id]


def get_emprestimos_por_livro(book_id):
    """Retorna empréstimos de um livro específico"""
    return [loan for loan in loans if loan.book_id == book_id]


def devolver_livro(loan_id):
    """Marca um empréstimo como devolvido"""
    for loan in loans:
        if loan.id == loan_id:
            loan.return_date = datetime.now()
            # Atualizar disponibilidade do livro
            for book in books:
                if book.id == loan.book_id:
                    book.available = True
                    break
            break
