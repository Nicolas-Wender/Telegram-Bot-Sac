# Telegram Bot SAC

Um bot de suporte ao cliente para Telegram, desenvolvido em Python, que apresenta categorias e perguntas frequentes para facilitar o atendimento.

## Funcionalidades

- Menu interativo com categorias e perguntas frequentes.
- Respostas automáticas para dúvidas comuns.
- Comandos `/start` e `/help`.

## Pré-requisitos

- Python 3.10+
- [python-telegram-bot](https://python-telegram-bot.org/) v20+
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Instalação

1. Clone este repositório:

   ```
   git clone https://github.com/seu-usuario/Telegram-Bot-Sac.git
   cd Telegram-Bot-Sac
   ```

2. Instale as dependências:

   ```
   pip install -r requirements.txt
   ```

3. Crie um arquivo `.env` com o token do seu bot:

   ```
   TOKEN=seu_token_aqui
   ```

4. Adicione um arquivo `questions.json` com as categorias e perguntas.

## Executando o Bot

```
python bot.py
```

## Estrutura do Projeto

- `bot.py` — Código principal do bot.
- `questions.json` — Perguntas e respostas exibidas pelo bot.
- `.env` — Variáveis de ambiente (não versionado).
- `README.md` — Este arquivo.

## Licença

MIT
