import pygame
from spritesheet import SpriteSheet


class Jogador(pygame.sprite.Sprite):
    """Classe que representa o jogador

    ...

    Atributos
    ---------
    image : pygame.Surface
        imagem do jogador
    rect : pygame.Rect
        retângulo da imagem do jogador
    vely : int
        velocidade do jogador no eixo y
    gravidade : int
        aceleração da gravidade
    lista_sprites : list
        lista de sprites do jogador

    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #Cria retangulo e aumenta a imagem
        self.sprites = SpriteSheet('jogo/assets/sprites/knight_.png')
        self.lista_sprites = []
        for contador in range(4):
            self.lista_sprites.append(self.sprites.corta_imagem(contador, 24 , 24, 4))

        self.frame_atual = 0

        #Tempo de troca de frame da animação em milisegundos
        self.cooldown_animacao = 100

        self.image = pygame.image.load('jogo/assets/sprites/knight_.png').convert_alpha()

        self.rect = self.lista_sprites[0].get_rect()

        self.dano_som = pygame.mixer.Sound('jogo/assets/audio/dano_som.mp3')
        self.pontuou_som = pygame.mixer.Sound('jogo/assets/audio/pontuou_som.mp3')

        self.vidas = 3

        self.mask = pygame.mask.from_surface(self.lista_sprites[0])

        self.dano_som = pygame.mixer.Sound('jogo/assets/audio/dano_som.mp3')
        self.pontuou_som = pygame.mixer.Sound('jogo/assets/audio/pontuou_som.mp3')
        self.pulo_som = pygame.mixer.Sound('jogo/assets/audio/pulo2_som.mp3')

        self.vidas = 3

        self.municoes = 3

        #Coordenadas
        self.rect.centerx = 80
        self.rect.centery = 600

        #Velocidade y

        self.vely = -21

        #Gravidade
        self.gravidade = 0

        #Tempo
        self.tempo = pygame.time.get_ticks()


    def update(self):

        tempo_atual = pygame.time.get_ticks()

        #Troca de frame da animação
        if tempo_atual - self.tempo > self.cooldown_animacao:
            #Próximo frame
            self.tempo = tempo_atual
            self.frame_atual += 1
        #Se o frame atual for maior ou igual que o tamanho da lista de sprites, volta para o primeiro frame
        if self.frame_atual >= len(self.lista_sprites):
            self.frame_atual = 0
        self.image = self.lista_sprites[self.frame_atual]



        #Faz o jogador cair, simula o efeito da aceleração da gravidade
        self.rect.centery += self.gravidade
        self.gravidade += 0.3


        #Não deixa o jogador passar do chão
        if self.rect.centery >= 600:
            self.rect.centery = 600
        
    def pulo_jogador (self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:

                #Muda a gravidade para cima para simular o pulo
                if self.rect.bottom >= 610:
                    self.gravidade = -10
                    self.pulo_som.play()
    
    def colisao_jogador(self,  inimigo):
        #Fazer a colisao do jogador com os inimigos através da máscara de pixels
        #https://www.pygame.org/docs/ref/mask.html
        if pygame.sprite.collide_mask(self, inimigo):
            self.vidas -= 1
            self.dano_som.play()
            return True

