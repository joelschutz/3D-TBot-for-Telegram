# 3D-TBot-for-Telegram
A a telegram bot to help yout play RPG games with your friends over Telegram.

## Usabilidade
No momento todas as funcionalidades ainda não foram implementadas, porém você já pode utilizar o bot com e fazer alguns teste.
Para criar um nome personagem basta utilizar o comando **/criar**. O bot vai pedir um nome para o seu personagem, perguntar o level dele e a raça. Essas duas últimas utilizam a opção de Teclado Personalizado do Telegram.
Ao fim o personagem pode ser salvo em um stock de personagens em arquivo para ser acessado a qualquer momento.

## Funcionalidades
- Criar Personagens(Parcialmente implementado)
    - Atribuir level(Implementado)
    - Atribuir raça(Implementado)
    - Atribuir modificadores(Implementado)
    - Atribuir características(Implementado)
    - Comprar características(Parcialmente implementado)
    - Distribuir pontos(Parcialmente implementado)
    - Atribuir itens
    - Definir tipo de dano
    - Atribuir magias e habilidades especiais
    - Definir história
- Salvar Personagens de usuários(Implementado)
    - Salvar um stock de personagens em disco(Implementado)
    - Identificar stock de forma única para cada usuário(Implementado)
- Mostrar e editar os Personagens salvos
    - Carregar stock salvo em disco para o usuário
    - Permitir que o usuário veja lista de personagens salvos
    - Permitir que o usuário edite as informações dos personagens salvos
- Interagir com grupos
    - Importar personagens salvos para uso em jogo em grupo
    - Implementar testes de habilidade
    - Implementar itens e recompensas 
    - Implementar combate

## Notas finais
Vou dedicar essa parte do README para fazer alguns comentários sobre o projeto ao longo do tempo. As últimas atualizações estarão sempre listados primeiro.

(08/06/2020) - Hoje Sai a uma nova implementação do bot escrito em Pyrogram, ela substitui a ultima versão em Aiogram. Essa mudança se deve por essa biblioteca contar com uma documentação mais extensa e detalhada que a outra. Além disso os seus métodos são mais fáceis de implementar e não forçam tanto o desenvolvedor a se prender a uma forma única de construir seu código.
Também há algumas atualizações nas funcionalidades que vão no sentido de corrigir bugs e implementar o stock de personagens. Passei a ultima semana dedicado exclusivamente a esse projeto e decidi dar uma pausa de alguns dias para estudar outras coisas. Espero voltar logo em breve para funalizar esse bot.
