import curses

#funcion que maneja el menu
def menu():
    pass

#funcion que lee un archivo y regresa una lista de bloques
def get_Blocks(num_level):
    pass

#funcion que lee un archivo y regresa una lista de paredes
def get_walls(num_level):
    pass

#maneja movimientos del jugador y de los bloques
def nivel():
    scr = curses.initscr()
    curses.curs_set(0)
    curses.echo(0)

    max_h, max_w = scr.getmaxyx()

    win = curses.newwin(max_h, max_w, 0, 0)
    win.keypad(1)
    win.timeout(100)

    play_x = int(max_w/4)
    play_y = int(max_h/2)

    jugador = [
        [play_y, play_x]
    ]

    blocks = [
        [int(max_h/2), int(max_w/2)],
        [int(max_h/2)+1, int(max_w/2)]
    ]

    walls = [
        [10, 10]
    ]

    for i in blocks:
        win.addch(i[0], i[1], 'B')

    for i in walls:
        win.addch(i[0], i[1], '#')

    key = curses.KEY_BACKSPACE

    while True : 
        box_error = 0 
        #Agarra tecla del usuario
        nxt_key = win.getch()
        key = curses.KEY_BACKSPACE if nxt_key == -1 else nxt_key

        #Si la tecla es F1 se sale del juego
        if(key == curses.KEY_F1):
            curses.endwin()
            quit()

        #Hace el cambio de la nueva posicion
        new_pos = [jugador[0][0], jugador[0][1]]
        if(key == curses.KEY_DOWN):
            new_pos[0]+=1
        if(key == curses.KEY_UP):
            new_pos[0]-=1
        if(key == curses.KEY_RIGHT):
            new_pos[1]+=1
        if(key == curses.KEY_LEFT):
            new_pos[1]-=1

        #Maneja la interaccion entre bloques
        if(new_pos in blocks):
            block_index = 0

            for i in range(len(blocks)):
                if(blocks[i] == new_pos):
                    block_index = i

            new_box = [blocks[block_index][0], blocks[block_index][1]]
            if(key == curses.KEY_DOWN):
               new_box[0]+=1
            if(key == curses.KEY_UP):
                new_box[0]-=1
            if(key == curses.KEY_RIGHT):
                new_box[1]+=1
            if(key == curses.KEY_LEFT):
                new_box[1]-=1
            
            if(new_box[0] >= max_h or new_box[1]>=max_w-1 or new_box[0]<=0 or new_box[1]<=0 or (new_box in blocks) or (new_box in walls)):
                new_pos = jugador[0]
                box_error=1

            if not(box_error):
                blocks[block_index] = new_box
                win.addch(blocks[block_index][0], blocks[block_index][1], 'B') 

        if(new_pos[0] >= max_h or new_pos[1] >= max_w-1  or new_pos[0]<=0 or new_pos[1]<=0 or box_error or (new_pos in walls)):
            new_pos = jugador[0]
        
        win.addch(jugador[0][0], jugador[0][1], ' ')

        jugador.insert(0, new_pos)

        win.addch(jugador[0][0], jugador[0][1], curses.ACS_PI)
        
        jugador.pop()
        


def main():
    nivel()
#ENDDEF

main()