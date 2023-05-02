import pygame
import random
import pandas as pd

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

class TelaInicial():
    """ Tela inicial do jogo.
    
    ...

    Atributos
    ---------
    dicionario : dict
        dicionário com os assets do jogo
    tela : pygame.Surface
        superfície que representa a tela
    fonte e fonte2: pygame.font.Font
        fonte utilizada para escrever o texto
    texto : pygame.Surface
        superfície que contém o texto que está sendo escrito
    texto_pos_x : int
        posição x do texto
    logo : pygame.Surface
        superfície que contém o logo do jogo
    fundo : pygame.Surface
        superfície que contém o fundo do jogo
    chao : pygame.Surface
        superfície que contém o chão do jogo
    musica_tela_inicial_tocando : bool
        variável que indica se a música da tela inicial está tocando
    tem_que_trocar : bool
        variável que indica se a tela deve ser trocada
    """
    def __init__(self, assets):
        self.dicionario = assets
        self.tela = assets['tela']
        self.fonte = pygame.font.Font(assets['fonte'], 50)
        self.fonte2 = assets['fonte2']
        self.texto2 = self.fonte2.render('Quando estiver pronto, aperte ENTER', True, (255, 230, 0))
        self.texto3 = self.fonte2.render('Clique e escreva seu apelido na caixa de texto.', True, (255, 230, 0))
        self.caixa_de_texto = CaixaTexto(self.fonte2, assets)
        self.texto2_pos_x = 640 - self.texto2.get_rect()[2] / 2
        self.texto3_pos_x = 640 - self.texto3.get_rect()[2] / 2

        
        self.logo = pygame.transform.scale(pygame.image.load('jogo/assets/imagens/logo.png'), (812, 98))

        self.fundo = assets['fundo']
        self.chao = assets['ground']

        self.musica_tela_inicial_tocando = False

        self.tem_que_trocar = False

        self.tela_tabela = False
        
        self.erro = False

        self.botao_som = pygame.mixer.Sound('jogo/assets/audio/botao_som.mp3')

    def desenha(self):
        self.tela.fill((255, 255, 255))

        self.tela.blit(self.fundo, (0, 0))
        self.tela.blit(self.chao, (0, 620))

        self.tela.blit(self.logo, (234, 250))

        self.tela.blit(self.texto2, (self.texto2_pos_x, 400))
        self.tela.blit(self.texto3, (self.texto3_pos_x, 368))

        if self.erro:
            self.texto4_pos_x = 640 - self.texto4.get_rect()[2] / 2
            self.tela.blit(self.texto4, (self.texto4_pos_x, 580))

        self.caixa_de_texto.desenha(self.tela)
        pygame.display.update()

    def update(self, assets):
        if not self.musica_tela_inicial_tocando:
            pygame.mixer_music.load('jogo/assets/audio/musica_inicial.mp3')
            pygame.mixer_music.set_volume(0.2)
            pygame.mixer_music.play()
            self.musica_tela_inicial_tocando = True

        for event in pygame.event.get():
            self.caixa_de_texto.escreve(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if assets['usuario_atual'] != '':
                        self.botao_som.play()
                        self.tem_que_trocar = True

                    elif self.erro == False:
                        self.texto4 = self.fonte2.render('Escreva seu nome primeiro!', True, (255, 255,255))
                        self.erro = True
        return True
    
    """ Troca a tela para a tela de instruções caso o usuário aperte ENTER."""
    def troca_tela(self):
        if self.tem_que_trocar:
            return TelaInstrucoes(self.dicionario)
        else:
            return self
        
class TelaInstrucoes():
    """ Tela de instruções do jogo. (Semelhante a tela inicial)"""
    def __init__(self, assets):
        self.dicionario = assets
        self.tela = assets['tela']
        self.fonte = pygame.font.Font(assets['fonte'], 50)
        self.fonte2 = assets['fonte2']
        self.fonte2_grande = assets['fonte2_grande']

        self.texto2 = self.fonte2_grande.render('COMO JOGAR:', True, (255, 230, 0))
        self.texto2_pos_x = 640 - self.texto2.get_rect()[2] / 2

        self.texto3 = self.fonte2.render('- Pressione "ESPAÇO" para pular', True, (255, 230, 0))
        self.texto3_pos_x = 640 - self.texto3.get_rect()[2] / 2

        self.texto4 = self.fonte2.render('- Pressione "BOTÃO ESQUERDO DO MOUSE" para atirar', True, (255, 230, 0))
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

        self.botao_som = pygame.mixer.Sound('jogo/assets/audio/botao_som.mp3')

        self.tem_que_trocar = False

    def desenha(self):
        self.tela.fill((255, 255, 255))

        self.tela.blit(self.fundo, (0, 0))
        self.tela.blit(self.chao, (0, 620))

        self.tela.blit(self.texto2, (self.texto2_pos_x, 100))
        self.tela.blit(self.texto3, (self.texto3_pos_x, 220))
        self.tela.blit(self.texto4, (self.texto4_pos_x, 290))
        self.tela.blit(self.texto5, (self.texto5_pos_x, 360))
        self.tela.blit(self.texto6, (self.texto6_pos_x, 430))
        self.tela.blit(self.texto7, (self.texto7_pos_x, 550))
        pygame.display.update()

    def update(self, assets):
        if not self.musica_tela_inicial_tocando:
            pygame.mixer_music.load('jogo/assets/audio/musica_inicial.ogg')
            pygame.mixer_music.set_volume(0.3)
            pygame.mixer_music.play()
            self.musica_tela_inicial_tocando = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.botao_som.play()
                    self.tem_que_trocar = True
        return True
    
    def troca_tela(self):
        if self.tem_que_trocar:
            return TelaJogo(self.dicionario)
        else:
            return self

class TelaJogo():
    """ Tela do jogo.
    Essa tela é responsável por atualizar os estados do jogo e desenhar os
    elementos na tela.

    ...

    Atributos
    ----------
    dicionario : dict
        dicionario com todos os assets do jogo
    tela : pygame.Surface
        superfície onde os elementos serão desenhados
    fonte : pygame.font.Font
        fonte usada para escrever na tela
    jogador : Jogador()
        classe do jogador
    scroll: int
        valor do scroll do fundo ou chao
    tiles : int
        quantidade de tiles do fundo ou chao
    pode_spawnar : bool
        variável que controla o spawn dos monstros
    Clock : pygame.time.Clock
        objeto que controla os fps do jogo
    tempo : int
        tempo do jogo
    tem_que_trocar : bool
        variável que controla a troca de tela 
    tiros : sprite.Group()
        grupo de tiros, usado para a colisão e desenhar os tiros
    As listas contém os objetos do jogo
    Os timers e os cooldowns determinam o tempo para certa ação acontecer
    """
    def __init__(self, assets):
        self.fonte = pygame.font.Font(assets['fonte'], 50)
        self.dicionario = assets
        #Adicionei essas imagens so para testar e dps mudar
        self.fundo = assets['fundo']
        self.chao = assets['ground']
        self.tela = assets['tela']

        self.fonte2 = assets['fonte2']
        

        self.tem_que_trocar = False
        self.Clock = pygame.time.Clock() #https://www.pygame.org/docs/ref/time.html#pygame.time.Clock

        #fonte: https://youtu.be/ARt6DLP38-Y
        self.scroll_fundo = 0
        self.tiles_fundo = 1280 // self.fundo.get_width() + 1

        self.scroll_chao = 0
        self.tiles_chao = 1280 // self.chao.get_width() + 1

        self.lista_de_inimigos = []
        self.tempo = 0
        self.pode_spawnar = True
        self.pode_spawnar_morcego = True

        self.jogador = Jogador()
        self.tiros = pygame.sprite.Group()

        self.lista_explosoes = []

        self.musica_jogo_tocando = False

        #Texto das vidas
        self.texto_vidas = pygame.transform.scale_by(self.fonte2.render(chr(9829) * self.jogador.vidas, True, (255, 0, 0)), 1.5)
        self.texto_vidas_max = pygame.transform.scale_by(self.fonte2.render(chr(9829) * 3, True, (0, 0, 0)), 1.5)

        self.pontuacao = 0
        self.texto_pontuacao = self.fonte2.render('Current score: ' + str(self.pontuacao), True, (255, 230, 0))

        """
        Com a biblioteca pandas, é possível ler o arquivo usuarios.csv
        e ordenar os usuários por score, do maior para o menor.
        Depois, o arquivo é reescrito com os usuários ordenados.
        Por fim, o highscore é atualizado.
        """
        df = pd.read_csv('usuarios.csv')
        df = df.sort_values(by=['score'], ascending=False)
        df.to_csv('usuarios.csv', index=False)
        if len(df) > 0:
            assets['highscore'] = df.iloc[0]['score']

        self.timer_pontuacao_comeco = 0
        self.texto_highscore = self.fonte2.render('High score: ' + str(assets['highscore']), True, (255, 230, 0))

        self.timer_recarga_municao_comeco = 0
        self.texto_municao = self.fonte2.render('Municao: ' + str(self.jogador.municoes), True, (255, 230, 0))

        self.lista_de_vidas = []
        self.timer_vidas_comeco = 0
        
        self.lista_objetos_fundo = []
        self.lista_objetos_fundo.append(ObjetoFundo(3))
        self.timer_objetos_fundo_comeco = 3

        self.cooldown_spawn_demonio = 2
        
        
    #Ajuda do Ninja Marcelo
    def salvar_highscore(self, assets, score):
        #Le o arquivo csv
        df = pd.read_csv('usuarios.csv', sep=',')
        #Adiciona ao dataframe o novo usuario e sua pontuacao
        df = df._append({'player': assets['usuario_atual'], 'score': score}, ignore_index=True)
        #Salva o arquivo csv com o dataframe
        df.to_csv('usuarios.csv', sep=',', index=False)

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

        #Desenha os objetos do fundo
        for objeto in self.lista_objetos_fundo:
            objeto.update()
            self.tela.blit(objeto.image, objeto.rect)

        #Vidas
        self.tela.blit(self.texto_vidas_max, (7, 0))
        self.tela.blit(self.texto_vidas, (7, 0))

        #Score
        self.tela.blit(self.texto_pontuacao, (1273 - self.texto_pontuacao.get_width(), 40))

        #High score
        self.tela.blit(self.texto_highscore, (1273 - self.texto_highscore.get_width(), 10))

        for vida in self.lista_de_vidas:
            vida.update()
            self.tela.blit(vida.image, vida.rect)

        #Desenha os inimigos
        for inimigo in self.lista_de_inimigos:
            inimigo.update()
            self.tela.blit(inimigo.image, inimigo.rect)
        
        #Desenha o jogador
        self.jogador.update()
        self.tela.blit(self.jogador.image, self.jogador.rect)

        #Desenha as explosoes
        for explosao in self.lista_explosoes:
            explosao.update()
            self.tela.blit(explosao.image, explosao.rect)

        self.tiros.update()
        self.tiros.draw(self.tela)

        self.Clock.tick(60) #https://www.pygame.org/docs/ref/time.html#pygame.time.Clock.tick

        self.tela.blit(self.texto_municao, (7, 40))

        pygame.display.update()

    def update(self, assets):
        #Tempo do jogo
        relogio = pygame.time.get_ticks() // 1000

        if not self.musica_jogo_tocando:
            pygame.mixer_music.load('jogo/assets/audio/musica_jogo.mp3')
            pygame.mixer_music.set_volume(0.3)
            pygame.mixer_music.play()
            self.musica_jogo_tocando = True


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            #Atira
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.jogador.municoes > 0:
                    self.tiros.add(Tiro(self.jogador.rect.centery))
                    #Som do tiro
                    Tiro(self.jogador.rect.centery).som.play()
                    self.jogador.municoes -= 1
                    self.texto_municao = self.fonte2.render('Municao: ' + str(self.jogador.municoes), True, (255, 230, 0))
            self.jogador.pulo_jogador(event)
        
        #Itera a lista de inimigos
        for inimigo in self.lista_de_inimigos:
            #Remove os inimigos que colidiram e diminui a vida do jogador
            if self.jogador.colisao_jogador(inimigo):
                self.lista_de_inimigos.remove(inimigo)
                self.texto_vidas = pygame.transform.scale_by(self.fonte2.render(chr(9829) * self.jogador.vidas, True, (255, 0, 0)), 1.5)
            #Remove os inimigos que sairam da tela
            if inimigo.rect.centerx < -50:
                self.lista_de_inimigos.remove(inimigo)
            #Remove os inimigos que colidiram com os tiros
            if pygame.sprite.spritecollide(inimigo, self.tiros, True, pygame.sprite.collide_mask):
                self.lista_explosoes.append(Explosao(inimigo.rect.centerx, inimigo.rect.centery))
                self.lista_de_inimigos.remove(inimigo)
                Jogador().pontuou_som.play()
                #Adiciona pontos de acordo com o tipo de inimigo
                if inimigo.tipo == 'morcego':
                    self.pontuacao += 100
                elif inimigo.tipo == 'fantasma':
                    self.pontuacao += 50
                elif inimigo.tipo == 'demonio':
                    self.pontuacao += 25
                self.texto_pontuacao = self.fonte2.render('Current score: ' + str(self.pontuacao), True, (255, 230, 0))


        #Animação da explosão
        for explosao in self.lista_explosoes:
            if explosao.frame_atual == 7:
                #Remove a explosão da lista caso sua animação termine
                self.lista_explosoes.remove(explosao)

        #Spawna inimigos a cada 2 segundos
        if relogio % self.cooldown_spawn_demonio == 0 and self.pode_spawnar and relogio != 0:
            self.spawn_inimigo()
            self.pode_spawnar = False
            self.tempo = relogio

        #Evita que o inimigo nasça em cima do outro
        if self.tempo != relogio:
            self.pode_spawnar = True
            self.pode_spawnar_morcego = True

        #Spawn Morcegos a cada 5 segundos
        if relogio % 5 == 0 and self.pode_spawnar_morcego and relogio != 0:
            self.lista_de_inimigos.append(Morcego())
            self.pode_spawnar_morcego = False
            self.tempo = relogio

        #Spawn Coracoes
        self.timer_vidas_fim = pygame.time.get_ticks() // 1000
        if self.timer_vidas_fim - self.timer_vidas_comeco >= 15:
            self.lista_de_vidas.append(Coracao())
            self.timer_vidas_comeco = self.timer_vidas_fim

        #Colisão com coração
        for vida in self.lista_de_vidas:
            if pygame.sprite.collide_mask(self.jogador, vida):
                self.lista_de_vidas.remove(vida)
                if self.jogador.vidas < 3:
                    self.jogador.vidas += 1
                    Coracao().som.play()
                self.texto_vidas = pygame.transform.scale_by(self.fonte2.render(chr(9829) * self.jogador.vidas, True, (255, 0, 0)), 1.5)


        #Jogador morre
        if self.jogador.vidas <=0:
            self.tem_que_trocar = True
            assets['pontuacao'] = self.pontuacao
            self.salvar_highscore(assets, self.pontuacao)
 
        #Pontuação
        self.timer_pontuacao_fim = pygame.time.get_ticks() // 1000

        #A cada 3 segundos adiciona 5 pontos
        if self.timer_pontuacao_fim - self.timer_pontuacao_comeco >= 3:
            self.pontuacao += 5
            self.texto_pontuacao = self.fonte2.render('Current score: ' + str(self.pontuacao), True, (255, 230, 0))
            self.timer_pontuacao_comeco = self.timer_pontuacao_fim
        #Atualiza o highscore
        if self.pontuacao > assets['highscore']:
            assets['highscore'] = self.pontuacao
            self.texto_highscore = self.fonte2.render('High score: ' + str(assets['highscore']), True, (255, 230, 0))

        #Municao
        self.timer_recarga_municao_fim = pygame.time.get_ticks() // 1000

        #A cada 7 segundos recarrega uma munição caso o jogador tenha menos de 3 munições
        if self.timer_recarga_municao_fim - self.timer_recarga_municao_comeco >= 7 and self.jogador.municoes < 3:
            self.jogador.municoes += 1
            self.timer_recarga_municao_comeco = self.timer_recarga_municao_fim
            self.texto_municao = self.fonte2.render('Municao: ' + str(self.jogador.municoes), True, (255, 230, 0))

        #Objetos fundo
        self.timer_objetos_fundo_fim = pygame.time.get_ticks() // 1000
        #A cada 3 segundos adiciona um objeto fundo
        if self.timer_objetos_fundo_fim - self.timer_objetos_fundo_comeco >= 3:
            #Aleatoriza o objeto que aparecerá
            index_objeto = random.randint(0, 3)
            self.lista_objetos_fundo.append(ObjetoFundo(index_objeto))
            self.timer_objetos_fundo_comeco = self.timer_objetos_fundo_fim


        
            
        return True
    def spawn_inimigo(self):
        #Define se vai ser fantasma ou demônio e adiciona a lista de inimigos
        if random.randint(0, 1):
            condicao = True
        else: condicao = False
        self.lista_de_inimigos.append(Inimigo(condicao))
    

    def troca_tela(self):
        if self.tem_que_trocar:
            return TelaGameOver(self.dicionario)
        else:
            return self
        
class Tabela():
    """Classe que cria a tabela de ranking"""
    def __init__(self, assets):
        self.dicionario = assets
        self.tela = assets['tela']

        self.fonte2 = assets['fonte2']
        self.fonte2_grande = assets['fonte2_grande']

        self.fonte = assets['fonte']
        self.texto = self.fonte2.render('Pressione "ESPAÇO" para reiniciar ou "ESC" PARA SAIR ' , True, (250, 250, 250))
        self.texto_pos_x = 640 - self.texto.get_rect()[2] / 2

        self.texto2 = self.fonte2_grande.render('RANKING:' , True, ((255, 230, 0)))
        self.texto2_pox_x = 640 - self.texto2.get_rect()[2] / 2

        self.lista_de_usuarios = []
        self.nomes = []
        df = pd.read_csv('usuarios.csv')
        
        #Ordem decrescente
        df = df.sort_values(by=['score'], ascending=False)

        df.to_csv('usuarios.csv', index=False)

        
        """Utiliza o pandas para ler o arquivo csv e criar uma variável que é um texto com os 5 primeiros colocados na tela"""
        for i in range(5):
            if i < len(df):
                #Escreve o nome do player ao lado da sua pontuacao em forma de tabela
                if df.iloc[i]['player']:
                    texto = self.fonte2.render(str(i+1) + ' - ' + str(df.iloc[i]['player']) + ' - ' + str(df.iloc[i]['score']), True, (255, 255, 255))
                    self.lista_de_usuarios.append(texto)

        self.fundo = assets['fundo']
        self.chao = assets['ground']

        self.musica_tela_inicial_tocando = False

        self.tem_que_trocar = False

        self.botao_som = pygame.mixer.Sound('jogo/assets/audio/botao_som.mp3')

    def desenha(self):
        self.tela.fill((255, 255, 255))

        self.tela.blit(self.fundo, (0, 0))
        self.tela.blit(self.chao, (0, 620))
        self.tela.blit(self.texto, (self.texto_pos_x, 225))
        self.tela.blit(self.texto2, (self.texto2_pox_x, 150))
        
        for player in self.lista_de_usuarios:
            self.texto_player_pos_x = 640 - player.get_rect()[2] / 2
            self.tela.blit(player, (self.texto_player_pos_x, 300 + 50 * self.lista_de_usuarios.index(player)))

        pygame.display.update()

    def update(self, assets):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.botao_som.play()
                    self.tem_que_trocar = True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
        return True
    
    def troca_tela(self):
        if self.tem_que_trocar:
            return TelaInicial(self.dicionario)
        else:
            return self
        
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

class TelaGameOver():
    """Classe que representa a tela de game over
        Texto e fundo semelhante as outras telas.
    """
    def __init__(self, assets):
        self.dicionario = assets
        self.tela = assets['tela']
        self.fonte = pygame.font.Font(assets['fonte'], 50)
        self.fonte2 = assets['fonte2']
        self.fonte2_grande = assets['fonte2_grande']
        self.fonte2_xgrande = assets['fonte2_xgrande']

        self.texto2 = self.fonte2_xgrande.render('GAME OVER', True, (255, 41, 41))
        self.texto2_pos_x = 640 - self.texto2.get_rect()[2] / 2

        self.texto3 = self.fonte2.render('Pressione "ESPAÇO" para reiniciar, "ESC" PARA SAIR ou' , True, (250, 250, 250))
        self.texto3_pos_x = 640 - self.texto3.get_rect()[2] / 2

        self.texto6 = self.fonte2.render('"TAB" para acessar o ranking de jogadores' , True, (250, 250, 250))
        self.texto6_pos_x = 640 - self.texto6.get_rect()[2] / 2

        self.texto4 = self.fonte2.render('High score: ' + str(assets['highscore']), True, (250, 250, 250))
        self.texto4_pos_x = 640 - self.texto4.get_rect()[2] / 2
        
        self.texto5 = self.fonte2.render('Sua pontuação: ' + str(assets['pontuacao']), True, (250, 250, 250))
        self.texto5_pos_x = 640 - self.texto5.get_rect()[2] / 2

        self.fundo = assets['fundo']
        self.chao = assets['ground']

        #Variáveis para controlar a troca de tela
        self.proxima_tela = None

        self.musica_tela_jogo_tocando = True

        self.botao_som = pygame.mixer.Sound('jogo/assets/audio/botao_som.mp3')

        self.tem_que_trocar = False

    def desenha(self):
        self.tela.fill((0, 0, 0))

        self.tela.blit(self.texto2, (self.texto2_pos_x, 250))
        self.tela.blit(self.texto4, (self.texto4_pos_x, 350))
        self.tela.blit(self.texto5, (self.texto5_pos_x, 400))
        self.tela.blit(self.texto3, (self.texto3_pos_x, 470))
        self.tela.blit(self.texto6, (self.texto6_pos_x, 500))
        

        pygame.display.update()

    def update(self, assets):
        if not self.musica_tela_jogo_tocando:
            pygame.mixer_music.load('jogo/assets/musica_jogo.ogg')
            pygame.mixer_music.set_volume(0.4)
            pygame.mixer_music.play()
            self.musica_tela_inicial_tocando = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.botao_som.play()
                    self.tem_que_trocar = True
                    #Proxima tela é a tela inicial
                    self.proxima_tela = TelaInicial(self.dicionario)

                elif event.key == pygame.K_TAB:
                    self.botao_som.play()
                    self.tem_que_trocar = True
                    #Proxima tela é a tabela
                    self.proxima_tela = Tabela(self.dicionario)

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False
        return True
    
    def troca_tela(self):
        if self.tem_que_trocar:
            return self.proxima_tela
        else:
            return self
        
#Fonte: https://www.youtube.com/watch?v=nXOVcOBqFwM&ab_channel=CodingWithRuss
class SpriteSheet:
    """Classe que corta as imagens do spritesheet
    
    ...

    Atributos
    ---------
    sheet : pygame.Surface
        Imagem que será cortada
    """
    def __init__(self, imagem):
        self.sheet = pygame.image.load(imagem).convert_alpha()

    def corta_imagem(self, frame ,altura, largura, escala):
        """Corta a imagem do spritesheet
        
        ...

        Parâmetros
        ----------
        frame : int
            Número do frame que será cortado
        altura : int
            Altura do frame
        largura : int
            Largura do frame
        escala : int
            Escala que a imagem será aumentada
        """
        imagem = pygame.Surface((largura, altura)).convert_alpha()

        #Blita a imagem cortada na superfície, ultimo argumento é a área retangular (x, y, lagura, altura) do frame que vai ser cortada 
        #(os spritesheets são organizados em linhas)
        imagem.blit(self.sheet, (0, 0) , ((frame * largura), 0, largura, altura)) 
        imagem = pygame.transform.scale(imagem, (largura*escala, altura*escala)) #Aumenta a imagem
        imagem.set_colorkey('White') #Define a cor do fundo da imagem para ser transparente
        return imagem
    
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