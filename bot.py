import logging
import ficha

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = 'TOKEN TO SEU BOT'

#Configura logging
logging.basicConfig(level=logging.INFO)

#Inicializa bot, dispatcher e alguma variáveis
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
players = {}
index = len(players) - 1
count = 0

#Função de prova de conceito
# Essa função simplismente cria um personagem quando o comando /start é enviado e
# verifica se personagem já consta na lista de personagens.
@dp.message_handler(commands = 'start')
async def start(message: types.Message):
    global count
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    nome = message.text
    nome = nome.replace('/start ', '')
    if nome in players:
        await message.answer('Esse personagem já existe:\n' + players[nome].dados())
    else:
        players[nome] = ficha.criar(nome, 1, count*2)
        count += 1
        await message.answer(players[nome].dados())

#Função que imprime o ultimo personagem criado ao receber o comando /print
@dp.message_handler(commands = 'print')
async def print(message: types.Message):
    # print(players[index].dados())
    await message.answer(players[index].dados())



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
