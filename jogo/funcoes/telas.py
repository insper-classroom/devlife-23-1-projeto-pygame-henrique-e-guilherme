import pygame
import random
import pandas as pd
from inimigos import Inimigo, Morcego
from jogador import Jogador
from sprites import Explosao, Tiro, ObjetoFundo, CaixaTexto, Coracao


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

        self.cooldown_spawn_demonio = 5

        self.nivel_dificuldade = 1
        self.nivel_dificuldade_timer_comeco = pygame.time.get_ticks() // 1000
        
        
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

        #Define o nivel de dificuldade
        self.nivel_dificuldade_timer_final = pygame.time.get_ticks() // 1000
        if self.nivel_dificuldade_timer_final - self.nivel_dificuldade_timer_comeco == 0:
            self.nivel_dificuldade = 1
        if self.nivel_dificuldade_timer_final - self.nivel_dificuldade_timer_comeco > 30:
            self.nivel_dificuldade = 2
        if self.nivel_dificuldade_timer_final - self.nivel_dificuldade_timer_comeco > 60:
            self.nivel_dificuldade = 3

        #Nivel de dificuldade 1
        if self.nivel_dificuldade == 1:
            #Spawna inimigos a cada 5 segundos
            if relogio % self.cooldown_spawn_demonio == 0 and self.pode_spawnar and relogio != 0:
                self.spawn_inimigo()
                self.pode_spawnar = False
                self.tempo = relogio

            #Evita que o inimigo nasça em cima do outro
            if self.tempo != relogio:
                self.pode_spawnar = True
                self.pode_spawnar_morcego = True

            #Spawn Morcegos a cada 10 segundos
            if relogio % 10 == 0 and self.pode_spawnar_morcego and relogio != 0:
                self.lista_de_inimigos.append(Morcego())
                self.pode_spawnar_morcego = False
                self.tempo = relogio

        #Nivel de dificuldade 2
        elif self.nivel_dificuldade == 2:
            #Spawna inimigos a cada 2 segundos
            self.cooldown_spawn_demonio = 2
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

        #Nivel de dificuldade 3
        elif self.nivel_dificuldade == 3:
            #Spawna inimigos a cada 1 segundos
            self.cooldown_spawn_demonio = 1
            if relogio % self.cooldown_spawn_demonio == 0 and self.pode_spawnar and relogio != 0:
                self.spawn_inimigo()
                self.pode_spawnar = False
                self.tempo = relogio

            #Evita que o inimigo nasça em cima do outro
            if self.tempo != relogio:
                self.pode_spawnar = True
                self.pode_spawnar_morcego = True

            #Spawn Morcegos a cada 1 segundos
            if relogio % 1 == 0 and self.pode_spawnar_morcego and relogio != 0:
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



