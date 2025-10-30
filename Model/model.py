from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional, List
from config.database import db_config


@dataclass
class User:
    id: str
    name: str
    email: str
    type: str

    def to_dict(self):
        """Converte o objeto para dicionário (para MongoDB)"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        """Cria um objeto User a partir de um dicionário (do MongoDB)"""
        return cls(**data)


@dataclass
class Book:
    id: str
    title: str
    author: str
    isbn: str
    available: bool

    def to_dict(self):
        """Converte o objeto para dicionário (para MongoDB)"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        """Cria um objeto Book a partir de um dicionário (do MongoDB)"""
        return cls(**data)


@dataclass
class Loan:
    id: str
    user_id: str
    book_id: str
    loan_date: datetime
    return_date: Optional[datetime] = None

    def to_dict(self):
        """Converte o objeto para dicionário (para MongoDB)"""
        data = asdict(self)
        # Converter datetime para string ISO para MongoDB
        data['loan_date'] = self.loan_date.isoformat()
        if self.return_date:
            data['return_date'] = self.return_date.isoformat()
        return data

    @classmethod
    def from_dict(cls, data):
        """Cria um objeto Loan a partir de um dicionário (do MongoDB)"""
        # Converter strings ISO de volta para datetime
        data['loan_date'] = datetime.fromisoformat(data['loan_date'])
        if data.get('return_date'):
            data['return_date'] = datetime.fromisoformat(data['return_date'])
        return cls(**data)


class DatabaseManager:
    """Gerenciador do banco de dados MongoDB"""

    def __init__(self):
        self.connected = False

    def connect(self):
        """Conecta ao banco de dados"""
        self.connected = db_config.connect()
        if self.connected:
            self.initialize_sample_data()
        return self.connected

    def disconnect(self):
        """Desconecta do banco de dados"""
        db_config.disconnect()
        self.connected = False

    def initialize_sample_data(self):
        """Inicializa o banco com dados de exemplo se estiver vazio"""
        try:
            # Verificar se já existem dados
            users_count = db_config.users_collection.count_documents({})
            books_count = db_config.books_collection.count_documents({})
            loans_count = db_config.loans_collection.count_documents({})

            if users_count == 0:
                # Dados de exemplo para usuários
                sample_users = [
                    User("u1", "João Silva", "joao@email.com", "Estudante"),
                    User("u2", "Maria Santos", "maria@email.com", "Professor"),
                    User("u3", "Pedro Costa", "pedro@email.com", "Estudante")
                ]

                for user in sample_users:
                    db_config.users_collection.insert_one(user.to_dict())
                print("✅ Dados de exemplo de usuários inseridos")

            if books_count == 0:
                # Dados de exemplo para livros
                sample_books = [
                    Book("b1", "Python para Iniciantes", "Alice Brown", "978-1234567890", True),
                    Book("b2", "Algoritmos e Estruturas de Dados", "Bob Wilson", "978-0987654321", True),
                    Book("b3", "Banco de Dados Relacionais", "Carol Davis", "978-1122334455", False)
                ]

                for book in sample_books:
                    db_config.books_collection.insert_one(book.to_dict())
                print("✅ Dados de exemplo de livros inseridos")

            if loans_count == 0:
                # Dados de exemplo para empréstimos
                sample_loans = [
                    Loan("l1", "u1", "b1", datetime(2024, 1, 10)),
                    Loan("l2", "u1", "b2", datetime(2024, 1, 15))
                ]

                for loan in sample_loans:
                    db_config.loans_collection.insert_one(loan.to_dict())
                print("✅ Dados de exemplo de empréstimos inseridos")

        except Exception as e:
            print(f"❌ Erro ao inicializar dados de exemplo: {e}")

    def adicionar_usuario(self, user: User):
        """Adiciona um novo usuário ao banco de dados"""
        try:
            result = db_config.users_collection.insert_one(user.to_dict())
            print(f"✅ Usuário {user.name} adicionado com ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            print(f"❌ Erro ao adicionar usuário: {e}")
            return None

    def adicionar_livro(self, book: Book):
        """Adiciona um novo livro ao banco de dados"""
        try:
            result = db_config.books_collection.insert_one(book.to_dict())
            print(f"✅ Livro '{book.title}' adicionado com ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            print(f"❌ Erro ao adicionar livro: {e}")
            return None

    def adicionar_emprestimo(self, loan: Loan):
        """Adiciona um novo empréstimo ao banco de dados"""
        try:
            # Verificar se o livro está disponível
            book = self.get_livro_por_id(loan.book_id)
            if book and not book.available:
                print(f"❌ Livro '{book.title}' não está disponível para empréstimo")
                return None

            result = db_config.loans_collection.insert_one(loan.to_dict())

            # Atualizar disponibilidade do livro
            if book:
                db_config.books_collection.update_one(
                    {"id": loan.book_id},
                    {"$set": {"available": False}}
                )
                print(f"✅ Livro '{book.title}' marcado como emprestado")

            print(f"✅ Empréstimo {loan.id} registrado com ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            print(f"❌ Erro ao adicionar empréstimo: {e}")
            return None

    def get_usuarios(self) -> List[User]:
        """Retorna lista de todos os usuários"""
        try:
            users_data = list(db_config.users_collection.find())
            return [User.from_dict(user_data) for user_data in users_data]
        except Exception as e:
            print(f"❌ Erro ao buscar usuários: {e}")
            return []

    def get_livros(self) -> List[Book]:
        """Retorna lista de todos os livros"""
        try:
            books_data = list(db_config.books_collection.find())
            return [Book.from_dict(book_data) for book_data in books_data]
        except Exception as e:
            print(f"❌ Erro ao buscar livros: {e}")
            return []

    def get_emprestimos(self) -> List[Loan]:
        """Retorna lista de todos os empréstimos"""
        try:
            loans_data = list(db_config.loans_collection.find())
            return [Loan.from_dict(loan_data) for loan_data in loans_data]
        except Exception as e:
            print(f"❌ Erro ao buscar empréstimos: {e}")
            return []

    def get_livros_disponiveis(self) -> List[Book]:
        """Retorna lista de livros disponíveis"""
        try:
            books_data = list(db_config.books_collection.find({"available": True}))
            return [Book.from_dict(book_data) for book_data in books_data]
        except Exception as e:
            print(f"❌ Erro ao buscar livros disponíveis: {e}")
            return []

    def get_usuario_por_id(self, user_id: str) -> Optional[User]:
        """Busca um usuário por ID"""
        try:
            user_data = db_config.users_collection.find_one({"id": user_id})
            return User.from_dict(user_data) if user_data else None
        except Exception as e:
            print(f"❌ Erro ao buscar usuário {user_id}: {e}")
            return None

    def get_livro_por_id(self, book_id: str) -> Optional[Book]:
        """Busca um livro por ID"""
        try:
            book_data = db_config.books_collection.find_one({"id": book_id})
            return Book.from_dict(book_data) if book_data else None
        except Exception as e:
            print(f"❌ Erro ao buscar livro {book_id}: {e}")
            return None

    def get_emprestimo_por_id(self, loan_id: str) -> Optional[Loan]:
        """Busca um empréstimo por ID"""
        try:
            loan_data = db_config.loans_collection.find_one({"id": loan_id})
            return Loan.from_dict(loan_data) if loan_data else None
        except Exception as e:
            print(f"❌ Erro ao buscar empréstimo {loan_id}: {e}")
            return None

    def get_emprestimos_por_usuario(self, user_id: str) -> List[Loan]:
        """Retorna empréstimos de um usuário específico"""
        try:
            loans_data = list(db_config.loans_collection.find({"user_id": user_id}))
            return [Loan.from_dict(loan_data) for loan_data in loans_data]
        except Exception as e:
            print(f"❌ Erro ao buscar empréstimos do usuário {user_id}: {e}")
            return []

    def get_emprestimos_por_livro(self, book_id: str) -> List[Loan]:
        """Retorna empréstimos de um livro específico"""
        try:
            loans_data = list(db_config.loans_collection.find({"book_id": book_id}))
            return [Loan.from_dict(loan_data) for loan_data in loans_data]
        except Exception as e:
            print(f"❌ Erro ao buscar empréstimos do livro {book_id}: {e}")
            return []

    def devolver_livro(self, loan_id: str) -> bool:
        """Marca um empréstimo como devolvido"""
        try:
            # Buscar o empréstimo
            loan = self.get_emprestimo_por_id(loan_id)
            if not loan:
                print(f"❌ Empréstimo {loan_id} não encontrado")
                return False

            if loan.return_date:
                print(f"⚠️ Empréstimo {loan_id} já foi devolvido")
                return False

            # Atualizar empréstimo com data de devolução
            return_date = datetime.now()
            result = db_config.loans_collection.update_one(
                {"id": loan_id},
                {"$set": {"return_date": return_date.isoformat()}}
            )

            if result.modified_count > 0:
                # Atualizar disponibilidade do livro
                db_config.books_collection.update_one(
                    {"id": loan.book_id},
                    {"$set": {"available": True}}
                )

                # Buscar o livro para mostrar o nome
                book = self.get_livro_por_id(loan.book_id)
                book_title = book.title if book else "Livro desconhecido"

                print(f"✅ Livro '{book_title}' devolvido com sucesso")
                return True
            else:
                print(f"❌ Falha ao atualizar empréstimo {loan_id}")
                return False

        except Exception as e:
            print(f"❌ Erro ao devolver livro: {e}")
            return False


# Instância global do gerenciador de banco de dados
db_manager = DatabaseManager()


# Funções de compatibilidade (mantém a mesma interface do código existente)
def adicionar_usuario(user: User):
    """Adiciona um novo usuário ao sistema"""
    return db_manager.adicionar_usuario(user)


def adicionar_livro(book: Book):
    """Adiciona um novo livro ao sistema"""
    return db_manager.adicionar_livro(book)


def adicionar_emprestimo(loan: Loan):
    """Adiciona um novo empréstimo ao sistema"""
    return db_manager.adicionar_emprestimo(loan)


def get_usuarios() -> List[User]:
    """Retorna lista de todos os usuários"""
    return db_manager.get_usuarios()


def get_livros() -> List[Book]:
    """Retorna lista de todos os livros"""
    return db_manager.get_livros()


def get_emprestimos() -> List[Loan]:
    """Retorna lista de todos os empréstimos"""
    return db_manager.get_emprestimos()


def get_livros_disponiveis() -> List[Book]:
    """Retorna lista de livros disponíveis"""
    return db_manager.get_livros_disponiveis()


def get_emprestimos_por_usuario(user_id: str) -> List[Loan]:
    """Retorna empréstimos de um usuário específico"""
    return db_manager.get_emprestimos_por_usuario(user_id)


def get_emprestimos_por_livro(book_id: str) -> List[Loan]:
    """Retorna empréstimos de um livro específico"""
    return db_manager.get_emprestimos_por_livro(book_id)


def devolver_livro(loan_id: str) -> bool:
    """Marca um empréstimo como devolvido"""
    return db_manager.devolver_livro(loan_id)
