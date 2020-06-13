import pygame
import map
import time

def main():
    pygame.init()
    pygame.display.set_caption("pathfinder")
    screen = pygame.display.set_mode(map.getSize())
    map.initialize(screen)
    running = True
    selecting = False
    startSelect = False
    solving = False
    undo = False

    frames_per_second = 20
    seconds_per_frame = 1.0 / frames_per_second
    lastDraw = time.time()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
                map.initialize(screen)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                solving = map.solveReady()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                undo = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                selecting = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                selecting = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                startSelect = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                startSelect = False
        if solving:
            selecting = False
            startSelect = False
            ret = map.stepSolution()
            if not ret:
                solving = False
        if selecting:
            map.select(pygame.mouse.get_pos())
        if startSelect:
            map.selectEndpoint(pygame.mouse.get_pos())

        if time.time() - lastDraw > seconds_per_frame:
            lastDraw = time.time()
            if solving:
                map.drawSolution(screen)
            if not solving:
                map.drawSolution(screen)
                map.overlay(screen)

        if undo:
            undo = False
            if map.hasSolved():
                map._resetSolution()
                map._resetDraw(screen)
            else:
                map.undo(screen)

        pygame.display.update()

if __name__=="__main__":
    main()