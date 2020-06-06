import logging
import ficha

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

API_TOKEN = 'TOKEN DO SEU BOT'

#Configura logging
logging.basicConfig(level=logging.INFO)

#Inicializa bot e dispatcher
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage = storage)
per = []

#Declara Estados do programa
class Criar(StatesGroup):
    nome = State()  # Nome do personagem
    level = State()  # Level do Personagem
    raca = State()  # Raça do personagem


#Função de prova de conceito
# Essa função assiste o usuário a cria um personagem quando o comando /criar é enviado.
@dp.message_handler(commands = 'criar')
async def criar(message: types.Message):
    await message.reply('Oba, vamos criar um personagem novo.')
    await Criar.nome.set()
    await message.reply('Qual vai ser o nome do seu personagem')
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    # nome = message.text
    # nome = nome.replace('/criar ', '')
    # if nome in players:
    #     await message.answer('Esse personagem já existe:\n' + players[nome].dados())
    # else:
    #     players[nome] = ficha.criar(nome, 1, count*2)
    #     count += 1
    #     await message.answer(players[nome].dados())

#Permite que o usuário cancele o processo
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())

#Processa nome do personagem e segue para o proximo item: level
@dp.message_handler(state=Criar.nome)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nome'] = message.text
    
    #Cria teclado com opções de 1 a 5
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for n in range(1,6):
        markup.add(str(n))

    await Criar.next()
    await message.reply("E qual o level dele?", reply_markup=markup)

#Processa level do personagem e segue para o proximo item: raca
@dp.message_handler(state=Criar.level)
async def process_level(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['level'] = int(message.text)
        logging.info(f'Recebendo Level: {message.text}')

    markup = types.ReplyKeyboardRemove()
    
    #Cria teclado com 10 opções de raças
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    for n in range(1,11):
        markup.add(f'{n}.{ficha.nome_raca(n)}')

    await Criar.next()
    await message.reply("E qual a raça dele?", reply_markup=markup)

#Processa raça do personagem e cria personagem
@dp.message_handler(state=Criar.raca)
async def process_raca(message: types.Message, state: FSMContext):
    
    async with state.proxy() as data:
        raca = message.text.split('.')
        logging.info(f'Identificando raça. {raca}')
        data['raca'] = int(raca[0])

    markup = types.ReplyKeyboardRemove()
    logging.info(f"Criando personagem com os dados. Nome: {data['nome']}, level: {data['level']}, raça:{data['raca']}")
    per.append(ficha.criar(data['nome'], data['level'], data['raca'], [],[]))

    await message.reply("Para as informações do seu personagem mande /print", reply_markup=markup)
    await state.finish()

#Função que imprime o ultimo personagem criado ao receber o comando /print
@dp.message_handler(commands = 'print')
async def print(message: types.Message):
    info = per[len(per)-1].dados()
    mensagem = f"\
    Nome: {info['básico']['Nome']}\n\
    Level: {info['básico']['Nível']}\n\
    Raça: {info['básico']['raca']}\n\
    Atributos:\n\
    Força - {info['atributos']['Força']}\n\
    Habilidade - {info['atributos']['Habilidade']}\n\
    Resistência - {info['atributos']['Resistência']}\n\
    Armadura - {info['atributos']['Armadura']}\n\
    Poder de Fogo - {info['atributos']['Poder de Fogo']}\n\
    Características: {info['características']}"

    await message.answer(mensagem)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
