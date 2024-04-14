import pygame

width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height))

pause = pygame.rect.Rect(width / 2 - 100, height / 2 - 100, width / 2, height / 2)


# on définit un rectangle pour le menu pause

def pause_menu(state):
    paused = state
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
        pygame.draw.rect(screen, (0, 0, 0), pause)
        pygame.display.update()
        pygame.display.flip()
        pygame.time.Clock().tick(60)
        # on affiche le menu pause
