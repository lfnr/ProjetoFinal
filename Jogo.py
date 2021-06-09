import sys
import pygame
import random
import math


pygame.init()
pygame.mixer.init()

WIDTH = 1600
HEIGHT = 960
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Jogo do canhão')

#-------------------------------------------
ORANGE= (255, 166, 0)


FPS = 30
ALVO_WIDTH = 100
ALVO_HEIGHT = 100
CANHAO_WIDTH = 150
CANHAO_HEIGHT = 150
LAUNCH_POINT = (CANHAO_WIDTH + 57, HEIGHT + 58 - CANHAO_HEIGHT)
LINE_LENGTH = 100
#Variaveis de tela


#Valor da gravidade 
gr = 1

#===================================
#Funções para funcionamento

def load_assets():
    assets = {}
    assets['background'] = pygame.image.load('jogo/Background.png').convert()
    assets['backgroundmain'] = pygame.image.load('jogo/backgroundmain.png').convert()
    assets['backgroundmain'] = pygame.transform.scale(assets['backgroundmain'], (WIDTH, HEIGHT))
    assets['alvo_png'] = pygame.image.load('jogo/alvo.png').convert_alpha()
    assets['alvo_png'] = pygame.transform.scale(assets['alvo_png'], (ALVO_WIDTH, ALVO_HEIGHT))
    assets['canhao_png'] = pygame.image.load('jogo/canhao.png').convert_alpha()
    assets['canhao_png'] = pygame.transform.scale(assets['canhao_png'], (CANHAO_WIDTH, CANHAO_HEIGHT))
    assets['tiro_png'] = pygame.image.load('jogo/tiro.png').convert_alpha()
    assets['tiro_png'] = pygame.transform.scale(assets['tiro_png'], (50, 50))


    return assets




class Canhao(pygame.sprite.Sprite):
    def __init__(self, groups, assets):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['canhao_png']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (CANHAO_WIDTH, HEIGHT + 100 - CANHAO_HEIGHT)
        self.groups = groups
        self.assets = assets

        # Só será possível atirar uma vez a cada 2000 milissegundos
        self.last_shot = pygame.time.get_ticks()
        self.shoot_ticks = 500
              
            
        
class AlvoMovel(pygame.sprite.Sprite):
    def __init__(self, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['alvo_png']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speedy = random.randint(5, 20) 
        self.rect.x = WIDTH - 100 #Dimensões da tela. É pra ser fixo
        self.rect.y += self.speedy


    #tentativa de fazer ele subir quando atingir o fim da tela
    def update(self):
        self.rect.y += self.speedy

        if self.rect.bottom > HEIGHT or self.rect.top < 0:
            self.speedy = self.speedy*-1

    def checkMorre(self, tiro):
        if self.rect.colliderect(tiro.rect):
            self.kill()
            
            
            
            
class Alvo(pygame.sprite.Sprite):
    def __init__(self, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['alvo_png']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 100 #Dimensões da tela. É pra ser fixo
        self.rect.y = random.randint(250, HEIGHT) #Dimensões da tela
    
    def checkMorre(self, tiro):
        if self.rect.colliderect(tiro.rect):
            self.kill()

        
class Tiro(pygame.sprite.Sprite):
    # Construtor da classe.
    def __init__(self, assets, velx, vely):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['tiro_png']

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.velx = velx
        self.vely = vely



        # Coloca no lugar inicial definido em x, y do constutor
        self.rect.centerx = LAUNCH_POINT[0] #Alterar valor baseado nas dimensões da tela
        self.rect.centery = LAUNCH_POINT[1]


    def update(self):

        self.rect.x += self.velx
        self.vely += gr
        self.rect.y += self.vely
        #Aqui que eu altero a gravidade

        # Se o tiro passar do inicio da tela, morre.
        if self.rect.right > WIDTH + self.rect.width:
            self.kill()


  
