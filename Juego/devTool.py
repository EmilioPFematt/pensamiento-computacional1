import curses
from SaveSystem import reading_sokoban as level

def nivel(num_level):
    scr = curses.initscr()
    curses.curs_set(0)
    curses.echo(0)

    max_h, max_w = scr.getmaxyx()

    win = curses.newwin(max_h, max_w, 0, 0)
    win.keypad(1)
    win.timeout(100)
    
    jugador = [[10, 10]]
    blocks = []
    walls = []
    goals = []

    #print(jugador)
    #print(blocks)
    #print(walls)
    #print(goals)

    for i in blocks:
        win.addch(i[0], i[1], 'B')

    for i in walls:
        win.addch(i[0], i[1], '#')

    for i in goals:
        win.addch(i[0], i[1], 'G')

    key = curses.KEY_BACKSPACE

    while True : 
        box_error = 0 
        #Agarra tecla del usuario
        nxt_key = win.getch()
        key = curses.KEY_BACKSPACE if nxt_key == -1 else nxt_key

        #Si la tecla es F1 se sale del juego
        if(key == curses.KEY_F1):
            curses.endwin()
            level.savingLevel(jugador, blocks, walls, goals, num_level)
            return False
        
        if(key == curses.KEY_F2):
            blocks.append([jugador[0][0], jugador[0][1]])
        if(key == curses.KEY_F3):
            walls.append([jugador[0][0], jugador[0][1]])
        if(key == curses.KEY_F4):
            goals.append([jugador[0][0], jugador[0][1]])
        if(key == curses.KEY_F5):
            if(jugador[0] in blocks):
                blocks.remove(jugador[0])
            if(jugador[0] in walls):
                walls.remove(jugador[0])
            if(jugador[0] in goals):
                goals.remove(jugador[0])

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


        if(new_pos[0] >= max_h or new_pos[1] >= max_w-1  or new_pos[0]<=0 or new_pos[1]<=0):
            new_pos = jugador[0]
        
        win.addch(jugador[0][0], jugador[0][1], ' ')

        jugador.insert(0, new_pos)

        win.addch(jugador[0][0], jugador[0][1], curses.ACS_PI)
        
        for i in blocks:
            if not (i in jugador):
                win.addch(i[0], i[1], 'B')

        for i in walls:
            if not (i in jugador):
                win.addch(i[0], i[1], '#')

        for i in goals:
             if not (i in jugador):
                win.addch(i[0], i[1], 'G')

        jugador.pop()
        


def main():
    print("Pon el numero del nivel que estas creando: ")
    num_lvl = int(input())
    nivel(num_lvl)
#ENDDEF

main()