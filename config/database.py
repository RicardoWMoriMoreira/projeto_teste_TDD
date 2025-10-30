"""
Configuração do banco de dados MongoDB
"""
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class DatabaseConfig:
    def __init__(self):
        # Configurações padrão do MongoDB
        self.mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.database_name = os.getenv('DATABASE_NAME', 'biblioteca_universitaria')

        # Nomes das coleções
        self.collection_users = os.getenv('COLLECTION_USERS', 'usuarios')
        self.collection_books = os.getenv('COLLECTION_BOOKS', 'livros')
        self.collection_loans = os.getenv('COLLECTION_LOANS', 'emprestimos')

        # Cliente MongoDB
        self.client = None
        self.db = None

    def connect(self):
        """Conecta ao MongoDB"""
        try:
            self.client = MongoClient(self.mongodb_uri)
            self.db = self.client[self.database_name]

            # Testa a conexão
            self.client.admin.command('ping')
            print(f"✅ Conectado ao MongoDB: {self.database_name}")
            return True

        except ConnectionFailure:
            print("❌ Erro ao conectar ao MongoDB. Verifique se o MongoDB está rodando.")
            print("Para instalar MongoDB:")
            print("  Windows: https://www.mongodb.com/try/download/community")
            print("  Linux: sudo apt install mongodb")
            print("  macOS: brew install mongodb-community")
            return False

    def disconnect(self):
        """Desconecta do MongoDB"""
        if self.client:
            self.client.close()
            print("🔌 Desconectado do MongoDB")

    def get_collection(self, collection_name):
        """Retorna uma coleção específica"""
        if not self.db:
            raise Exception("Banco de dados não conectado. Chame connect() primeiro.")
        return self.db[collection_name]

    # Métodos específicos para cada coleção
    @property
    def users_collection(self):
        return self.get_collection(self.collection_users)

    @property
    def books_collection(self):
        return self.get_collection(self.collection_books)

    @property
    def loans_collection(self):
        return self.get_collection(self.collection_loans)

# Instância global da configuração
db_config = DatabaseConfig()
