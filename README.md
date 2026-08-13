# 💍 WeddingHub API

API REST para gerenciamento de casamentos, convidados, presentes, pagamentos e mensagens.

O projeto foi desenvolvido com **Django** e **Django REST Framework**, utilizando autenticação JWT, PostgreSQL, Docker, Gunicorn e testes automatizados.

---

## 🚀 Funcionalidades

- 👤 Cadastro e gerenciamento de usuários
- 🔐 Autenticação com JWT
- 💒 Gerenciamento de casamentos
- 👨‍👩‍👧 Gerenciamento de convidados
- 📩 Controle de RSVP
- 🎁 Lista e reservas de presentes
- 💳 Registro e gerenciamento de pagamentos
- 💌 Livro de visitas
- 📊 Dashboard com estatísticas
- 🔎 Filtros, busca e ordenação
- 📚 Documentação automática com Swagger/OpenAPI
- 🧪 Testes automatizados
- 🐳 Docker e Docker Compose
- ⚙️ Integração contínua com GitHub Actions

---

# 🛠️ Tecnologias

- Python 3.11
- Django 5.2
- Django REST Framework
- PostgreSQL 17
- Docker
- Docker Compose
- Gunicorn
- SimpleJWT
- drf-spectacular
- django-filter
- django-cors-headers
- WhiteNoise
- Pillow
- GitHub Actions

---

# 📂 Estrutura do Projeto

```text
WeddingHub/
│
├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── analytics/
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── gifts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── guestbook/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── guests/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── payments/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── wedding/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md