import pygame
import random
from spritesheet import SpriteSheet

class Inimigo (pygame.sprite.Sprite):
    """Classe que representa os inimigos demônios e fantasmas
    
    ...

    Atributos
    ---------
    image : pygame.Surface
        imagem do inimigo
    lista_sprites : list
        lista de sprites do inimigo
    tipo : str
        tipo do inimigo
    sprites : SpriteSheet
        spritesheet do inimigo (Inicializa já com o do demônio)

    """
    def __init__(self, em_cima):
        pygame.sprite.Sprite.__init__(self)

        
        self.sprites = SpriteSheet('jogo/assets/sprites/demonio_sprite_sheet.png')
        self.lista_sprites = []

        self.frame_atual = 0
        self.cooldown_animacao = 100

        self.velocidade = 3
        

        if em_cima:
            posicao_y = 400 #Céu
            self.image = pygame.image.load('jogo/assets/sprites/ghost.png').convert_alpha()
            self.sprites = SpriteSheet('jogo/assets/sprites/ghost_sprite_sheet.png')
            self.tipo = 'fantasma'
            for contador in range(4):
                self.lista_sprites.append(self.sprites.corta_imagem(contador, 20, 22, 4))

            
        else:
            posicao_y = 595 #Chão
            self.image = pygame.image.load('jogo/assets/sprites/demon.png').convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)
            for contador in range(4):
                self.lista_sprites.append(self.sprites.corta_imagem(contador, 24 , 24, 4))
            self.tipo = 'demonio'



        self.image = pygame.transform.scale_by(self.image, 4)
        self.mask = pygame.mask.from_surface(self.image)
        self.tempo = pygame.time.get_ticks()

        self.rect = self.mask.get_rect()
        self.rect.centery = posicao_y
        self.rect.centerx = 1280

    def update(self):
        #Movimentação do inimigo para a esquerda
        self.rect.centerx -= self.velocidade

        #Se o inimigo passar da tela, ele é destruído
        if self.rect.centerx <= -100:
            self.kill()
        tempo_atual = pygame.time.get_ticks()
        #Troca de frame da animação
        if tempo_atual - self.tempo > self.cooldown_animacao:
            self.tempo = tempo_atual
            self.frame_atual += 1
        if self.frame_atual >= len(self.lista_sprites):
            self.frame_atual = 0
        self.image = self.lista_sprites[self.frame_atual]

class Morcego (pygame.sprite.Sprite):
    """Classe que representa os morcegos"""


    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = SpriteSheet('jogo/assets/sprites/morcego_spritesheet.png')
        self.lista_sprites = []

        self.frame_atual = 0
        self.cooldown_animacao = 100

        #Animacao
        for contador in range(2):
            self.lista_sprites.append(self.sprites.corta_imagem(contador, 52, 80, 1))
        self.image = self.lista_sprites[0]


        self.image = pygame.transform.scale_by(self.image, 1)
        self.mask = pygame.mask.from_surface(self.image)

        self.tempo = pygame.time.get_ticks()

        self.rect = self.mask.get_rect()
        
        #Posicoes
        self.rect.centery = 500
        self.rect.centerx = 1280

        self.tipo = 'morcego'
        self.velocidade = 7
    
    def update(self):
        #Movimentação do morcego para a esquerda (Mais rápido que os outros inimigos)
        self.rect.centerx -= self.velocidade
        tempo_atual = pygame.time.get_ticks()

        #Troca de frame da animação
        if tempo_atual - self.tempo > self.cooldown_animacao:
            self.tempo = tempo_atual
            self.frame_atual += 1
        if self.frame_atual >= len(self.lista_sprites):
            self.frame_atual = 0
        self.image = self.lista_sprites[self.frame_atual]

        #Se o morcego passar da tela, ele é destruído
        if self.rect.centerx <= -100:
            self.kill()

