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

#===========================================
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



def mousetracker():
    mx, my = pygame.mouse.get_pos()

    try:
        a = math.atan((LAUNCH_POINT[1] - my)/(mx - LAUNCH_POINT[0]))

        if mx - LAUNCH_POINT[0] > 0 and LAUNCH_POINT[1] - my > 0:
            if 0 < a < math.pi:
                return int(LAUNCH_POINT[0] + LINE_LENGTH*math.cos(a)), int(LAUNCH_POINT[1] - LINE_LENGTH*math.sin(a))
        
        else:
            if mx - LAUNCH_POINT[0] < 0:
                return LAUNCH_POINT[0], LAUNCH_POINT[1] - LINE_LENGTH
            elif LAUNCH_POINT[1] - my < 0:
                return LAUNCH_POINT[0] + LINE_LENGTH, LAUNCH_POINT[1]

    except:
        pass

    
    
def calculatePower(length):
    mx, my = pygame.mouse.get_pos()

    if mx - LAUNCH_POINT[0] != 0:
        a = math.atan((LAUNCH_POINT[1] - my)/(mx - LAUNCH_POINT[0]))

        if mx - LAUNCH_POINT[0] > 0 and LAUNCH_POINT[1] - my > 0:
            if 0 < a < math.pi:
                return int(length*math.cos(a)), int(length*math.sin(a))
        
        else:
            if mx - LAUNCH_POINT[0] < 0:
                return 0, length
            elif LAUNCH_POINT[1] - my < 0:
                return length, 0
    
    else: return 0, length 



def drawLine():
    endPoint = mousetracker()

    if endPoint != None:
        pygame.draw.line(window, (0, 0, 0), LAUNCH_POINT, endPoint, 3)
    else:
        pygame.draw.line(window, (0, 0, 0), LAUNCH_POINT , (LAUNCH_POINT[0] + LINE_LENGTH, LAUNCH_POINT[1]), 3)

  
#=================================================
#Classes
    

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


#================================================================

#Parte do menu =================================================================


# Main Menu

def mainmenu():
    assets = load_assets()
    loop = True
            
    while loop:
        window.fill((0, 0, 0))  
        window.blit(assets['backgroundmain'], (0, 0))


        font = pygame.font.Font("freesansbold.ttf", 150)
        text_surf = font.render("Jogo do canhão", True, (196, 190, 0))
        text_rect = text_surf.get_rect(center=(WIDTH//2, 200))
        window.blit(text_surf, text_rect)


        font = pygame.font.Font("freesansbold.ttf", 30)
        text_surf = font.render("Pressione A para jogar", True, ORANGE)
        text_rect = text_surf.get_rect(midtop = (WIDTH//2, 5))
        window.blit(text_surf, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    game_screen(window)               
            
        pygame.display.update()
        

def game_screen(window):
    clock = pygame.time.Clock()

    assets = load_assets()



    # Criando as sprites
    all_sprites = pygame.sprite.Group()
    all_alvos = pygame.sprite.Group()
    all_alvo_movel = pygame.sprite.Group()
    all_tiros = pygame.sprite.Group()
    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_alvos'] = all_alvos
    groups['all_tiros'] = all_tiros
    groups['all_alvo_movel'] = all_alvo_movel

    # Criando o jogador
    player = Canhao(groups, assets)
    all_sprites.add(player)

    #Numero de alvos
    alvos_vivos = 2

    todos_os_alvos = []


    # Criando os alvos
    for i in range(1):
        alvo = Alvo(assets)
        alvo_movel = AlvoMovel(assets)
        all_sprites.add(alvo)
        all_sprites.add(alvo_movel)
        all_alvos.add(alvo)
        all_alvos.add(alvo_movel)
        todos_os_alvos.append(alvo)
        todos_os_alvos.append(alvo_movel)


    PLAYING = 1
    state = PLAYING

    novo_tiro = None

    # ===== Loop principal =====
    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Só verifica o teclado se está no estado de jogo
            if state == PLAYING:
                # Verifica se apertou alguma tecla.
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Verifica se pode atirar
                        now = pygame.time.get_ticks()
                        # Verifica quantos ticks se passaram desde o último tiro.
                        

                       
                        # Marca a força/velocidade da bala
                        velx, vely = calculatePower(60)
                        
                        #Cria novo tiro
                        novo_tiro = Tiro(assets, velx, -vely)
                        groups['all_sprites'].add(novo_tiro)
                        groups['all_tiros'].add(novo_tiro)


           # ----- Atualiza estado do jogo
        # Atualizando a posição dos alvos
        all_sprites.update()
            
        
        if alvo.rect.colliderect(alvo_movel.rect):
            alvo_movel.speedy = alvo_movel.speedy * -1

        if novo_tiro != None:  
            for a in todos_os_alvos:
                a.checkMorre(novo_tiro)
                if novo_tiro.rect.colliderect(a.rect):
                    todos_os_alvos.remove(a)
                    alvos_vivos -= 1
                
    

        if alvos_vivos == 0:
            mainmenu()



        # ----- Cria a tela
        window.fill((0, 0, 0))  
        window.blit(assets['background'], (0, 0))
        all_sprites.draw(window)

        #Linha da mira
        drawLine()

        pygame.display.update()  # Mostra o novo frame para o jogador

        
       #Roda o main menu
mainmenu()
