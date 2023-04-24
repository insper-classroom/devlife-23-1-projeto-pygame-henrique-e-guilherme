import pygame
import random



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
        self.texto = self.fonte.render('Tela Jogo', True, (255, 0, 0))
        self.dicionario = assets
        #Adicionei essas imagens so para testar e dps mudar
        self.fundo = assets['fundo']
        self.chao = assets['ground']
        self.tela = assets['tela']
        
        self.lista_de_inimigos = []
        self.spawn_inimigo()

        self.tem_que_trocar = False
        self.tempo = 0
        self.pode = True
        self.Clock = pygame.time.Clock() #https://www.pygame.org/docs/ref/time.html#pygame.time.Clock


        self.jogador = Jogador()
        self.vidas = self.fonte.render(str(self.jogador.vidas), True, (0, 255, 0))
        
    def desenha(self):
        self.tela.blit(self.fundo, (0, 0))
        self.tela.blit(self.texto, (250, 0))
        self.tela.blit(self.chao, (0, 620))

        for inimigo in self.lista_de_inimigos:
            inimigo.update()
            self.tela.blit(inimigo.image, inimigo.rect)

        
        self.jogador.update()

        self.vidas = self.fonte.render(str(self.jogador.vidas), True, (255, 0, 0))
        self.tela.blit(self.jogador.image, self.jogador.rect)
        self.tela.blit(self.vidas, (0, 0))
    

        #Trava os fps pra movimentação ficar clean  
        self.Clock.tick(60) #https://www.pygame.org/docs/ref/time.html#pygame.time.Clock.tick

        pygame.display.update()

    def update(self):
        relogio = pygame.time.get_ticks() // 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    #a condicao de trocar tela vira true
                    self.tem_que_trocar = True
            self.jogador.pulo_jogador(event)

        #Fiz essa gambiarra pra remover o inimigo da lista de inimigos e ter a colisão perfeita (máscara)
        for inimigo in self.lista_de_inimigos:
            if self.jogador.colisao_jogador(inimigo) or inimigo.rect.centerx <= 0:
                self.lista_de_inimigos.remove(inimigo)

        #Spawna inimigos a cada 2 segundos
        if relogio % 2 == 0 and self.pode and relogio != 0:
            self.spawn_inimigo()
            self.pode = False
            self.tempo = relogio
            
        #Faz spawnar a cada 1 segundo
        if self.tempo != relogio:
            self.pode = True

            
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
        
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect()

        #Vidas
        self.vidas = 5

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
        self.gravidade += 1


        #Não deixa o jogador passar do chão
        if self.rect.centery >= 560:
            self.rect.centery = 560
        
    def pulo_jogador (self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                #Faz o jogador pular
                if self.rect.bottom >= 560:
                    self.gravidade = -20
    
    def colisao_jogador(self,  inimigo):
        #Fazer a colisao do jogador com os inimigos
        if pygame.sprite.collide_mask(self, inimigo):
            self.vidas -= 1
            return True

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

    
    def update(self):
        self.rect.centerx -= 5

        if self.rect.centerx <= -100:
            self.rect.centerx = 1280
