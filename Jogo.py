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



    def shoot(self):
        # Verifica se pode atirar
        now = pygame.time.get_ticks()
        # Verifica quantos ticks se passaram desde o último tiro.
        elapsed_ticks = now - self.last_shot

        # Se já pode atirar novamente...
        if elapsed_ticks > self.shoot_ticks:
            # Marca o tick da nova imagem.
            self.last_shot = now
            velx, vely = calculatePower(60)
            # A nova bala vai ser criada logo acima e no centro horizontal do canhão
            novo_tiro = Tiro(self.assets, velx, -vely)
            self.groups['all_sprites'].add(novo_tiro)
            self.groups['all_tiros'].add(novo_tiro)

              
            
        
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
            
            
            
            
class Alvo(pygame.sprite.Sprite):
    def __init__(self, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['alvo_png']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 100 #Dimensões da tela. É pra ser fixo
        self.rect.y = random.randint(150, HEIGHT -100) #Dimensões da tela

        
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
        if self.rect.right > WIDTH:
            self.kill()


  
