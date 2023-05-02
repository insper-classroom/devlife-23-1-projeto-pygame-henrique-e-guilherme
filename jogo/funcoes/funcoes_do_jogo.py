import pygame
from telas import TelaInicial


def inicializa():
    """Função que inicializa o jogo e carrega os assets
        Retorna um dicionário com os assets
    """
    pygame.init()
    pygame.mixer.init()
    tela = pygame.display.set_mode((1280,720))
    fonte = pygame.font.get_default_font()
    pygame.display.set_caption('Knight Runner')
    fonte2 = pygame.font.Font('jogo/assets/fontes/joystix monospace.otf', 25)
    fonte2_grande = pygame.font.Font('jogo/assets/fontes/joystix monospace.otf', 40)
    fonte2_xgrande = pygame.font.Font('jogo/assets/fontes/joystix monospace.otf', 60)

    assets ={
        'tela': tela,
        'fonte': fonte,
        'fonte2': fonte2,
        'fonte2_grande': fonte2_grande,
        'fonte2_xgrande': fonte2_xgrande,
        
        'fundo': pygame.transform.scale((pygame.image.load('jogo/assets/imagens/Red Sky.png').convert_alpha()), (1280, 720)),
        'ground': pygame.transform.scale((pygame.image.load('jogo/assets/imagens/ground1.png').convert_alpha()), (1280, 300)),

        'usuario_atual': '',
        'highscore': 0,
        'pontuacao': 0,
    }
    return assets


def game_loop():
    """Função que inicializa o jogo e chama as telas
        Caso a tela seja trocada, a função chama a nova tela
    """
    assets = inicializa()
    tela_atual = TelaInicial(assets)
    while tela_atual.update(assets): 
        tela_atual = tela_atual.troca_tela()
        tela_atual.desenha()
