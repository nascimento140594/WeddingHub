# 💍 WeddingHub API

Uma plataforma completa para gerenciamento de casamentos desenvolvida com Django e Django REST Framework.

---

# 🚀 Funcionalidades

- Cadastro de usuários
- Autenticação JWT
- Cadastro de casamento
- Gerenciamento de convidados
- RSVP
- Lista de presentes
- Pagamentos
- Livro de mensagens
- Dashboard
- Swagger
- Testes Automatizados

---

# 🛠 Tecnologias

- Python 3.11
- Django 5.2
- Django REST Framework
- SimpleJWT
- drf-spectacular
- SQLite
- django-filter
- WhiteNoise
- Pillow

---

# 📂 Estrutura

```text
WeddingHub/
│
├── accounts/
├── analytics/
├── config/
├── gifts/
├── guestbook/
├── guests/
├── payments/
├── wedding/
├── manage.py
├── requirements.txt
└── README.md
```

---

# 🔐 Autenticação

Obter Token

```http
POST /api/token/
```

Atualizar Token

```http
POST /api/token/refresh/
```

Header

```text
Authorization: Bearer SEU_TOKEN
```

---

# 📚 Documentação

Swagger

```text
/api/docs/
```

Schema

```text
/api/schema/
```

---

# 📦 Instalação

Clone o projeto

```bash
git clone https://github.com/nascimento140594/WeddingHub.git
```

Entre na pasta

```bash
cd WeddingHub
```

Crie o ambiente virtual

```bash
python -m venv .venv
```

Ative

Windows

```bash
.venv\Scripts\activate
```

Linux

```bash
source .venv/bin/activate
```

Instale as dependências

```bash
pip install -r requirements.txt
```

Execute as migrações

```bash
python manage.py migrate
```

Inicie o servidor

```bash
python manage.py runserver
```

---

# 🧪 Testes

Executar todos os testes

```bash
python manage.py test
```

Resultado atual

```text
39 testes automatizados

Todos passando ✅
```

---

# 📊 Apps

## Accounts

- Cadastro
- Perfil
- JWT

## Wedding

- Casamento
- Configuração

## Guests

- RSVP
- Convidados

## Gifts

- Lista de presentes

## Payments

- Pagamentos

## Guestbook

- Mensagens

## Analytics

- Dashboard

---

# 👨‍💻 Autor

Matheus Araújo Nascimento

GitHub:

https://github.com/nascimento140594

---

⭐ Se este projeto foi útil, deixe uma estrela no repositório.
