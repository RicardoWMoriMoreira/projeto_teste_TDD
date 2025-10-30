from View_and_Interface import view as vw
from http.server import HTTPServer
from Model.model import db_manager

def main():
    print("Sistema de Gestão de Biblioteca Universitária")
    print("Equipe 4 - Seguindo arquitetura MVC com MongoDB")
    print("=" * 50)

    # Conectar ao banco de dados
    print("🔌 Conectando ao MongoDB...")
    if not db_manager.connect():
        print("❌ Falha ao conectar ao banco de dados. Encerrando aplicação.")
        return

    try:
        print("🌐 Iniciando servidor web...")
        servidor = HTTPServer(("localhost", 8000), vw.BibliotecaController)
        print("✅ Servidor rodando em http://localhost:8000")
        print("📚 Biblioteca Universitária - Sistema Online")
        print("=" * 50)
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️  Servidor interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro no servidor: {e}")
    finally:
        print("🔌 Desconectando do banco de dados...")
        db_manager.disconnect()
        print("👋 Aplicação encerrada")

if __name__ == "__main__":
    main()
