import pygame


class TelaInicial():
    def __init__(self, assets):
        self.dic = assets
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
                if event.key == pygame.K_SPACE:
                    self.tem_que_trocar = True
        return True
    
    def troca_tela(self):
        if self.tem_que_trocar:
            return TelaJogo(self.dic)
        else:
            return self

class TelaJogo():
    def __init__(self, assets):
        self.fonte = pygame.font.Font(assets['fonte'], 50)
        self.texto = self.fonte.render('Tela Jogo', True, (0, 0, 0))
        self.dic = assets
        self.tela = assets['tela']
        self.tem_que_trocar = False
        self.x = 800
        self.y = 600

    def desenha(self):
        self.tela.fill((255, 255, 0))
        self.tela.blit(self.texto, (250, 0))
        pygame.draw.circle(self.tela, (0, 0, 0), (self.x, self.y), 50)
        pygame.display.update()


    def troca_tela(self):
        if self.tem_que_trocar:
            return TelaInicial(self.dic)
        else:
            return self


    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.tem_que_trocar = True
        self.x -= 1
        self.y -= 1
        return True
    