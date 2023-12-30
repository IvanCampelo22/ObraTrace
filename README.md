# Ordem de Serviço | Backe-End

## Objetivo 

 Essa aplicação tem como objetivo sanar problemas que empresas e suas equipes tem ao atender clientes, tanto em obras quanto em manutenções. Esse aplicativo vai ser capaz de cadastrar Clientes e Funcionários. Os Clientes serão capazes de verificar as Ordens de Serviços que estão abertas em seu nome, enquanto que os funcionários terão uma maior liberdade para criar, editar, excluir... dentre outras coisas. Há algumas funcionalidades essenciais, como criar Ordem de Serviço para instalação de equipamentos em obras e Ordem de Serviço para manutenção ou instalção de equipamentos.



docker build -t fastapi-app .

docker run -p 8080:8080 fastapi-app