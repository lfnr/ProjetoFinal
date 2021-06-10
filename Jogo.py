import sys
import pygame
import random
import math


pygame.init()
pygame.mixer.init()

WIDTH = 1600
HEIGHT = 960
window = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.mixer.music.load('jogo/Music-Rain.wav')
pygame.mixer.music.set_volume(0.4)

pygame.mixer.music.play(loops=-1)

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
#Valores da tela e posições


#Alterar valor da gravidade 
gr = 1


#Funções ============================================

#Assets
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


    assets['boom'] = pygame.mixer.Sound('jogo/canhao.mp3')
    pygame.mixer.Sound.set_volume(assets['boom'], 0.3)




    return assets


#Acompanha o mouse
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

#Desenha a linha da mira. Ela faz referência ao mousetracker, assim ela também segue o mouse.
def drawLine():
    endPoint = mousetracker()

    if endPoint != None:
        pygame.draw.line(window, (0, 0, 0), LAUNCH_POINT, endPoint, 3)
    else:
        pygame.draw.line(window, (0, 0, 0), LAUNCH_POINT , (LAUNCH_POINT[0] + LINE_LENGTH, LAUNCH_POINT[1]), 3)


        
#Calcula a trahetória/ vetor velocidade do tiro.
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


#Classes ===========================================



class Canhao(pygame.sprite.Sprite):
    def __init__(self, groups, assets):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['canhao_png']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (CANHAO_WIDTH, HEIGHT + 100 - CANHAO_HEIGHT)
        self.groups = groups
        self.assets = assets






# Um dos dois tipos de alvo. Esse tem uma velocidde aleatória e move no eixo y.
class AlvoMovel(pygame.sprite.Sprite):
    def __init__(self, assets, dif):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['alvo_png']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speedy = random.randint(5, 20) 
        self.rect.x = WIDTH - 100 - dif #Dimensões da tela. É pra ser fixo
        self.rect.y += self.speedy


    #Faz ele alterar de sentido quando atinge os limites da tela.
    def update(self):
        self.rect.y += self.speedy

        if self.rect.bottom > HEIGHT or self.rect.top < 0:
            self.speedy = self.speedy*-1

    #Verifica colisão com o tiro
    def checkMorre(self, tiro):
        if self.rect.colliderect(tiro.rect):
            self.kill()



#Alvo fixo. Não se move
class Alvo(pygame.sprite.Sprite):
    def __init__(self, assets, dif):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['alvo_png']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 100 - dif #Dimensões da tela. É pra ser fixo
        self.rect.y = random.randint(250, HEIGHT - 75) #Dimensões da tela
    
    
    #Verifica colisão com o tiro.
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


#Utiliza como referencia o Launch point. Variavel definida no começo.

        self.rect.centerx = LAUNCH_POINT[0] 
        self.rect.centery = LAUNCH_POINT[1]

#Aqui a velocidade é afetada pela aceleração da gravidade. O valor dela foi ajustado para o jogo.
    def update(self):

        self.rect.x += self.velx
        self.vely += gr
        self.rect.y += self.vely
        #Aqui que eu altero a gravidade

        # Se o tiro passar do inicio da tela, morre.
        if self.rect.right > WIDTH + self.rect.width:
            self.kill()
        if self.rect.bottom > HEIGHT + self.rect.height:
            self.kill()
        



#Parte do menu =================================================================


# Main Menu

def mainmenu():
    

    assets = load_assets()
    loop = True
            
    #Escreve as mensagens na tela de inicio
    while loop:
        window.fill((0, 0, 0))  
        window.blit(assets['backgroundmain'], (0, 0))


        font = pygame.font.Font("freesansbold.ttf", 150)
        text_surf = font.render("Jogo do canhão", True, (196, 190, 0))
        text_rect = text_surf.get_rect(center=(WIDTH//2, 200))
        window.blit(text_surf, text_rect)


        font = pygame.font.Font("freesansbold.ttf", 30)
        text_surf = font.render("Pressione A para modo fácil", True, ORANGE)
        text_rect = text_surf.get_rect(center = (WIDTH//2, 400))
        window.blit(text_surf, text_rect)

        font = pygame.font.Font("freesansbold.ttf", 30)
        text_surf = font.render("Pressione S para modo médio", True, ORANGE)
        text_rect = text_surf.get_rect(center = (WIDTH//2, 500))
        window.blit(text_surf, text_rect)

        font = pygame.font.Font("freesansbold.ttf", 30)
        text_surf = font.render("Pressione D para dificil", True, ORANGE)
        text_rect = text_surf.get_rect(center = (WIDTH//2, 600))
        window.blit(text_surf, text_rect)

        
        #Diferentes eventos para cada uma das teclas. Cada uma delas retorna uma dificuldade diferente que será utilizada como argumento da função da game screen.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    game_screen(1)  
                if event.key == pygame.K_s:
                    game_screen(2) 
                if event.key == pygame.K_d:
                    game_screen(3)           
            
        pygame.display.update()
        #Update



#Jogo ============================================


def game_screen(dificuldade):


    assets = load_assets()
 
    clock = pygame.time.Clock()




    # Criando um grupo de sprites
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

    #Listagem dos diferentes tipos de alvos. Eles serão usados la na frente.
    alvos_vivos = 2 * dificuldade
    todos_os_alvos = []

    alvos_moveis = []
    alvos_fixos = []



    # Criando alvos nos niveis baseado na dificuldade.
    #No facil só tem uma coluna. No médio tem duas. No hard tem 3.
    #Cada coluna tem 2 alvos: Um movel, e um fixo.
    if dificuldade == 1:
        alvo = Alvo(assets, 0)
        alvo_movel = AlvoMovel(assets, 0)
        all_sprites.add(alvo)
        all_sprites.add(alvo_movel)
        all_alvos.add(alvo)
        all_alvos.add(alvo_movel)
        todos_os_alvos.append(alvo)
        todos_os_alvos.append(alvo_movel)
        alvos_moveis.append(alvo_movel)
        alvos_fixos.append(alvo)


    elif dificuldade == 2:
        alvo = Alvo(assets, 0)
        alvo_movel = AlvoMovel(assets, 0)
        all_sprites.add(alvo)
        all_sprites.add(alvo_movel)
        all_alvos.add(alvo)
        all_alvos.add(alvo_movel)
        todos_os_alvos.append(alvo)
        todos_os_alvos.append(alvo_movel)
        alvos_moveis.append(alvo_movel)
        alvos_fixos.append(alvo)
        
        alvo = Alvo(assets, 130)
        alvo_movel = AlvoMovel(assets, 130)
        all_sprites.add(alvo)
        all_sprites.add(alvo_movel)
        all_alvos.add(alvo)
        all_alvos.add(alvo_movel)
        todos_os_alvos.append(alvo)
        todos_os_alvos.append(alvo_movel)
        alvos_moveis.append(alvo_movel)
        alvos_fixos.append(alvo)
    else:

        alvo = Alvo(assets, 0)
        alvo_movel = AlvoMovel(assets, 0)
        all_sprites.add(alvo)
        all_sprites.add(alvo_movel)
        all_alvos.add(alvo)
        all_alvos.add(alvo_movel)
        todos_os_alvos.append(alvo)
        todos_os_alvos.append(alvo_movel)
        alvos_moveis.append(alvo_movel)
        alvos_fixos.append(alvo)

        alvo = Alvo(assets, 130)
        alvo_movel = AlvoMovel(assets, 130)
        all_sprites.add(alvo)
        all_sprites.add(alvo_movel)
        all_alvos.add(alvo)
        all_alvos.add(alvo_movel)
        todos_os_alvos.append(alvo)
        todos_os_alvos.append(alvo_movel)
        alvos_moveis.append(alvo_movel)
        alvos_fixos.append(alvo)

        alvo = Alvo(assets, 260)
        alvo_movel = AlvoMovel(assets, 260)
        all_sprites.add(alvo)
        all_sprites.add(alvo_movel)
        all_alvos.add(alvo)
        all_alvos.add(alvo_movel)
        todos_os_alvos.append(alvo)
        todos_os_alvos.append(alvo_movel)
        alvos_moveis.append(alvo_movel)
        alvos_fixos.append(alvo)


    PLAYING = 1
    state = PLAYING
    
    
    #Tiro de referencia.
    novo_tiro = None

    
    #Numero de tiros que o jogador pode usar. Ele perde se não matar os alvos com os 4 que tem.
    tiros_restantes = 4

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

                        #Verifica se tem um tiro no jogo que ainda não foi morto pelos limites da janela de jogo.
                        #Se ainda tiver um tiro vivo, não pode atirar.
                        #Ele também toca o som de tiro de canhão.
                        if novo_tiro == None:
                            if tiros_restantes > 0:
                                velx, vely = calculatePower(60)
                                tiros_restantes -= 1
                                

                                assets['boom'].play()
                                novo_tiro = Tiro(assets, velx, -vely)
                                groups['all_sprites'].add(novo_tiro)
                                groups['all_tiros'].add(novo_tiro)

            

        # ----- Atualiza estado do jogo
        # Atualizando a posição dos alvos
        all_sprites.update()


        #Verifica a colisão entre alvos.
        #Se eles colidirem, o alvo movel troca seu sentido.
        for am in alvos_moveis:

            for af in alvos_fixos:
                if af.rect.colliderect(am.rect):
                    am.speedy = am.speedy * -1
            
        #Faz a contagem de alvos vivos na tela. Se alvos vivos for = 0, jogo se encerra.
        if novo_tiro != None:  
            for am in alvos_moveis:
                am.checkMorre(novo_tiro)
                if novo_tiro.rect.colliderect(am.rect):
                    alvos_moveis.remove(am)
                    alvos_vivos -= 1
            for af in alvos_fixos:
                af.checkMorre(novo_tiro)
                if novo_tiro.rect.colliderect(af.rect):
                    alvos_fixos.remove(af)
                    alvos_vivos -= 1
            #Mata os tiros quando passarem do limite da tela.
            if novo_tiro.rect.right > WIDTH + novo_tiro.rect.width:
                novo_tiro = None
            elif novo_tiro.rect.bottom > HEIGHT + novo_tiro.rect.height:
                novo_tiro = None
            

        #Aqui o jogo se encerra quando alvos vivos = 0, retornando ao main menu
        if alvos_vivos == 0:
            mainmenu()

        #Jogo se encerra quando tiros restantes for = 0 e não tiver nenhum tiro na tela.
        if tiros_restantes == 0 and novo_tiro == None:
            mainmenu()




        # ----- Cria a tela
        window.fill((0, 0, 0))  
        window.blit(assets['background'], (0, 0))
        all_sprites.draw(window)


        font = pygame.font.Font("freesansbold.ttf", 50)
        text_surf = font.render(f"Tiros restante: { tiros_restantes }", True, (0, 0, 0))
        text_rect = text_surf.get_rect(topleft=(100, 100))
        window.blit(text_surf, text_rect)


        #Desenha a linha de mira.
        drawLine()

        pygame.display.update()  # Mostra o novo frame para o jogador


mainmenu()
