import pygame
import random



class TelaInicial():
    def __init__(self, assets):
        self.dicionario = assets
        self.tela = assets['tela']
        self.fonte = pygame.font.Font(assets['fonte'], 50)
        self.texto = self.fonte.render('Tela inicial', True, (0, 255, 0))

        self.fonte2 = assets['fonte2']
        self.texto2 = self.fonte2.render('Pressione "ESPAÇO" para continuar', True, (255, 230, 0))
        self.texto2_pos_x = 640 - self.texto2.get_rect()[2] / 2
        
        self.logo = pygame.transform.scale(pygame.image.load('jogo/assets/logo.png'), (812, 98))

        self.fundo = assets['fundo']
        self.chao = assets['ground']

        self.musica_tela_inicial_tocando = False

        self.tem_que_trocar = False

    def desenha(self):
        self.tela.fill((255, 255, 255))

        self.tela.blit(self.fundo, (0, 0))
        self.tela.blit(self.chao, (0, 620))

        self.tela.blit(self.texto, (300, 0))

        self.tela.blit(self.logo, (234, 250))

        self.tela.blit(self.texto2, (self.texto2_pos_x, 368))
        pygame.display.update()

    def update(self):
        if not self.musica_tela_inicial_tocando:
            pygame.mixer_music.load('jogo/assets/musica_inicial.ogg')
            pygame.mixer_music.set_volume(0.3)
            pygame.mixer_music.play()
            self.musica_tela_inicial_tocando = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.tem_que_trocar = True
        return True
    
    def troca_tela(self):
        if self.tem_que_trocar:
            return TelaJogo(self.dicionario)
        else:
            return self

class TelaJogo():
    def __init__(self, assets):

        self.fonte = pygame.font.Font(assets['fonte'], 50)
        self.texto = self.fonte.render('Tela Jogo', True, (255, 0, 0))
        self.dicionario = assets
        #Adicionei essas imagens so para testar e dps mudar
        self.fundo = assets['fundo']
        self.chao = assets['ground']
        self.tela = assets['tela']

        self.tem_que_trocar = False
        self.tempo = 0
        self.pode = True
        self.Clock = pygame.time.Clock() #https://www.pygame.org/docs/ref/time.html#pygame.time.Clock

        #fonte: https://youtu.be/ARt6DLP38-Y
        self.scroll_fundo = 0
        self.tiles_fundo = 1280 // self.fundo.get_width() + 1

        self.scroll_chao = 0
        self.tiles_chao = 1280 // self.chao.get_width() + 1

        self.jogador = Jogador()

    def desenha(self):
        #Fundo infinito
        for i in range(self.tiles_fundo):
            self.tela.blit(self.fundo, (i * self.fundo.get_width() + self.scroll_fundo, 0))
        self.scroll_fundo -= 5
        if abs(self.scroll_fundo) > self.fundo.get_width():
            self.scroll_fundo = 0
        
        #Chao infinito
        for i in range(self.tiles_chao):
            self.tela.blit(self.chao, (i * self.chao.get_width() + self.scroll_chao, 620))
        self.scroll_chao -= 5
        if abs(self.scroll_chao) > self.chao.get_width():
            self.scroll_chao = 0
 
        self.tela.blit(self.texto, (250, 0))

        #Vidas
        self.tela.blit(self.texto_vidas, (7, 5))

        self.inimigo.update()
        self.tela.blit(self.inimigo.image, self.inimigo.rect)

        self.jogador.update()

        self.vidas = self.fonte.render(str(self.jogador.vidas), True, (255, 0, 0))
        self.tela.blit(self.jogador.image, self.jogador.rect)

        self.Clock.tick(60) #https://www.pygame.org/docs/ref/time.html#pygame.time.Clock.tick

        pygame.display.update()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    #a condicao de trocar tela vira true
                    self.tem_que_trocar = True
                elif event.key == pygame.K_w:
                    self.tiros.add(Tiro(self.jogador.rect.centery))
                    Tiro(self.jogador.rect.centery).som.play()
            self.jogador.pulo_jogador(event)
        
        return True
    
    def troca_tela(self):
        if self.tem_que_trocar:
            return TelaInicial(self.dicionario)
        else:
            return self

    def spawn_inimigo(self):
        if random.randint(0, 1):
            condicao = True
        else: condicao = False
        self.lista_de_inimigos.append(Inimigo(condicao))



class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #Adicionei essas imagens so para testar e dps mudar
        #Cria retangulo e aumenta a imagem
        self.image = pygame.image.load('jogo/assets/jogador_provisorio.png').convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 4)
        self.rect = self.image.get_rect()

        #Coordenadas
        self.rect.centerx = 60      #https://www.pygame.org/docs/ref/rect.html
        self.rect.centery = 560

        self.x = 0
        self.delta_t = 0
        #Velocidade y

        self.vely = -25

        #Gravidade
        self.gravidade = 0


    def update(self):
        
        #Faz o jogador cair, simula o efeito da aceleração da gravidade
        self.rect.centery += self.gravidade
        self.gravidade += 0.3


        #Não deixa o jogador passar do chão
        if self.rect.centery >= 560:
            self.rect.centery = 560
        
    def pulo_jogador (self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                #Faz o jogador pular
                if self.rect.bottom >= 560:
                    self.gravidade = -20

class Inimigo (pygame.sprite.Sprite):
    def __init__(self, em_cima):
        pygame.sprite.Sprite.__init__(self)

        #Tipo de Inimigo
        if em_cima:
            posicao_y = 400
            self.image = pygame.image.load('jogo/assets/ghost_provisorio.png').convert_alpha()
            
        else:
            posicao_y = 595
            self.image = pygame.image.load('jogo/assets/inimigo_provisorio.png').convert_alpha()
            self.image = pygame.transform.flip(self.image, True, False)

        
        self.image = pygame.transform.scale_by(self.image, 4)
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.mask.get_rect()
        self.rect.centery = posicao_y
        self.rect.centerx = 1280
        self.rect.centery = 600
    
    def update(self):
        self.rect.centerx += 3

        if self.rect.centerx > 1280:
            self.kill()
