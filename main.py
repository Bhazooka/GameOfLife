import time
import pygame
import numpy as np

COLOUR_BG = (10,10,10)
COLOUR_GRID = (40, 40, 40)
COLOUR_DIE_NEXT = (170, 170, 170)                                      #transition from alive to dying. By the rules
COLOUR_ALIVE_NEXT = (255, 255, 255) 
                                    # you can define your own size as a constant variable

def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

#game rules:        
    for row, col in np.ndindex(cells.shape):   
        alive = np.sum(cells[row-1: row+2, col-1: col+2]) - cells[row,col]  #numpy array
        color = COLOUR_BG if cells[row, col] == 0 else COLOUR_ALIVE_NEXT

        if cells[row, col] == 1:                                        #if the cell has state 1 (Alive == true)
            if alive < 2 or alive > 3:                                  #if its alone or has one neighbor...
                if with_progress:
                    color = COLOUR_DIE_NEXT                             #...it dies

            elif 2 <= alive <= 3:                                       #if it has 2 or 3 neighbour...
                updated_cells[row, col] = 1                             #...cell lives
                if with_progress:
                    colour = COLOUR_ALIVE_NEXT                          #update colour of cell to alive
        
        else:
            if alive == 3:                                              #if theres 3 alive cells...
                updated_cells[row, col] = 1                             #...this cell comes to life
                if with_progress:
                    colour = COLOUR_ALIVE_NEXT

        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))   #

    return updated_cells

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    cells = np.zeros((60, 80))
    screen.fill(COLOUR_GRID)
    update(screen, cells, 10)

    pygame.display.flip()
    pygame.display.update()

    running = False

    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            #
            elif event.type == pygame.KEYDOWN:                     
                if event.key == pygame.K_SPACE:                     
                    running = not running                           #press space to run or pause game
                    update(screen, cells, 10)
                    pygame.display.update()

            #Mouse press to set alive cells
            if pygame.mouse.get_pressed()[0]:                       #if the mouse is pressed
                pos = pygame.mouse.get_pos()                        #get position of where its pressed
                cells[pos[1] // 10, pos[0] // 10] = 1               #make cell alive (set cell to 1)        #pos is a tuple (x,y)
                update(screen, cells, 10)
                pygame.display.update()

        screen.fill(COLOUR_GRID)

        if running:
            cells = update(screen, cells, 10, with_progress=True)
            pygame.display.update()
            
        time.sleep(0.001)

if __name__ == '__main__':
    main()
