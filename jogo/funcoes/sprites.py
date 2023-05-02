import pygame
import random
from spritesheet import SpriteSheet

class Coracao (pygame.sprite.Sprite):
    """Classe que representa o coração do jogador"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.lista_sprites = []

        self.frame_atual = 0
        self.cooldown_animacao = 100
        #Tipo de Inimigo
        posicao_y = 595
        
        self.lista_sprites.append(pygame.transform.scale(pygame.image.load('jogo/assets/coracao/Cuore1.png').convert_alpha(), (40, 40)))
        self.lista_sprites.append(pygame.transform.scale(pygame.image.load('jogo/assets/coracao/Cuore2.png').convert_alpha(), (40, 40)))
        self.lista_sprites.append(pygame.transform.scale(pygame.image.load('jogo/assets/coracao/Cuore3.png').convert_alpha(), (40, 40)))
        self.lista_sprites.append(pygame.transform.scale(pygame.image.load('jogo/assets/coracao/Cuore4.png').convert_alpha(), (40, 40)))
        self.lista_sprites.append(pygame.transform.scale(pygame.image.load('jogo/assets/coracao/Cuore5.png').convert_alpha(), (40, 40)))
        self.lista_sprites.append(pygame.transform.scale(pygame.image.load('jogo/assets/coracao/Cuore6.png').convert_alpha(), (40, 40)))
        self.lista_sprites.append(pygame.transform.scale(pygame.image.load('jogo/assets/coracao/Cuore7.png').convert_alpha(), (40, 40)))
        self.lista_sprites.append(pygame.transform.scale(pygame.image.load('jogo/assets/coracao/Cuore8.png').convert_alpha(), (40, 40)))
        self.image = self.lista_sprites[self.frame_atual]

        self.mask = pygame.mask.from_surface(self.image)
        self.tempo = pygame.time.get_ticks()

        self.rect = self.mask.get_rect()
        self.rect.centery = posicao_y
        self.rect.centerx = 1280

        self.som = pygame.mixer.Sound('jogo/assets/audio/vida_som.mp3')

    def update(self):
        #Movimentação do coração
        self.rect.centerx -= 2.5

        if self.rect.centerx <= -100:
            self.kill()
        tempo_atual = pygame.time.get_ticks()
        
        #Animação do coração
        if tempo_atual - self.tempo > self.cooldown_animacao:
            self.tempo = tempo_atual
            self.frame_atual += 1
        if self.frame_atual >= len(self.lista_sprites):
            self.frame_atual = 0
        self.image = self.lista_sprites[self.frame_atual]


class Explosao (pygame.sprite.Sprite): 
    """Classe que representa a explosão do inimigo quando é atingido por um tiro
        A explosão é um objeto
    """
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = SpriteSheet('jogo/assets/sprites/explosao.png')
        self.lista_sprites = []

        self.frame_atual = 0
        self.cooldown_animacao = 100

        #Animacao
        for contador in range(8):
            self.lista_sprites.append(self.sprites.corta_imagem(contador, 48, 48, 2))
        self.image = self.lista_sprites[0]


        self.image = pygame.transform.scale_by(self.image, 1)
        self.mask = pygame.mask.from_surface(self.image)

        self.tempo = pygame.time.get_ticks()

        self.rect = self.mask.get_rect()
        
        #Posicoes
        self.rect.centery = pos_y
        self.rect.centerx = pos_x

    
    def update(self):
        tempo_atual = pygame.time.get_ticks()

        if tempo_atual - self.tempo > self.cooldown_animacao:
            self.tempo = tempo_atual
            self.frame_atual += 1
        if self.frame_atual >= len(self.lista_sprites):
            self.frame_atual = 0
        self.image = self.lista_sprites[self.frame_atual]

        if self.rect.centerx <= -100:
            self.kill()

class ObjetoFundo(pygame.sprite.Sprite):
    def __init__(self, numero):
        pygame.sprite.Sprite.__init__(self)
        self.lista_imagens = []
        self.lista_imagens.append(pygame.image.load('jogo/assets/objetos_fundo/objeto2.png').convert_alpha())
        self.lista_imagens.append(pygame.image.load('jogo/assets/objetos_fundo/objeto3.png').convert_alpha())
        self.lista_imagens.append(pygame.image.load('jogo/assets/objetos_fundo/objeto4.png').convert_alpha())
        self.lista_imagens.append(pygame.image.load('jogo/assets/objetos_fundo/objeto5.png').convert_alpha())
        self.image = self.lista_imagens[numero]
        self.image = pygame.transform.scale_by(self.image, 7)
        self.rect = self.image.get_rect()

        #Quatro possíveis posições para os objetos dependendo do número que for passado
        if numero == 0:
            self.rect.centery = 530
        elif numero == 1:
            self.rect.centery = 520
        elif numero == 2:
            self.rect.centery = 515
        elif numero == 3:
            self.rect.centery = 557
        self.rect.centerx = 1350


    def update(self):
        self.rect.x -= 5

        if self.rect.left < -20:
            self.kill()

class Tiro (pygame.sprite.Sprite):
    """Classe que representa os tiros do jogador"""
    def __init__(self, jogador_center_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('jogo/assets/sprites/tiro.png').convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 0.5)
        self.rect = self.image.get_rect()

        self.rect.centery = jogador_center_y 
        self.rect.centerx = 100

        self.som = pygame.mixer.Sound('jogo/assets/audio/tiro_som.mp3')

    def update(self):
        #Movimentação do tiro para a direita
        self.rect.centerx += 8

        #Se o tiro passar da tela, ele é destruído
        if self.rect.centerx > 1280:
            self.kill()

class CaixaTexto():
    """ 
    Classe utilizada para criar uma caixa de texto em que é possível escrever.

    ...

    Atributos
    ---------
    rect : pygame.Rect
        retângulo que representa a caixa de texto
    assets : dict
        dicionário com os assets do jogo
    texto : str
        texto que está sendo escrito na caixa de texto
    texto_surface : pygame.Surface
        superfície que contém o texto que está sendo escrito
    pode_escrever : bool
        variável que indica se é possível escrever na caixa de texto
    fonte : pygame.font.Font
        fonte utilizada para escrever o texto
    cor : str
        cor da caixa de texto
    """

    def __init__ (self, fonte, assets):
        self.rect = pygame.Rect(590, 500, 100 , 40)
        self.assets = assets
        self.texto = ''
        self.texto_surface = fonte.render(self.texto, True, 'Black')
        self.pode_escrever = False
        self.fonte = fonte
        self.cor = 'Yellow'
    
    def escreve(self, event): 
        """ Caso o usuário clique dentro da caixa, o retângulo muda de cor e é possível escrever.
            O texto é escrito dentro da caixa de texto pegando o unicode do evento.
            Ao escrever o tamanho do retângulo varia.

        Parameters
        ----------
        event : pygame.event.Event
            evento que está sendo tratado
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #Muda cor caso clicado
            if  self.rect.collidepoint(event.pos):
                self.pode_escrever = True
                self.cor = (152, 152, 49)
            else:
                self.pode_escrever = False
                self.cor = 'Yellow'
        #Salva o texto
        if event.type == pygame.KEYDOWN and self.pode_escrever:
            if event.key == pygame.K_RETURN:
                self.assets['usuario_atual'] = self.texto
                
            #Diminui o tamanho
            elif event.key == pygame.K_BACKSPACE:
                self.texto = self.texto[:-1]
                self.rect.width -= 20
                self.rect.x += 10
            #Aumenta o tamanho
            else:
                self.texto += event.unicode #https://www.pygame.org/docs/ref/event.html
                self.rect.width += 20
                self.rect.x -= 10
            self.texto_surface = self.fonte.render(self.texto, True, 'Black')
        
    def desenha(self, screen):
        pygame.draw.rect(screen, self.cor, self.rect, 5)
        screen.blit(self.texto_surface, (self.rect.x + 5, self.rect.y + 5))
