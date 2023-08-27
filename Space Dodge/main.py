import pygame
import time
import random
pygame.font.init()

### Configurações da janela do jogo ###
width, height = 1000, 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Dodge")

### Carregar imagem de fundo ###
bg = pygame.transform.scale(pygame.image.load("img/bg.jpeg"), (width, height))

### Configurar player ###
player_width = 40
player_height = 60
player_velocity = 5

### Ticks do jogo ###
tick_n = 75

### Projetil ###
star_width = 10
star_height = 20
star_velocity = 5

### Configurar fonte ###
font = pygame.font.SysFont("Consolas", 30)

### adicionar objetos no jogo ###
def draw(player, elapsed_time, stars):
    ### Imagem de fundo ###
    win.blit(bg, (0, 0))

    ### Desenhar o player ###
    pygame.draw.rect(win, "red", player)

    ### Mostrar o tempo decorrido desde o inicio do jogo ###
    time_text = font.render(f'Sobreviveu por: {round(elapsed_time)}s', 1, "white")
    win.blit(time_text, (10, 10))

    for star in stars:
        pygame.draw.rect(win, "white", star)

    pygame.display.update()

### função principal ###
def main():
    run = True
    player = pygame.Rect(200, height - player_height, player_width, player_height)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    ### Projéteis ###
    star_add_increment = 2000
    star_count = 0
    stars = []
    hit = False

    ### Loop para manter o jogo aberto ###
    while(run):
        ### Definir os ticks do jogos 60 ticks por segundo ###
        star_count += clock.tick(tick_n)
        clock.tick(tick_n)  

        ### Criar projéteis na tela ###
        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, width - star_width)
                star = pygame.Rect(star_x, -star_height, star_width, star_height)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0 


        ### Tempo decorrido ###
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        ### Obter teclas pressionadas e mover o player ###
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] and player.x - player_velocity >= 0):
            player.x -= player_velocity
        if (keys[pygame.K_RIGHT] and player.x + player_velocity + player_width <= width):
            player.x += player_velocity

        ### Gerar estrelas ###
        for star in stars[:]:
            star.y += star_velocity
            if star.y > height:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = font.render(f"Você sobreviveu por: {str(int(elapsed_time))} segundos" , 1, "white")
            reinicio = font.render(f"Jogo reiniciara em 4 segundos" , 1, "white")
            win.blit(lost_text, (width/2 - lost_text.get_width()/2, height/2 - lost_text.get_height()/2))
            win.blit(reinicio, (width/2 - reinicio.get_width()/2, (height/2 - reinicio.get_height()/2)+100))
            pygame.display.update()
            pygame.time.delay(4000)
            main()

        ### Adicionar objetos no jogo ###
        draw(player, elapsed_time, stars) 
    pygame.quit()

if __name__ == "__main__":
    main()