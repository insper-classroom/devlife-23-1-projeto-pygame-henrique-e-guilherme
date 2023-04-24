import pygame
from classes import TelaInicial, TelaJogo

def inicializa():
    pygame.init()
    tela = pygame.display.set_mode((1280,720))
    fonte = pygame.font.get_default_font()
    pygame.display.set_caption('Knight Runner')
    fonte2 = pygame.font.Font('jogo/assets/joystix monospace.otf', 25)

    assets ={
        'tela': tela,
        'fonte': fonte,
        'fonte2': fonte2,
        
        #Adicionei essas imagens so para testar e dps mudar
        'fundo': pygame.transform.scale((pygame.image.load('jogo/assets/Red Sky.png').convert_alpha()), (1280, 720)),
        'ground': pygame.transform.scale((pygame.image.load('jogo/assets/ground_provisorio.png').convert_alpha()), (1280, 300)),

    }
    return assets


def game_loop():
    assets = inicializa()
    tela_atual = TelaInicial(assets)
    while tela_atual.update(): 
        tela_atual = tela_atual.troca_tela()
        tela_atual.desenha()


if __name__ == '__main__':
    game_loop()

