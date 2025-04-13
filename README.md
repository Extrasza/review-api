# 📚 REKT Review API

## Descrição

A **REKT Review API** é uma API RESTful para gerenciamento de reviews de jogos. A API permite:

- Enviar avaliações de jogos com nota e texto;
- Consultar reviews por nome do jogo;
- Curtir (like) uma review existente;
- Listar as 20 reviews mais recentes.

A API é construída com Python, Flask e OpenAPI 3. A persistência é feita via SQLite.

---

## 🚀 Como Executar

### ✅ Requisitos

- Python 3.8+
- Pip
- Docker

### 🔧 Instalação

1. Clone este repositório:

```bash
git clone https://github.com/extrasza/rekt-review-api.git
cd rekt-review-api
```
2. Instale as dependencias:

```bash
pip install -r requirements.txt
```

### 3. Utilizando Containers
```bash
docker build -t review-api .
docker run -p 5001:5001 review-api
```
Este comando faz com que a aplicação esteja disponível no navegador, acessível pelo endereço http://localhost:5001/
