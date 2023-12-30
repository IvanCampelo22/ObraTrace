# Ordem de Serviço | Backe-End

## Objetivo 

 Essa aplicação tem como objetivo sanar problemas que empresas e suas equipes tem ao atender clientes, tanto em obras quanto em futuras manutenções. Esse aplicativo vai ser capaz de cadastrar Clientes, Fucionários, e também criar checklists. Os Clientes serão capazes de verificar as os que estão abertas em seu nome, enquanto que os funcionários terão uma maior liberdade para criar, editar, excluir... dentre outras coisas. Há algumas funcionalidades essenciais, como criar Ordem de Serviço para instalação de equipamentos em obras, outra para manutenção ou instalação de equipamentos, filtros que buscam clientes ativos e inativos, filtros por data e, também algumas coisas que já foram deixadas prontas para que no futuro possam ser melhor trabalhadas. 


## Tecnologias Usadas

- Python
- Fastapi
- Postgresql
- Docker


 ## Como executar o projeto

1. Ir até a pasta do projeto e criar a virualenv

> virtualenv venv

2. Ative a virtualenv

> source venv/bin/activate

3. Instale as dependencias

> pip install -r requirements.txt

4. Na raiz do projeto, onde estiver o arquivo main.py execute: 

> python main.py


### Se sua distribuição adotar o PEP 668 

1. Ir até a pasta do projeto e criar a virualenv
> python3 -m venv .venv

2. Ative a virtualenv
> source .venv/bin/activate

3. Instale as dependencias

> python3 -m pip install -r requirements.txt

4. Na raiz do projeto, onde estiver o arquivo main.py execute: 

> python3 -m main

* Teste local

> http://127.0.0.1:8000/docs


## Executando via Docker

1. Faça o build da image Docker que está na raiz do projeto

 > docker build -t fastapi-app .

2. Execute a imagem Docker que foi construida

 > docker run -p 8080:8080 fastapi-app


## Como fazer migrações no banco de dados

1. Execute o comando para criar o arquivo de migração no versions

> alembic revision -m "<nome-da-migraçao>"

2. Depois de criada a migração execute

> alembic upgrade head --sql

> alembic upgrade head

### Obs: consulte a documentação do alembic para entender como fazer a migração no banco de dados, pois se trata de algo um tanto complexo. 
