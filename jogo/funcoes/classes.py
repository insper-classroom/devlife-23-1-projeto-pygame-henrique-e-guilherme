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

    def update(self, assets):
        if not self.musica_tela_inicial_tocando:
            # pygame.mixer_music.load('jogo/assets/musica_inicial.ogg')
            # pygame.mixer_music.set_volume(0.3)
            # pygame.mixer_music.play()
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
            return TelaInstrucoes(self.dicionario)
        else:
            return self
        
class TelaInstrucoes():
    def __init__(self, assets):
        self.dicionario = assets
        self.tela = assets['tela']
        self.fonte = pygame.font.Font(assets['fonte'], 50)
        self.texto = self.fonte.render('Tela instrucoes', True, (0, 255, 0))
        self.fonte2 = assets['fonte2']
        self.fonte2_grande = assets['fonte2_grande']

        self.texto2 = self.fonte2_grande.render('COMO JOGAR:', True, (255, 230, 0))
        self.texto2_pos_x = 640 - self.texto2.get_rect()[2] / 2

        self.texto3 = self.fonte2.render('- Pressione "ESPAÇO" para pular', True, (255, 230, 0))
        self.texto3_pos_x = 640 - self.texto3.get_rect()[2] / 2

        self.texto4 = self.fonte2.render('- Pressione "BOTÃO MOUSE 1" para atirar', True, (255, 230, 0))
        self.texto4_pos_x = 640 - self.texto4.get_rect()[2] / 2

        self.texto5 = self.fonte2.render('- Sobreviva por mais tempo para obter pontos', True, (255, 230, 0))
        self.texto5_pos_x = 640 - self.texto5.get_rect()[2] / 2

        self.texto6 = self.fonte2.render('- Mate monstros para obter pontos', True, (255, 230, 0))
        self.texto6_pos_x = 640 - self.texto6.get_rect()[2] / 2

        self.texto7 = self.fonte2.render('PRESSIONE "ESPAÇO" PARA CONTINUAR', True, (255, 230, 0))
        self.texto7_pos_x = 640 - self.texto7.get_rect()[2] / 2

        self.fundo = assets['fundo']
        self.chao = assets['ground']

        self.musica_tela_inicial_tocando = True

        self.tem_que_trocar = False

    def desenha(self):
        self.tela.fill((255, 255, 255))

        self.tela.blit(self.fundo, (0, 0))
        self.tela.blit(self.chao, (0, 620))

        self.tela.blit(self.texto, (300, 0))

        self.tela.blit(self.texto2, (self.texto2_pos_x, 100))
        self.tela.blit(self.texto3, (self.texto3_pos_x, 220))
        self.tela.blit(self.texto4, (self.texto4_pos_x, 290))
        self.tela.blit(self.texto5, (self.texto5_pos_x, 360))
        self.tela.blit(self.texto6, (self.texto6_pos_x, 430))
        self.tela.blit(self.texto7, (self.texto7_pos_x, 550))
        pygame.display.update()

    def update(self, assets):
        if not self.musica_tela_inicial_tocando:
            # pygame.mixer_music.load('jogo/assets/musica_inicial.ogg')
            # pygame.mixer_music.set_volume(0.3)
            # pygame.mixer_music.play()
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

        self.lista_de_inimigos = []
        self.tempo = 0
        self.pode = True

        self.jogador = Jogador()
        self.tiros = pygame.sprite.Group()

        self.musica_jogo_tocando = False

        #Texto das vidas
        self.texto_vidas = pygame.transform.scale_by(self.fonte2.render(chr(9829) * self.jogador.vidas, True, (255, 0, 0)), 1.5)

        self.pontuacao = 0
        self.texto_pontuacao = self.fonte2.render('Current score: ' + str(self.pontuacao), True, (255, 230, 0))
        self.timer_pontuacao_comeco = 0
        self.texto_highscore = self.fonte2.render('High score: ' + str(assets['highscore']), True, (255, 230, 0))

        self.timer_recarga_municao_comeco = 0
        self.texto_municao = self.fonte2.render('Municao: ' + str(self.jogador.municoes), True, (255, 230, 0))


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
        self.tela.blit(self.texto_vidas, (7, 0))

        #Score
        self.tela.blit(self.texto_pontuacao, (1273 - self.texto_pontuacao.get_width(), 40))

        #High score
        self.tela.blit(self.texto_highscore, (1273 - self.texto_highscore.get_width(), 10))

        for inimigo in self.lista_de_inimigos:
            inimigo.update()
            self.tela.blit(inimigo.image, inimigo.rect)
        self.jogador.update()
        self.tela.blit(self.jogador.image, self.jogador.rect)

        self.tiros.update()
        self.tiros.draw(self.tela)

        self.tiros.update()
        self.tiros.draw(self.tela)

        self.Clock.tick(60) #https://www.pygame.org/docs/ref/time.html#pygame.time.Clock.tick

        self.tela.blit(self.texto_municao, (7, 40))

        pygame.display.update()

    def update(self, assets):
        if not self.musica_jogo_tocando:
            # pygame.mixer_music.load('jogo/assets/musica_jogo.ogg')
            # pygame.mixer_music.set_volume(0.2)
            # pygame.mixer_music.play()
            self.musica_jogo_tocando = True

        # if not self.musica_jogo_tocando:
        #     pygame.mixer_music.load('jogo/assets/musica_jogo.ogg')
        #     pygame.mixer_music.set_volume(0.2)
        #     pygame.mixer_music.play()
        #     self.musica_jogo_tocando = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.jogador.municoes > 0:
                    self.tiros.add(Tiro(self.jogador.rect.centery))
                    Tiro(self.jogador.rect.centery).som.play()
                    self.jogador.municoes -= 1
                    self.texto_municao = self.fonte2.render('Municao: ' + str(self.jogador.municoes), True, (255, 230, 0))
            self.jogador.pulo_jogador(event)
        
        relogio = pygame.time.get_ticks() // 1000

        #Fiz essa gambiarra pra remover o inimigo da lista de inimigos e ter a colisão perfeita (máscara)
        for inimigo in self.lista_de_inimigos:
            if self.jogador.colisao_jogador(inimigo):
                self.lista_de_inimigos.remove(inimigo)
                self.texto_vidas = pygame.transform.scale_by(self.fonte2.render(chr(9829) * self.jogador.vidas, True, (255, 0, 0)), 1.5)
            if inimigo.rect.centerx <= -100:
                self.lista_de_inimigos.remove(inimigo)
            if pygame.sprite.spritecollide(inimigo, self.tiros, True):
                self.lista_de_inimigos.remove(inimigo)
                Jogador().pontuou_som.play()
                self.pontuacao += 50
                self.texto_pontuacao = self.fonte2.render('Current score: ' + str(self.pontuacao), True, (255, 230, 0))

        #Spawna inimigos a cada 2 segundos
        if relogio % 2 == 0 and self.pode and relogio != 0:
            self.spawn_inimigo()
            self.pode = False
            self.tempo = relogio
            
        #Faz spawnar a cada 1 segundo
        if self.tempo != relogio:
            self.pode = True

        if self.jogador.vidas <=0:
            self.tem_que_trocar = True
            assets['pontuacao'] = self.pontuacao
 
        self.timer_pontuacao_fim = pygame.time.get_ticks() // 1000
        if self.timer_pontuacao_fim - self.timer_pontuacao_comeco >= 3:
            self.pontuacao += 5
            self.texto_pontuacao = self.fonte2.render('Current score: ' + str(self.pontuacao), True, (255, 230, 0))
            self.timer_pontuacao_comeco = self.timer_pontuacao_fim
        if self.pontuacao > assets['highscore']:
            assets['highscore'] = self.pontuacao
            self.texto_highscore = self.fonte2.render('High score: ' + str(assets['highscore']), True, (255, 230, 0))

        self.timer_recarga_municao_fim = pygame.time.get_ticks() // 1000
        if self.timer_recarga_municao_fim - self.timer_recarga_municao_comeco >= 7 and self.jogador.municoes < 3:
            self.jogador.municoes += 1
            self.timer_recarga_municao_comeco = self.timer_recarga_municao_fim
            self.texto_municao = self.fonte2.render('Municao: ' + str(self.jogador.municoes), True, (255, 230, 0))
            
        return True
    
    def spawn_inimigo(self):
        if random.randint(0, 1):
            condicao = True
        else: condicao = False
        self.lista_de_inimigos.append(Inimigo(condicao))
    
    def troca_tela(self):
        if self.tem_que_trocar:
            return TelaGameOver(self.dicionario)
        else:
            return self
        

class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #Adicionei essas imagens so para testar e dps mudar
        #Cria retangulo e aumenta a imagem
        self.sprites = SpriteSheet('jogo/assets/knight_.png')
        self.lista_sprites = []
        for contador in range(4):
            self.lista_sprites.append(self.sprites.corta_imagem(contador, 24 , 24, 4))

        self.frame_atual = 0
        self.cooldown_animacao = 100

        self.image = pygame.image.load('jogo/assets/knight_.png').convert_alpha()

        self.rect = self.lista_sprites[0].get_rect()

        self.dano_som = pygame.mixer.Sound('jogo/assets/dano_som.mp3')
        self.pontuou_som = pygame.mixer.Sound('jogo/assets/pontuou_som.mp3')

        self.vidas = 3

        self.mask = pygame.mask.from_surface(self.image)

        self.dano_som = pygame.mixer.Sound('jogo/assets/dano_som.mp3')
        self.pontuou_som = pygame.mixer.Sound('jogo/assets/pontuou_som.mp3')

        self.vidas = 3

        self.municoes = 3

        #Coordenadas
        self.rect.centerx = 80
        self.rect.centery = 600

        #Velocidade y

        self.vely = -21

        #Gravidade
        self.gravidade = 0
        self.tempo = pygame.time.get_ticks()


    def update(self):

        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo > self.cooldown_animacao:
            self.tempo = tempo_atual
            self.frame_atual += 1
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

                #Faz o jogador pular
                if self.rect.bottom >= 600:
                    self.gravidade = -10
    
    def colisao_jogador(self,  inimigo):
        #Fazer a colisao do jogador com os inimigos
        if pygame.sprite.collide_mask(self, inimigo):
            self.vidas -= 1
            self.dano_som.play()
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
        self.rect.centerx -= 3

        if self.rect.centerx <= -100:
            self.kill()

class Tiro (pygame.sprite.Sprite):
    def __init__(self, jogador_center_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('jogo/assets/tiro.png').convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 0.5)
        self.rect = self.image.get_rect()

        self.rect.centery = jogador_center_y
        self.rect.centerx = 60

        self.som = pygame.mixer.Sound('jogo/assets/tiro_som.mp3')

    def update(self):
        self.rect.centerx += 3

        if self.rect.centerx > 1280:
            self.kill()

class TelaGameOver():
    def __init__(self, assets):
        self.dicionario = assets
        self.tela = assets['tela']
        self.fonte = pygame.font.Font(assets['fonte'], 50)
        self.texto = self.fonte.render('Tela game over', True, (0, 255, 0))
        self.fonte2 = assets['fonte2']
        self.fonte2_grande = assets['fonte2_grande']
        self.fonte2_xgrande = assets['fonte2_xgrande']

        self.texto2 = self.fonte2_xgrande.render('GAME OVER', True, (255, 41, 41))
        self.texto2_pos_x = 640 - self.texto2.get_rect()[2] / 2

        self.texto3 = self.fonte2.render('Pressione "ESPAÇO" para reiniciar ou "ESC" PARA SAIR', True, (250, 250, 250))
        self.texto3_pos_x = 640 - self.texto3.get_rect()[2] / 2

        self.texto4 = self.fonte2.render('High score: ' + str(assets['highscore']), True, (250, 250, 250))
        self.texto4_pos_x = 640 - self.texto4.get_rect()[2] / 2
        
        self.texto5 = self.fonte2.render('Sua pontuação: ' + str(assets['pontuacao']), True, (250, 250, 250))
        self.texto5_pos_x = 640 - self.texto5.get_rect()[2] / 2

        self.fundo = assets['fundo']
        self.chao = assets['ground']

        self.musica_tela_jogo_tocando = True

        self.tem_que_trocar = False

    def desenha(self):
        self.tela.fill((0, 0, 0))

        self.tela.blit(self.texto, (300, 0))

        self.tela.blit(self.texto2, (self.texto2_pos_x, 250))
        self.tela.blit(self.texto4, (self.texto4_pos_x, 350))
        self.tela.blit(self.texto5, (self.texto5_pos_x, 400))
        self.tela.blit(self.texto3, (self.texto3_pos_x, 470))
        

        pygame.display.update()

    def update(self, assets):
        if not self.musica_tela_jogo_tocando:
            pygame.mixer_music.load('jogo/assets/musica_jogo.ogg')
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
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
        return True
    
    def troca_tela(self):
        if self.tem_que_trocar:
            return TelaJogo(self.dicionario)
        else:
            return self
        


#Fonte: https://www.youtube.com/watch?v=nXOVcOBqFwM&ab_channel=CodingWithRuss
class SpriteSheet:
    def __init__(self, imagem):
        self.sheet = pygame.image.load(imagem).convert_alpha()

    def corta_imagem(self, frame ,altura, largura, escala):
        imagem = pygame.Surface((largura, altura)).convert_alpha()
        imagem.blit(self.sheet, (0, 0) , ((frame * largura), 0, largura, altura)) #Ultimo argumento é a área do frame que vai ser cortada
        imagem = pygame.transform.scale(imagem, (largura*escala, altura*escala)) #Aumenta a imagem
        imagem.set_colorkey('White') #Define a cor do fundo da imagem para ser transparente
        return imagem