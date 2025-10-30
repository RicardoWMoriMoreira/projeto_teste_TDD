#!/usr/bin/env python3
"""
Script para verificar diretamente os documentos de usuários no MongoDB
"""
from config.database import db_config

def check_mongo_users():
    """Verifica todos os documentos de usuários no MongoDB"""
    print("=== VERIFICANDO USUÁRIOS NO MONGODB ===")

    # Conectar ao banco
    if not db_config.connect():
        print("ERRO: Falha ao conectar ao banco")
        return

    try:
        # Buscar todos os documentos da coleção usuários
        users_collection = db_config.users_collection
        all_users = list(users_collection.find())

        print(f"Encontrados {len(all_users)} documentos na coleção 'usuarios':")

        for i, user_doc in enumerate(all_users, 1):
            print(f"\n--- Documento {i} ---")
            print(f"  _id: {user_doc.get('_id')}")
            print(f"  id: '{user_doc.get('id', 'CAMPO AUSENTE')}'")
            print(f"  name: '{user_doc.get('name', 'CAMPO AUSENTE')}'")
            print(f"  email: '{user_doc.get('email', 'CAMPO AUSENTE')}'")
            print(f"  type: '{user_doc.get('type', 'CAMPO AUSENTE')}'")

            # Verificar campos obrigatórios
            campos_ausentes = []
            if 'id' not in user_doc or not user_doc.get('id'):
                campos_ausentes.append('id')
            if 'name' not in user_doc or not user_doc.get('name'):
                campos_ausentes.append('name')
            if 'email' not in user_doc or not user_doc.get('email'):
                campos_ausentes.append('email')
            if 'type' not in user_doc or not user_doc.get('type'):
                campos_ausentes.append('type')

            if campos_ausentes:
                print(f"  ATENCAO: Campos ausentes/vazios: {campos_ausentes}")
            else:
                print("  SUCESSO: Todos os campos preenchidos")

            # Mostrar documento completo
            print(f"  Documento completo: {user_doc}")

    except Exception as e:
        print(f"ERRO: Erro ao verificar usuários: {e}")
        import traceback
        traceback.print_exc()

    finally:
        db_config.disconnect()

if __name__ == "__main__":
    check_mongo_users()
