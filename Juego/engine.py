import curses
from SaveSystem import reading_sokoban as level

#funcion que maneja el menu
def menu():
    print("**Sokoban**\nDesea iniciar?(S/N)")
    inicio = ""
    while inicio.upper() != "S" and inicio.upper() !="N":
        inicio = input()
        if inicio.upper() != "S" and inicio.upper() !="N":
            print("Error, escriba S o N")
    if inicio.upper() == "S":
        print("Partida nueva o antigua?(N/A)")
        partida = ""
        while partida.upper() != "N" and partida.upper() != "A":
            partida = input()
            if partida.upper() != "N" and partida.upper() != "A":
                print("Error, escriba N o A")
        if partida.upper() == "N":
            abrir_Partida(1)
        else:
            abrir_Partida(-1)            
    else:
        return
def abrir_Partida(num_level):
    aux = True
    while(aux):
        aux = nivel(num_level)
        if(aux == -2):
            print("No hay partida guardada")
            return 0
        if(aux>0):
            num_level=aux
            if(num_level >= 3):
                print("Haz acabado todos los niveles. Felicidades! :)")
                return 0
        


#maneja movimientos del jugador y de los bloques
def nivel(num_level):
    scr = curses.initscr()
    curses.start_color()
    curses.curs_set(0)
    curses.echo(0)

    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_WHITE)

    max_h, max_w = scr.getmaxyx()

    win = curses.newwin(max_h, max_w, 0, 0)
    win.keypad(1)
    win.timeout(100)

    if num_level == -1 : 
        jugador, blocks, walls, goals, num_level = level.openLevel("saving.txt")
    else: 
        jugador, blocks, walls, goals, num_level = level.openLevel("nivel" + str(num_level) + ".txt")
    
    for i in blocks:
        win.addch(i[0], i[1], 'X', curses.color_pair(2))

    for i in walls:
        win.addch(i[0], i[1], '#', curses.color_pair(4))

    for i in goals:
        if not (i in blocks): 
            win.addch(i[0], i[1], 'O', curses.color_pair(3))
    
    if(num_level == -2):
        return -2

    key = curses.KEY_BACKSPACE
    instrucciones = "F1 para guardar y salir. F2 para reiniciar nivel. Flechas para mover. Mueve todos los bloques( ) a los objetivos( )"
    win.addstr(0, 0, instrucciones)
    win.addch(0, len(instrucciones)-2, 'O', curses.color_pair(3))
    win.addch(0, len(instrucciones)-21, 'X', curses.color_pair(2))
    while True : 
        box_error = 0 
        #Agarra tecla del usuario
        nxt_key = win.getch()
        key = curses.KEY_BACKSPACE if nxt_key == -1 else nxt_key

        if (key == curses.KEY_F2):
            win.addch(jugador[0][0], jugador[0][1], ' ')
            for i in blocks: 
                win.addch(i[0], i[1], ' ')
            jugador, blocks, walls, goals, num_level = level.openLevel("nivel" + str(num_level) + ".txt")
            win.addch(jugador[0][0], jugador[0][1], curses.ACS_PI, curses.color_pair(1))
            for i in blocks: 
                win.addch(i[0], i[1], 'X', curses.color_pair(2))

        #Si la tecla es F1 se sale del juego
        if(key == curses.KEY_F1):
            curses.endwin()
            level.savingLevel(jugador, blocks, walls, goals, num_level)
            return False

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
                win.addch(blocks[block_index][0], blocks[block_index][1], 'X', curses.color_pair(2)) 

        if(new_pos[0] >= max_h or new_pos[1] >= max_w-1  or new_pos[0]<=0 or new_pos[1]<=0 or box_error or (new_pos in walls)):
            new_pos = jugador[0]
        
        win.addch(jugador[0][0], jugador[0][1], ' ')

        jugador.insert(0, new_pos)

        win.addch(jugador[0][0], jugador[0][1], curses.ACS_PI, curses.color_pair(1))
        goals_achieved = 0 
        for i in goals:
            if not (i in blocks) and not (i in jugador):
                win.addch(i[0], i[1], 'O', curses.color_pair(3))
            if i in blocks:
                goals_achieved+=1
        if (goals_achieved == len(goals)):
            curses.endwin()
            return num_level+1
        jugador.pop()
        


def main():
    menu()
#ENDDEF

main()