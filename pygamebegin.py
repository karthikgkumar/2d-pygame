import pygame
import os
pygame.font.init()
pygame.mixer.init()

VEL=5
WIDTH,HEIGHT=900,500
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("FIRST GAME")
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)
SPACESHIP_WIDTH,SPACESHIP_HEIGHT=55,40
BORDER=pygame.Rect(WIDTH//2-5,0,10,HEIGHT)
BULLETS_HIT_SOUND=pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))
BULLETS_FIRE_SOUND=pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))
HEALTH_FONT=pygame.font.SysFont('comicsans',40)
WINNER_FONT=pygame.font.SysFont('comicsans',100)

BULLET_VEL=7
MAX_BULLETS=4
FPS=60

YELLOW_HIT=pygame.USEREVENT+1
RED_HIT=pygame.USEREVENT+2

YELLOW_SPACESHIP_IMAGE=pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP_IMAGE=pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)

RED_SPACESHIP_IMAGE=pygame.image.load(os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP_IMAGE=pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)

SPACE=pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')),(WIDTH,HEIGHT))
def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
    WIN.blit(SPACE,(0,0))
    #WIN.fill(WHITE)#rgb
    pygame.draw.rect(WIN,BLACK,BORDER)

    red_health_text=HEALTH_FONT.render("HEALTH: "+ str(red_health),1,WHITE)
    yellow_health_text=HEALTH_FONT.render("HEALTH: "+ str(yellow_health),1,WHITE)

    WIN.blit(red_health_text,(WIDTH - red_health_text.get_width() - 10,10))
    WIN.blit(yellow_health_text,(10,10))
    WIN.blit(YELLOW_SPACESHIP_IMAGE,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP_IMAGE,(red.x,red.y))
    

    for bullets in red_bullets:
        pygame.draw.rect(WIN,RED,bullets)
    for bullets in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullets)
    
        
    pygame.display.update()

def yellow_handle_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x-VEL>0:#left
            yellow.x-=VEL
    if keys_pressed[pygame.K_d] and yellow.x+VEL+yellow.width<BORDER.x:#RIGHT
        yellow.x+=VEL
    if keys_pressed[pygame.K_w]:#up
        yellow.y-=VEL
    if keys_pressed[pygame.K_s]:#down
        yellow.y+=VEL
    
def red_handle_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x-VEL>BORDER.x+BORDER.width:#left
        red.x-=VEL
    if keys_pressed[pygame.K_RIGHT] and red.x+VEL+red.width<WIDTH:#RIGHT
        red.x+=VEL
    if keys_pressed[pygame.K_UP] and red.x-VEL>0:#up
        red.y-=VEL
    if keys_pressed[pygame.K_DOWN]:#down
        red.y+=VEL
def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x+=BULLET_VEL
        if red.colliderect(bullet):#both objects should be rect
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x>WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x-=BULLET_VEL
        if yellow.colliderect(bullet):#both objects should be rect
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x<0:
            red_bullets.remove(bullet)
def draw_winner(winner_text):
    draw_text=WINNER_FONT.render(winner_text,1,WHITE)
    WIN.blit(draw_text,(WIDTH/2- draw_text.get_width()/2,HEIGHT/2-draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
    
def main():
    red=pygame.Rect(700,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow=pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)

    red_bullets=[]
    yellow_bullets=[]
    red_health=10
    yellow_health=10
    
    clock=pygame.time.Clock()

    run=True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LCTRL and len(yellow_bullets)<MAX_BULLETS:
                    bullet=pygame.Rect(yellow.x+yellow.width,yellow.y+yellow.height//2,10,5)
                    yellow_bullets.append(bullet)
                    BULLETS_FIRE_SOUND.play()

                if event.key==pygame.K_RCTRL and len(red_bullets)<MAX_BULLETS:
                    bullet=pygame.Rect(red.x,red.y+red.height//2,10,5)
                    red_bullets.append(bullet)
                    BULLETS_FIRE_SOUND.play()
            if event.type==RED_HIT:
                red_health-=1
                BULLETS_HIT_SOUND.play()
            if event.type==YELLOW_HIT:
                yellow_health-=1
                BULLETS_HIT_SOUND.play()
        winner_text=""
        if red_health<=0:
            winner_text="yellow wins"
        if yellow_health<=0:
            winner_text="red wins"
        if winner_text != "":
            draw_winner(winner_text)
            break
    
        keys_pressed=pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed,red)
        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        
        draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health)
    
    
    


    main()    
    #pygame.quit()

if __name__=="__main__":
    main()
 
