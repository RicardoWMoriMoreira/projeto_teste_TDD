#!/usr/bin/env python3
"""
Script para testar o cadastro de usuários
"""
from Controller.controller import Controller

def test_cadastro_usuario():
    """Testa o cadastro de um usuário"""
    print("=== TESTANDO CADASTRO DE USUÁRIO ===")

    controller = Controller()

    # Dados de teste
    usuario_data = {
        "id": "u4",
        "name": "Teste Usuario",
        "email": "teste@email.com",
        "type": "Estudante"
    }

    print(f"Cadastrando usuário: {usuario_data}")

    try:
        usuario = controller.adicionar_usuario(usuario_data)
        print(f"SUCESSO: Usuário cadastrado: {usuario}")

        # Verificar se foi cadastrado corretamente
        usuarios = controller.get_usuarios()
        usuario_encontrado = None
        for u in usuarios:
            if u.id == "u4":
                usuario_encontrado = u
                break

        if usuario_encontrado:
            print(f"USUARIO ENCONTRADO: ID={usuario_encontrado.id}, Nome={usuario_encontrado.name}, Email={usuario_encontrado.email}, Tipo={usuario_encontrado.type}")

            # Verificar se todos os campos estão preenchidos
            if usuario_encontrado.id and usuario_encontrado.name and usuario_encontrado.email and usuario_encontrado.type:
                print("SUCESSO: Todos os campos estão preenchidos!")
            else:
                print("ATENCAO: Alguns campos estão vazios!")
                print(f"  ID: '{usuario_encontrado.id}'")
                print(f"  Name: '{usuario_encontrado.name}'")
                print(f"  Email: '{usuario_encontrado.email}'")
                print(f"  Type: '{usuario_encontrado.type}'")
        else:
            print("ERRO: Usuário não foi encontrado após cadastro!")

    except Exception as e:
        print(f"ERRO: Falha ao cadastrar usuário: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_cadastro_usuario()
