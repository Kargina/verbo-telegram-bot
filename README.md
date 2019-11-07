# verbo-telegram-bot
[@learnwords_bot](https://telegram.me/learnwords_bot) is a bot for remembering new foreign words

## Run with docker

1. Get API key from [@BotFather](https://telegram.me/BotFather)
2. Clone repo and run:
```bash
git clone https://github.com/Kargina/verbo-telegram-bot
cd verbo-telegram-bot
docker build . -t bot
docker run -d -e TELEGRAM_TOKEN=<YOUR_TOKEN> bot
```