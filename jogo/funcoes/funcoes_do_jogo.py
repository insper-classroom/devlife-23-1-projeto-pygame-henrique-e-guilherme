import pygame
from classes import TelaInicial, TelaJogo


def inicializa():
    pygame.init()
    tela = pygame.display.set_mode((800,600))
    fonte = pygame.font.get_default_font()
    pygame.display.set_caption('Knight Runner')

    assets ={
        'tela': tela,
        'fonte': fonte,

    }
    return assets

def recebe_eventos():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False
    return True

def game_loop():
    assets = inicializa()
    tela_atual = TelaInicial(assets)
    while tela_atual.update():
        tela_atual = tela_atual.troca_tela()
        tela_atual.desenha()

if __name__ == '__main__':
    game_loop()

