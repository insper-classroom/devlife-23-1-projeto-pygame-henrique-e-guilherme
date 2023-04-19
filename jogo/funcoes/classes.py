import pygame




class TelaInicial():
    def __init__(self, assets):
        self.dicionario = assets
        self.tela = assets['tela']
        self.fonte = pygame.font.Font(assets['fonte'], 50)
        self.texto = self.fonte.render('Tela inicial', True, (0, 0, 0))
        self.tem_que_trocar = False

    def desenha(self):
        self.tela.fill((255, 255, 255))
        self.tela.blit(self.texto, (300, 0))
        pygame.display.update()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
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

        self.tem_que_trocar = False


        self.inimigo = Inimigo()
        self.jogador = Jogador()

    def desenha(self):
        self.tela.blit(self.fundo, (0, 0))
        self.tela.blit(self.texto, (250, 0))
        self.tela.blit(self.chao, (0, 620))

        self.inimigo.update()
        self.tela.blit(self.inimigo.image, self.inimigo.rect)

        self.jogador.update()
        self.tela.blit(self.jogador.image, self.jogador.rect)

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
            self.jogador.pulo_jogador(event)
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
        
        #Faz o jogador cair
        self.rect.centery += self.gravidade
        self.gravidade += 0.05


        #Não deixa o jogador passar do chão
        if self.rect.centery >= 560:
            self.rect.centery = 560
            

    def pulo_jogador (self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:

                #Faz o jogador pular
                if self.rect.bottom >= 560:
                    self.gravidade = -6

class Inimigo (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('jogo/assets/inimigo_provisorio.png').convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 4)
        self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect()

        self.rect.centerx = 1280
        self.rect.centery = 600
    
    def update(self):
        self.rect.centerx -= 1

        if self.rect.centerx <= -100:
            self.rect.centerx = 1280
