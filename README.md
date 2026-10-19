# PokéAPI — Projeto Final de Backend Python

API REST para gerenciamento de Pokémon, construída com FastAPI, SQLAlchemy 2, PostgreSQL, Docker Compose e pytest. A organização do projeto toma como referência os padrões praticados no repositório `exercicio-m36-backend`, incluindo configuração por ambiente, testes, CI, containerização, logs e manifesto Kubernetes.

## Requisitos

- Python 3.11+ para execução local
- Docker com Docker Compose ou Podman com `podman-compose`
- Git

## Executar com containers

1. Copie `.env.example` para `.env` e defina uma senha forte em `POSTGRES_PASSWORD`.
2. Inicie os serviços com `docker compose up --build` ou `podman-compose up --build`.
3. Abra `http://localhost:8000/docs` para testar os endpoints.
4. Verifique `http://localhost:8000/health` para o health check.

O Compose inicia a API e o PostgreSQL em containers separados e mantém os dados em um volume nomeado. Não versione o arquivo `.env`.

## Executar localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL='sqlite:///./pokemon.db'
uvicorn app.main:app --reload
```

No PowerShell, use `$env:DATABASE_URL='sqlite:///./pokemon.db'`. A aplicação cria as tabelas na inicialização.

## Testes

```bash
pytest -v
```

Os testes cobrem criação, leitura, listagem, filtros, atualização, exclusão, validação, duplicidade e respostas 404. A integração contínua executa a suíte em push e pull request.

## Endpoints

| Método | Rota | Descrição | Respostas comuns |
|---|---|---|---|
| GET | `/` | Informações básicas da API | `200` |
| GET | `/health` | Health check | `200` |
| POST | `/pokemons` | Cria Pokémon | `201`, `409`, `422` |
| GET | `/pokemons` | Lista Pokémon | `200` |
| GET | `/pokemons/{pokemon_id}` | Busca por ID | `200`, `404` |
| PUT | `/pokemons/{pokemon_id}` | Atualiza campos enviados | `200`, `404`, `409`, `422` |
| DELETE | `/pokemons/{pokemon_id}` | Exclui Pokémon | `204`, `404` |

A listagem aceita `offset`, `limit`, `name` e `type`. Exemplo: `/pokemons?type=Electric&limit=20`.

### Exemplo de criação

```json
{
  "pokedex_number": 25,
  "name": "Pikachu",
  "type_1": "Electric",
  "type_2": null,
  "hp": 35,
  "attack": 55,
  "defense": 40,
  "special_attack": 50,
  "special_defense": 50,
  "speed": 90,
  "generation": 1
}
```

## Modelo de dados

Cada Pokémon tem ID interno, número único da Pokédex, nome único, tipo primário, tipo secundário opcional, seis atributos de batalha e geração. O Pydantic valida entradas e o SQLAlchemy persiste os dados. Restrições no banco reforçam unicidade e valores não negativos.

## Estrutura

```text
app/                 Aplicação, modelos, schemas e conexão
 tests/              Testes automatizados
.github/workflows/   CI com pytest
Dockerfile           Imagem da API
docker-compose.yml   API + PostgreSQL
.env.example         Variáveis de ambiente de exemplo
deployment.yaml      Manifesto Kubernetes
service.yaml         Service Kubernetes
pyproject.toml       Configuração Poetry/pytest
requirements.txt     Dependências reproduzíveis
```

## Versionamento Git

O histórico real de commits é criado no repositório local durante o desenvolvimento; um arquivo ZIP não transporta um histórico Git válido. Para versionar esta entrega em etapas, inicialize um repositório e faça commits separados, por exemplo:

```bash
git init
git add .gitignore .dockerignore pyproject.toml requirements.txt .env.example
 git commit -m "chore: configurar projeto e dependências"
git add app
 git commit -m "feat: implementar CRUD de Pokémon com FastAPI e SQLAlchemy"
git add tests
 git commit -m "test: cobrir endpoints e validações da API"
git add Dockerfile docker-compose.yml
 git commit -m "build: containerizar API e PostgreSQL"
git add README.md .github deployment.yaml service.yaml
 git commit -m "docs: documentar API, CI e implantação"
```

Revise os arquivos e execute os testes antes de enviar o projeto para o repositório remoto. O vídeo do módulo pode conter detalhes adicionais que não aparecem no enunciado escrito.
