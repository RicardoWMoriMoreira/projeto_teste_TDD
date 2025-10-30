#!/usr/bin/env python3
"""
Script para debugar o HTML gerado para listagem de usuários
"""
from View_and_Interface import view as vw
from Controller.controller import Controller
from Model.model import db_manager
import re

def debug_html_usuarios():
    """Debug do HTML gerado para usuários"""
    print("=== DEBUG HTML USUÁRIOS ===")

    # Conectar ao banco
    if not db_manager.connect():
        print("ERRO: Falha ao conectar ao banco")
        return

    try:
        # Simular a geração do HTML como no view.py
        resposta = ""
        controller = Controller()
        usuarios = controller.get_usuarios()

        print(f"Processando {len(usuarios)} usuários...")

        for usuario in usuarios:
            # Define o ícone baseado no tipo de usuário
            if usuario.type == "Professor":
                icon = "[PROFESSOR]"
            elif usuario.type == "Funcionário":
                icon = "[FUNCIONARIO]"
            else:
                icon = "[ESTUDANTE]"

            # Gerar o HTML do card (igual ao view.py)
            card_html = f"""
                <div class="user-card">
                    <div class="user-icon">{icon}</div>
                    <div class="user-name">{vw._esc(usuario.name)}</div>
                    <div class="user-info">
                        <div class="user-info-item">
                            <span class="user-info-label">ID:</span>
                            <span class="user-info-value">{vw._esc(usuario.id)}</span>
                        </div>
                        <div class="user-info-item">
                            <span class="user-info-label">Email:</span>
                            <span class="user-info-value">{vw._esc(usuario.email)}</span>
                        </div>
                        <div class="user-info-item">
                            <span class="user-info-label">Tipo:</span>
                            <span class="user-info-value">{vw._esc(usuario.type)}</span>
                        </div>
                    </div>
                </div>
                """

            resposta += card_html
            print(f"\nCard para {usuario.name}:")
            print(card_html.strip())

        print(f"\nHTML final gerado ({len(resposta)} caracteres):")
        print(resposta[:500] + "..." if len(resposta) > 500 else resposta)

        # Verificar se há campos vazios no HTML
        vazio_patterns = [
            r'<span class="user-info-value"></span>',
            r'<span class="user-info-value">\s*</span>',
            r'<div class="user-name"></div>',
            r'<div class="user-name">\s*</div>'
        ]

        campos_vazios = []
        for pattern in vazio_patterns:
            matches = re.findall(pattern, resposta)
            if matches:
                campos_vazios.extend(matches)

        if campos_vazios:
            print(f"\nATENCAO: Encontrados {len(campos_vazios)} campos vazios no HTML:")
            for campo in campos_vazios[:5]:  # Mostrar apenas os primeiros 5
                print(f"  {campo}")
        else:
            print("\nSUCESSO: Nenhum campo vazio encontrado no HTML")

    except Exception as e:
        print(f"ERRO: Erro ao debugar HTML: {e}")
        import traceback
        traceback.print_exc()

    finally:
        db_manager.disconnect()

if __name__ == "__main__":
    debug_html_usuarios()
