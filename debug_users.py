#!/usr/bin/env python3
"""
Script para debugar a listagem de usuários
"""
from Model.model import db_manager

def debug_listar_usuarios():
    """Debug da listagem de usuários"""
    print("=== DEBUG LISTAGEM DE USUÁRIOS ===")

    # Conectar ao banco
    if not db_manager.connect():
        print("❌ Falha ao conectar ao banco")
        return

    try:
        # Buscar usuários
        usuarios = db_manager.get_usuarios()
        print(f"Encontrados {len(usuarios)} usuários no banco:")

        for i, usuario in enumerate(usuarios, 1):
            print(f"\n--- Usuário {i} ---")
            print(f"  Objeto: {usuario}")
            print(f"  Tipo do objeto: {type(usuario)}")
            print(f"  ID: '{usuario.id}' (tipo: {type(usuario.id)})")
            print(f"  Name: '{usuario.name}' (tipo: {type(usuario.name)})")
            print(f"  Email: '{usuario.email}' (tipo: {type(usuario.email)})")
            print(f"  Type: '{usuario.type}' (tipo: {type(usuario.type)})")

            # Verificar se algum campo está vazio
            campos_vazios = []
            if not usuario.id or usuario.id == "":
                campos_vazios.append("id")
            if not usuario.name or usuario.name == "":
                campos_vazios.append("name")
            if not usuario.email or usuario.email == "":
                campos_vazios.append("email")
            if not usuario.type or usuario.type == "":
                campos_vazios.append("type")

            if campos_vazios:
                print(f"  ATENCAO: Campos vazios: {campos_vazios}")
            else:
                print("  SUCESSO: Todos os campos preenchidos")

    except Exception as e:
        print(f"ERRO: Erro ao debugar usuários: {e}")
        import traceback
        traceback.print_exc()

    finally:
        db_manager.disconnect()

if __name__ == "__main__":
    debug_listar_usuarios()
