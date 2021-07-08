# musicsite

[![CI](https://github.com/sammyzord/musicsite/actions/workflows/main.yml/badge.svg)](https://github.com/sammyzord/musicsite/actions/workflows/main.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/820348cf4f3506300f63/maintainability)](https://codeclimate.com/github/sammyzord/musicsite/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/820348cf4f3506300f63/test_coverage)](https://codeclimate.com/github/sammyzord/musicsite/test_coverage)

O musicsite é um aplicativo feito em python django feito para um desafio técnico de um processo seletivo. Ele possui um sistema de autenticação simples, um CRUD de Músicas e se comunica com a API aberta do Spotify para obter as 50 músicas mais tocadas em um determinado país.

A aplicação está disponível para demonstração no link a seguir:

[https://musicsite-flux.herokuapp.com/](https://musicsite-flux.herokuapp.com/ "Ver aplicação no Heroku")

## Como rodar

Para rodar o ambiente de desenvolvimento é necessário seguir os seguintes passos:

1. Instalar o **Docker** e o **Docker-Compose**;
1. Criar um arquivo `.env` a partir do arquivo `.env.example` fornecido;
1. Se autenticar no Dashboard de desenvolvedor do Spotif;
1. Obter o seu `CLIENT_ID` e `CLIENT_SECRET`;
1. Disponibilizar estes valores no arquivo `.env`;
1. Escolher a `PORT` em que a aplicação rodará e disponibilizar ela no `.env`.

Concluídos estes passos, é possível rodar a aplicação usando o comando a seguir:

```sh
sudo docker-compose up web
```
