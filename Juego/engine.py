#Emilio Antonio Pérez Fematt y José Carlos de la Torre Hernández
#A01236167 y A01235953
#Avenida: ICT
#engine.py
#Este programa maneja todos los aspectos del juego y del menu
#Version de python utlizada: 3.8.5  

import curses
from SaveSystem import reading_sokoban as level
import os

#Funcion menu, que permite al usuario decidir si quiere iniciar el juego y si quiere empezar un juego nuevo o empezar uno antiguo
#Autor: Jose Carlos de la Torre Hernandez
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

#Funcion que recibe el numero de nivel para empezar una partida y se encarga de cargar niveles nuevos cuando se completa el anterior
#Autor: Emilio Perez
def abrir_Partida(num_level):
    aux = True
    while(aux):
        aux = nivel(num_level)
        if(aux == -2):
            print("No hay partida guardada")
            return 0
        if(aux>0):
            num_level=aux
            if(num_level >= 10):
                print("Haz acabado todos los niveles. Felicidades! :)")
                return 0
        
#Funcion que recibe el numero de nivel carga los objetos del mismo, tambien se encarga del movimiento del jugador
#Autor: Emilio Perez
def nivel(num_level):
    #encuentra directorio del archivo
    dir = [x for x in os.path.dirname(os.path.realpath(__file__)).split('\\') if x != "Juego"]
    pathName = ""
    for i in dir: 
        pathName = os.path.join(pathName, i)
        if pathName == "C:" : pathName+="\\"
    print(pathName)

    #Inicializa la libreria de curses
    scr = curses.initscr()
    curses.start_color()
    curses.curs_set(0)
    curses.echo(0)

    #Inicializa las combinaciones de colores utilizadas
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_WHITE)

    #Inicializa la pantalla y el teclado
    max_h, max_w = scr.getmaxyx()
    win = curses.newwin(max_h, max_w, 0, 0)
    win.keypad(1)
    win.timeout(100)

    #Carga los datos del nivel en la pantalla
    if num_level == -1 : 
        jugador, blocks, walls, goals, num_level = level.openLevel(os.path.join(pathName, "saving.txt"))
    else: 
        jugador, blocks, walls, goals, num_level = level.openLevel(os.path.join(pathName, "nivel" + str(num_level) + ".txt"))
    for i in blocks:
        win.addch(i[0], i[1], 'X', curses.color_pair(2))
    for i in walls:
        win.addch(i[0], i[1], '#', curses.color_pair(4))
    for i in goals:
        if not (i in blocks): 
            win.addch(i[0], i[1], 'O', curses.color_pair(3))
    #if que checa si existe una partida antigua guardada
    if(num_level == -2):
        return -2

    key = curses.KEY_BACKSPACE
    #Agrega una linea de texto arriba de la pantalla con instrucciones
    instrucciones = "F1 para guardar y salir. F2 para reiniciar nivel. Flechas para mover. Mueve todos los bloques( ) a los objetivos( )"
    win.addstr(0, 0, instrucciones)
    win.addch(0, len(instrucciones)-2, 'O', curses.color_pair(3))
    win.addch(0, len(instrucciones)-21, 'X', curses.color_pair(2))

    #Loop principal del programa
    while True : 
        box_error = 0 
        #Recibe tecla del usuario
        nxt_key = win.getch()
        key = curses.KEY_BACKSPACE if nxt_key == -1 else nxt_key
        
        #Si usuario ingresa F2 reinicia el nivel
        if (key == curses.KEY_F2):
            win.addch(jugador[0][0], jugador[0][1], ' ')
            for i in blocks: 
                win.addch(i[0], i[1], ' ')
            jugador, blocks, walls, goals, num_level = level.openLevel(os.path.join(pathName, "nivel" + str(num_level) + ".txt"))
            win.addch(jugador[0][0], jugador[0][1], curses.ACS_PI, curses.color_pair(1))
            for i in blocks: 
                win.addch(i[0], i[1], 'X', curses.color_pair(2))

        #Si la tecla es F1 se sale del juego
        if(key == curses.KEY_F1):
            curses.endwin()
            level.savingLevel( pathName, jugador, blocks, walls, goals, num_level)
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

        #Previene que el usuario haga movimientos illegales
        if(new_pos[0] >= max_h or new_pos[1] >= max_w-1  or new_pos[0]<=0 or new_pos[1]<=0 or box_error or (new_pos in walls)):
            new_pos = jugador[0]
        
        win.addch(jugador[0][0], jugador[0][1], ' ')

        jugador.insert(0, new_pos)

        win.addch(jugador[0][0], jugador[0][1], curses.ACS_PI, curses.color_pair(1))
        #Cuenta las cajas en objetivos y si son todas acaba el nivel
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