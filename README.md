# 📚 Biblioteca Universitária - Sistema de Gestão

Sistema de gestão de empréstimos de livros desenvolvido em Python seguindo arquitetura MVC com persistência em MongoDB.

## 👥 Integrantes

- RICARDO WAGNER MORI MOREIRA
- PEDRO HENRIQUE DA SILVA
- DOUGLAS KENJI MATSUMOTO
- VICTOR HUGO RODRIGUES DE OLIVEIRA
- VICTOR HUGO SILVA GARCIA

**Professor:** DACIO

---

## 🚀 Instalação e Configuração

### Pré-requisitos

1. **Python 3.8+** instalado
2. **MongoDB** instalado e rodando

### Instalação do MongoDB

#### Windows:
```bash
# Baixar e instalar via Chocolatey
choco install mongodb

# Ou baixar manualmente de: https://www.mongodb.com/try/download/community
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

#### macOS:
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb/brew/mongodb-community
```

### Instalação das Dependências Python

```bash
# Instalar dependências
pip install -r requirements.txt
```

### Verificar Instalação

```bash
# Testar conexão com MongoDB
python test_mongodb.py
```

---

## 🎯 Como Usar

### 1. Iniciar a Aplicação

```bash
python src/main.py
```

A aplicação estará disponível em: **http://localhost:8000**

### 2. Funcionalidades Disponíveis

#### 📖 **Gerenciamento de Livros**
- Listar todos os livros
- Adicionar novos livros
- Visualizar status de disponibilidade

#### 👥 **Gerenciamento de Usuários**
- Listar usuários cadastrados
- Cadastrar novos usuários (Estudantes/Professores/Funcionários)

#### 🔄 **Sistema de Empréstimos**
- Realizar empréstimos
- Listar empréstimos ativos
- Controlar devoluções

### 3. Interface Web

- **Design responsivo** com gradientes modernos
- **Efeitos de foco** interativos (cards se destacam no hover)
- **Tipografia elegante** (Playfair Display + Poppins)
- **Ícones emoji** para melhor identificação

---

## 🏗️ Arquitetura

```
biblioteca_universitaria/
├── config/
│   ├── database.py          # Configuração MongoDB
│   └── __init__.py
├── Model/
│   └── model.py            # Classes de dados + DB Manager
├── Controller/
│   └── controller.py       # Lógica de negócio
├── View_and_Interface/
│   ├── *.html             # Templates web
│   └── view.py            # Servidor HTTP
├── src/
│   └── main.py            # Ponto de entrada
└── tests/                 # Testes TDD
```

### 🗄️ Banco de Dados

**Coleções MongoDB:**
- `usuarios` - Dados dos usuários
- `livros` - Catálogo de livros
- `emprestimos` - Histórico de empréstimos

**Dados de exemplo** são inseridos automaticamente na primeira execução.

---

## 🧪 Testes

```bash
# Executar todos os testes
pytest tests/

# Com cobertura
pytest --cov=src tests/
```

---

## 🔧 Configuração Avançada

### Variáveis de Ambiente

O sistema usa as seguintes configurações padrão:

```python
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=biblioteca_universitaria
COLLECTION_USERS=usuarios
COLLECTION_BOOKS=livros
COLLECTION_LOANS=emprestimos
```

Para alterar, defina variáveis de ambiente antes de executar:

```bash
export MONGODB_URI="mongodb://localhost:27017/"
export DATABASE_NAME="minha_biblioteca"
python src/main.py
```

---

## 📊 Funcionalidades Técnicas

- ✅ **Persistência completa** em MongoDB
- ✅ **Arquitetura MVC** bem definida
- ✅ **Interface web moderna** com efeitos visuais
- ✅ **Validação de dados** e tratamento de erros
- ✅ **Geração automática de IDs únicos**
- ✅ **Controle de disponibilidade** de livros
- ✅ **Histórico completo** de empréstimos

---

## 🐛 Troubleshooting

### Erro de Conexão MongoDB
```
❌ Erro ao conectar ao MongoDB. Verifique se o MongoDB está rodando.
```

**Soluções:**
1. Verificar se MongoDB está instalado: `mongod --version`
2. Iniciar o serviço: `sudo systemctl start mongodb` (Linux)
3. Verificar se a porta 27017 está livre
4. Testar conexão: `python test_mongodb.py`

### Porta 8000 Ocupada
```
OSError: [Errno 48] Address already in use
```

**Solução:**
```bash
# Matar processos na porta 8000
sudo lsof -ti:8000 | xargs kill -9
# Ou usar outra porta
```

---

## 📝 Desenvolvimento

Para contribuir com o projeto:

1. Criar branch: `git checkout -b feature/nova-funcionalidade`
2. Fazer commits seguindo TDD
3. Testar todas as funcionalidades
4. Fazer pull request

---

## 📄 Licença

Este projeto foi desenvolvido como trabalho acadêmico para a disciplina de Desenvolvimento de Software.
