import pygame
from pygame.locals import *
from math import log as ln
from math import tan
from math import cos
from math import fabs
import matplotlib.pyplot as plt

# Constantes de altura e velocidade, obrigatórias para o funcionamento do simulador:

STAGE_HEIGHTS           =   [21, 38, 107, 122, 230, 240, 320, 350]
STAGE_VELOCITIES        =   [1405.0, 1705.0, 2710.0, 2890.0, 5110.0, 5080.0, 4240.0, 3480.0, 7800.0]

SCREEN_X, SCREEN_Y      =   (800, 600)  # Constantes de largura e altura da tela do simulador.

# Constantes que representam os sprites do foguete em seus diversos estágios:

BASE_IMAGE = pygame.image.load('base.png')
BASE_IMAGE = pygame.transform.scale(BASE_IMAGE, (122, 401))
BASE_RECT = BASE_IMAGE.get_rect()

RCKT_FIRST_STG_I = pygame.image.load('rocket_first_stage.png')
RCKT_FIRST_STG_I = pygame.transform.scale(RCKT_FIRST_STG_I, (44, 323))
RCKT_FIRST_STG_R = RCKT_FIRST_STG_I.get_rect()

RCKT_SECOND_STG_I = pygame.image.load('rocket_second_stage.png')
RCKT_SECOND_STG_I = pygame.transform.scale(RCKT_SECOND_STG_I, (44, 323))
RCKT_SECOND_STG_R = RCKT_SECOND_STG_I.get_rect()

RCKT_THIRD_STG_I = pygame.image.load('rocket_third_stage.png')
RCKT_THIRD_STG_I = pygame.transform.scale(RCKT_THIRD_STG_I, (44, 323))
RCKT_THIRD_STG_R = RCKT_THIRD_STG_I.get_rect()

RCKT_LAST_STG_I = pygame.image.load('rocket_last_stage.png')
RCKT_LAST_STG_I = pygame.transform.scale(RCKT_LAST_STG_I, (44, 323))
RCKT_LAST_STG_R = RCKT_LAST_STG_I.get_rect()

RCKT_SATELLITE_I = pygame.image.load('rocket_satellite_orbit.png')
RCKT_SATELLITE_I = pygame.transform.scale(RCKT_SATELLITE_I, (44, 323))
RCKT_SATELLITE_R = RCKT_SATELLITE_I.get_rect()

sprite_list = [RCKT_FIRST_STG_I, RCKT_FIRST_STG_I, RCKT_SECOND_STG_I, RCKT_SECOND_STG_I, RCKT_THIRD_STG_I, RCKT_THIRD_STG_I, RCKT_LAST_STG_I, RCKT_LAST_STG_I, RCKT_LAST_STG_I]

RCKT_TRHOWN_PART1_I = pygame.image.load('rocket_thrown_part1.png')
RCKT_TRHOWN_PART1_I = pygame.transform.scale(RCKT_TRHOWN_PART1_I, (44, 126))

RCKT_TRHOWN_PART2_I = pygame.image.load('rocket_thrown_part2.png')
RCKT_TRHOWN_PART2_I = pygame.transform.scale(RCKT_TRHOWN_PART2_I, (32, 88))

RCKT_TRHOWN_PART3_I = pygame.image.load('rocket_thrown_part3.png')
RCKT_TRHOWN_PART3_I = pygame.transform.scale(RCKT_TRHOWN_PART3_I, (29, 72))

pygame.init()   # Inicializa os módulos do Pygame.
pygame.display.set_caption('Rocket Launch Simulation')  # Altera o título da janela.

screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))  # Inicializa a janela principal.

global camera_x
camera_x = 0

global camera_y
camera_y = 0

# Funções da camera de visualização:
def get_camera_x():
    global camera_x
    return 0

def set_camera_x(new_x):
    global camera_x
    camera_x = new_x

def get_camera_y():
    global camera_y
    return 0

def set_camera_y(new_y):
    global camera_y
    camera_y = new_y

# Classe que representa uma parte do foguete que fora ejetada:
class ThrownPart():
    def __init__(self, sprite):
        self.image = sprite
        self.position = (0,0)
        self.rotation = 0

    def update(self, rotation):
        self.position = (self.position[0]-0.25, self.position[1]+0.5)

    def draw(self, screen):
        screen.blit(pygame.transform.rotate(self.image, -1*self.rotation), (self.position[0], self.position[1]))

# Classe que representa o grupo de sprites que formam uma animação:
class SpriteGroup(pygame.sprite.Sprite):
    def __init__(self, sprites):
        super(SpriteGroup, self).__init__()
        self.images = []
        [self.images.append(i) for i in sprites]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(5, 5, 20, 60)
        self.rotation = 0

    def update(self, pos, new_angle):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        if self.rotation < fabs(new_angle):
            self.rotation += new_angle*0.0001
        self.image = pygame.transform.rotate(self.images[self.index], -1*self.rotation)
        self.rect = pygame.Rect(pos[0], pos[1], 20, 60)

# Classe do foguete:
class Rocket():

    # Função inicializadora do foguete:
    def __init__(self):
        self.altitude = 0
        self.position = tuple((int(SCREEN_X/4), SCREEN_Y/1.125-RCKT_FIRST_STG_R.height))
        self.velocity = (0, 0)
        self.rotation = 0

    # Atualiza as propriedades do foguete:
    def update(self, new_velocity, new_angle):
        # Gradualmente atualiza a velocidade do foguete:
        if self.velocity[0] < new_velocity[0]:
            self.velocity = (self.velocity[0]+new_velocity[0]*0.0001, self.velocity[1])
        if self.velocity[1] < new_velocity[1]:
            self.velocity = (self.velocity[0], self.velocity[1]+new_velocity[1]*0.0001)

        # Gradualmente atualiza a rotação do foguete:
        if self.rotation < fabs(new_angle):
            self.rotation += new_angle*0.0001

        # Atualiza a posição do foguete baseada em sua velocidade:
        if self.altitude < SCREEN_Y/4:
            self.position = (self.position[0]+self.velocity[0]*0.01, self.position[1]-self.velocity[1]*0.01)
        self.altitude += self.velocity[1]*0.01
        set_camera_y(get_camera_y()+self.velocity[1]*0.01)
        set_camera_x(get_camera_x()+self.velocity[0]*0.01)

    # Desenha o foguete na tela de acordo com o estágio especificado:
    def draw(self, screen, stage):
        sprite = pygame.transform.rotate(sprite_list[current_stage], -1*self.rotation)
        screen.blit(sprite, (self.position[0]-get_camera_x(), self.position[1]+get_camera_y()))

    # Retorna a altitude atual do foguete:
    def get_altitude(self):
        return self.altitude

# Função que desenha as cores de fundo (em forma de gradiente) que representam o céu:
def fill_gradient(surface, color, gradient, rect=None, vertical=True, forward=True):
    if rect is None: rect = surface.get_rect()
    x1,x2 = rect.left, rect.right
    y1,y2 = rect.top, rect.bottom
    if vertical: h = y2-y1
    else:        h = x2-x1
    if forward: a, b = color, gradient
    else:       b, a = color, gradient
    rate = (
        float(b[0]-a[0])/h,
        float(b[1]-a[1])/h,
        float(b[2]-a[2])/h
    )
    fn_line = pygame.draw.line
    if vertical:
        for line in range(y1,y2):
            color = (
                min(max(a[0]+(rate[0]*(line-y1)),0),255),
                min(max(a[1]+(rate[1]*(line-y1)),0),255),
                min(max(a[2]+(rate[2]*(line-y1)),0),255)
            )
            fn_line(surface, color, (x1,line), (x2,line))
    else:
        for col in range(x1,x2):
            color = (
                min(max(a[0]+(rate[0]*(col-x1)),0),255),
                min(max(a[1]+(rate[1]*(col-x1)),0),255),
                min(max(a[2]+(rate[2]*(col-x1)),0),255)
            )
            fn_line(surface, color, (col,y1), (col,y2))

floor_color, ceil_color = (85,85,85), (176,196,222) # Cores iniciais do gradiente de fundo.

rocket = Rocket() # Objeto Foguete.
current_stage = 0 # Estágio inicial do foguete.
current_velocity = (0, 0) # Velocidade (x, y) do foguete antes de ser lançado.

# Posições dos fogos dos exaustores do foguete:
muzzle1_pos = (0, 0)
muzzle2_pos = (0, 0)
muzzle3_pos = (0, 0)

# Animação do fogo dos exaustores:
muzzle_sprites = [pygame.transform.scale(pygame.image.load('engine_muzzle\\muzzle'+str(i)+'.png'), (20, 60)) for i in range(1, 23)]
muzzle_group = SpriteGroup(muzzle_sprites)
muzzle_anim = pygame.sprite.Group(muzzle_group)

# Sprites das partes do foguete que são ejetadas:
rocket_thrown_part1 = ThrownPart(RCKT_TRHOWN_PART1_I)
rocket_thrown_part2 = ThrownPart(RCKT_TRHOWN_PART2_I)
rocket_thrown_part3 = ThrownPart(RCKT_TRHOWN_PART3_I)

last_stage = None
running = True
launch = False

while running:

    # Preenche o fundo com o gradiente que representa o céu:
    fill_gradient(screen, ceil_color, floor_color)
    
    # Atualiza os eventos de input do simulador:
    pygame.event.pump()

    # Verifica os eventos de input do simulador:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                launch = True

    # Desenha a base de lançamento:
    if rocket.get_altitude() < STAGE_HEIGHTS[0]*1000:
        screen.blit(BASE_IMAGE, (SCREEN_X/4-RCKT_LAST_STG_R.width-12, SCREEN_Y/1.125-RCKT_LAST_STG_R.height-40+rocket.get_altitude()*2))

    # Condição que determina o início do lançamento do foguete:
    if launch:

        # Define a posição do fogo dos exaustores no começo do lançamento do foguete:
        muzzle1_pos = (rocket.position[0]-get_camera_x()+2, rocket.position[1]+get_camera_y()+310)
        muzzle2_pos = (rocket.position[0]-get_camera_x()+12, rocket.position[1]+get_camera_y()+315)
        muzzle3_pos = (rocket.position[0]-get_camera_x()+22, rocket.position[1]+get_camera_y()+309)

        # Verifica a altitude do foguete e toma as ações necessárias como: ejetar partes, rotacionar foguete, etc...
        if (rocket.get_altitude() > SCREEN_Y/4 and rocket.get_altitude() <= STAGE_HEIGHTS[0]*1000):
            ceil_color, floor_color = (176,196,222), (176,196,222)
        elif (rocket.get_altitude() > STAGE_HEIGHTS[0]*1000 and rocket.get_altitude() <= STAGE_HEIGHTS[1]*1000):
            muzzle1_pos = (rocket.position[0]-get_camera_x()-2, rocket.position[1]+get_camera_y()+310)
            muzzle2_pos = (rocket.position[0]-get_camera_x()+8, rocket.position[1]+get_camera_y()+316)
            muzzle3_pos = (rocket.position[0]-get_camera_x()+18, rocket.position[1]+get_camera_y()+310)
            ceil_color, floor_color = (106,90,205), (176,196,222)
            current_stage = 1
        elif (rocket.get_altitude() > STAGE_HEIGHTS[1]*1000 and rocket.get_altitude() <= STAGE_HEIGHTS[2]*1000):
            muzzle2_pos = (rocket.position[0]-get_camera_x()+24-(current_stage*4), rocket.position[1]+get_camera_y()+200)
            rocket_thrown_part1.update(current_stage*12)
            rocket_thrown_part1.draw(screen)
            ceil_color, floor_color = (25,25,112), (106,90,205)
            current_stage = 2
        elif (rocket.get_altitude() > STAGE_HEIGHTS[2]*1000 and rocket.get_altitude() <= STAGE_HEIGHTS[3]*1000):
            ceil_color, floor_color = (25,25,112), (25,25,112)
            current_stage = 3
        elif (rocket.get_altitude() > STAGE_HEIGHTS[3]*1000 and rocket.get_altitude() <= STAGE_HEIGHTS[4]*1000):
            ceil_color, floor_color = (0,0,0), (25,25,112)
            rocket_thrown_part2.update(current_stage*12)
            rocket_thrown_part2.draw(screen)
            current_stage = 4
        elif (rocket.get_altitude() > STAGE_HEIGHTS[4]*1000 and rocket.get_altitude() <= STAGE_HEIGHTS[5]*1000):
            ceil_color, floor_color = (0,0,0), (12,12,56)
            current_stage = 5
        elif (rocket.get_altitude() > STAGE_HEIGHTS[5]*1000 and rocket.get_altitude() <= STAGE_HEIGHTS[6]*1000):
            ceil_color, floor_color = (0,0,0), (6,6,28)
            rocket_thrown_part3.update(current_stage*12)
            rocket_thrown_part3.draw(screen)
            current_stage = 6
        elif (rocket.get_altitude() > STAGE_HEIGHTS[6]*1000 and rocket.get_altitude() <= STAGE_HEIGHTS[7]*1000):
            current_stage = 7
        elif (rocket.get_altitude() > STAGE_HEIGHTS[7]*1000):
            current_stage = 8

        # Atualiza e desenha o fogo dos exaustores do foguete:
        if current_stage < 2:
            muzzle_anim.update(muzzle1_pos, current_stage*12)
            muzzle_anim.draw(screen)
            muzzle_anim.update(muzzle3_pos, current_stage*12)
            muzzle_anim.draw(screen)
        if current_stage < 3:
            muzzle_anim.update(muzzle2_pos, current_stage*12)
            muzzle_anim.draw(screen)

        # Atualiza os componentes do foguete:
        rocket.update((0, STAGE_VELOCITIES[current_stage]), current_stage*12)

        # Verifica a mudança de estágio:
        if current_stage != last_stage:

            print('\nEstagio', current_stage+1)

            if current_stage == 0:
                print('Iniciando processo de lançamento do foguete...')
            elif current_stage == 1:
                print('Inclinando foguete...')
            elif current_stage == 2:
                print('Ejetando o primeiro motor do foguete...')
                rocket_thrown_part1.position = (rocket.position[0], rocket.position[1]+200)
            elif current_stage == 3:
                print('Saindo da atmosfera...')
                rocket_thrown_part2.position = (rocket.position[0]+56, rocket.position[1]+130)
            elif current_stage == 4:
                print('Estamos fora da atmosfera!')
                print('Ejetando o segundo motor do foguete...')
            elif current_stage == 5:
                print('Estabilizando posicionamento...')
            elif current_stage == 6:
                print('Posicionamento estabilizado com sucesso!')
                print('Ejetando o terceiro motor do foguete...')
                rocket_thrown_part3.position = (rocket.position[0]+100, rocket.position[1]+70)
            elif current_stage == 7:
                print('Estabilizando orbita...')
            elif current_stage == 8:
                print('Orbita estabilizada com sucesso!')
                print('A missão de lançamento foi bem-sucedida!')
            
            print('Altitude:', rocket.get_altitude()/1000, 'km.')
            print('Velocidade:', STAGE_VELOCITIES[current_stage]*3.6, 'km/h.')
            last_stage = current_stage
    
    # Desenha o foguete na tela:
    rocket.draw(screen, current_stage)

    # Desenha todos os objetos na tela:
    pygame.display.flip()
