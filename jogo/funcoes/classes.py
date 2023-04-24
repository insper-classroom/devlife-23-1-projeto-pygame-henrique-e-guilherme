import pygame




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
        self.texto = self.fonte.render('Tela Jogo', True, (0, 255, 0))
        self.dicionario = assets
        #Adicionei essas imagens so para testar e dps mudar
        self.fundo = assets['fundo']
        self.chao = assets['ground']
        self.tela = assets['tela']

        self.fonte2 = assets['fonte2']
        
        self.imune = False
        self.timer_imune_comeco = 0
        self.timer_imune_fim = 0

        self.tem_que_trocar = False
        self.Clock = pygame.time.Clock() #https://www.pygame.org/docs/ref/time.html#pygame.time.Clock

        #fonte: https://youtu.be/ARt6DLP38-Y
        self.scroll_fundo = 0
        self.tiles_fundo = 1280 // self.fundo.get_width() + 1

        self.scroll_chao = 0
        self.tiles_chao = 1280 // self.chao.get_width() + 1

        self.jogador = Jogador()
        self.tiros = pygame.sprite.Group()

        self.inimigos = pygame.sprite.Group()
        self.inimigos.add(Inimigo())
        self.timer_spawn_comeco = 0

        #Texto das vidas
        self.texto_vidas = pygame.transform.scale_by(self.fonte2.render(chr(9829) * self.jogador.vidas, True, (255, 0, 0)), 1.5)



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

        self.inimigos.update()
        self.inimigos.draw(self.tela)

        self.jogador.update()
        self.tela.blit(self.jogador.image, self.jogador.rect)

        self.tiros.update()
        self.tiros.draw(self.tela)

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
            self.jogador.pulo_jogador(event)
        
        #colisao com monstro
        if pygame.sprite.spritecollide(self.jogador, self.inimigos, False):
            if not self.imune:
                self.jogador.vidas -= 1
                self.imune = True
                self.texto_vidas = pygame.transform.scale_by(self.fonte2.render(chr(9829) * self.jogador.vidas, True, (255, 0, 0)), 1.5)
                self.timer_imune_comeco = pygame.time.get_ticks()
            else:
                self.timer_imune_fim = pygame.time.get_ticks()
                if self.timer_imune_fim - self.timer_imune_comeco > 3000:
                    self.imune = False
        
        pygame.sprite.groupcollide(self.inimigos, self.tiros, True, True)

        self.timer_spawn_fim = pygame.time.get_ticks()
        if self.timer_spawn_fim - self.timer_spawn_comeco > 5000:
            self.inimigos.add(Inimigo())
            self.timer_spawn_comeco = self.timer_spawn_fim

        return True
    
    def troca_tela(self):
        if self.tem_que_trocar:
            return TelaInicial(self.dicionario)
        else:
            return self

class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #Adicionei essas imagens so para testar e dps mudar
        #Cria retangulo e aumenta a imagem
        self.image = pygame.image.load('jogo/assets/jogador_provisorio.png').convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 4)
        self.rect = self.image.get_rect()

        self.vidas = 3

        #Coordenadas
        self.rect.centerx = 60
        self.rect.centery = 560

        self.x = 0
        self.delta_t = 0
        #Velocidade y

        self.vely = -21

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
                    self.gravidade = -15

class Inimigo (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('jogo/assets/inimigo_provisorio.png').convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 4)
        self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect()

        self.rect.centerx = 1280
        self.rect.centery = 600

        self.vidas = 3
    
    def update(self):
        self.rect.centerx -= 3

        if self.rect.centerx <= -100 or self.vidas <= 0:
            self.rect.centerx = 1300


class Tiro (pygame.sprite.Sprite):
    def __init__(self, jogador_center_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('jogo/assets/inimigo_provisorio.png').convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.centery = jogador_center_y
        self.rect.centerx = 60

    def update(self):
        self.rect.centerx += 3

        if self.rect.centerx > 1280:
            self.kill()
