import pygame

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
    