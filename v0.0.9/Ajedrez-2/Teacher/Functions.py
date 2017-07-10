# -*- coding: cp1252 -*-

import Listas


def cambio_ficha(a):
    """
    Traducci�n ingl�s-espa�ol.

    :param a: pieza en ingl�s
    :return: pieza en espa�ol
    """
    if a == "Pawn":
        a = u"Pe�n"
    elif a == "Rock":
        a = "Torre"
    elif a == "Knight":
        a = "Caballo"
    elif a == "Bishop":
        a = "Alfil"
    elif a == "Queen":
        a = "Reina"
    elif a == "King":
        a = "Rey"

    return a


def inv_cambio_ficha(a):
    """
    Traducci�n espa�ol-ingl�s.
    Solo se usa en la coronaci�n, por lo que no se traducen ni el pe�n ni el rey

    :param a: pieza en espa�ol
    :return: pieza en ingl�s
    """
    if a == "Torre":
        a = "Rock"
    elif a == "Caballo":
        a = "Knight"
    elif a == "Alfil":
        a = "Bishop"
    elif a == "Reina":
        a = "Queen"

    return a


def cambio_posicion(position):
    """
    Traducci�n de la posici�n de las piezas m�quina-humano.
    Sirve para que que el movimiento se identifique mejor porlas personas.
    El objetivo de usar coordenadas es facilitar las operaciones de movimiento.

    :param position: posici�n coordenadas
    :return: posici�n columna-fila
    """
    columna = str
    fila = str(position[1])

    if position[0] == 1:
        columna = "A"
    elif position[0] == 2:
        columna = "B"
    elif position[0] == 3:
        columna = "C"
    elif position[0] == 4:
        columna = "D"
    elif position[0] == 5:
        columna = "E"
    elif position[0] == 6:
        columna = "F"
    elif position[0] == 7:
        columna = "G"
    elif position[0] == 8:
        columna = "H"

    return columna + fila


def inv_cambio_posicion(position):
    """
    Traducci�n de la posici�n de las piezas humano-m�quina.
    Sirve para insertar los movimientos a mano.
    Mismo objetivo que la funci�n anterior.

    :param position: posici�n columna-fila
    :return: posici�n coordenadas
    """
    x = int
    y = eval(position[1])

    if position[0].upper() == "A":
        x = 1
    elif position[0].upper() == "B":
        x = 2
    elif position[0].upper() == "C":
        x = 3
    elif position[0].upper() == "D":
        x = 4
    elif position[0].upper() == "E":
        x = 5
    elif position[0].upper() == "F":
        x = 6
    elif position[0].upper() == "G":
        x = 7
    elif position[0].upper() == "H":
        x = 8

    return tuple([x, y])


def cambio_listas(which, e0, ef, jugador):
    """
    Se llama cuando la jugada es correcta.

    :param jugador:
    :param which: pieza que se ha movido
    :param e0: posici�n inicial de la pieza
    :param ef: posici�n final de la pieza
    :return: cambio de listas
    """

    lista_1 = dict
    lista_2 = dict
    mayores_1 = list
    menores_1 = list
    mayores_2 = list
    menores_2 = list
    compar_1 = str
    compar_2 = str

    #

    if jugador == 1:
        lista_1 = Listas.casillasOcupadas['Blancas']
        lista_2 = Listas.casillasOcupadas['Negras']

        mayores_1 = Listas.PiezasMayores_B
        menores_1 = Listas.PiezasMenores_B

        mayores_2 = Listas.PiezasMayores_N
        menores_2 = Listas.PiezasMenores_N

        compar_1 = "ef[0] <= 4"
        compar_2 = "ef[0] > 4"

    elif jugador == 2:
        lista_1 = Listas.casillasOcupadas['Negras']
        lista_2 = Listas.casillasOcupadas['Blancas']

        mayores_1 = Listas.PiezasMayores_N
        menores_1 = Listas.PiezasMenores_N

        mayores_2 = Listas.PiezasMayores_B
        menores_2 = Listas.PiezasMenores_B

        compar_1 = "ef[0] >= 4"
        compar_2 = "ef[0] < 4"

    #

    del lista_1[e0]

    if which == "Pawn" and (ef[1] == 1 or ef[1] == 8):
        p = raw_input("Pieza: ")
        p = inv_cambio_ficha(p[0].upper() + p[1:].lower())

        lista_1[ef] = p
        mayores_1.append(p)

        if "Pawn_%s" % ef[0] in menores_1:
            menores_1.remove("Pawn_%s" % ef[0])

        else:
            for i in range(1, 9):

                j = "Pawn_%s" % i
                if j in menores_1:

                    menores_1.remove(j)
                    break

    else:
        lista_1[ef] = which

    if ef in lista_2:
        pieza_comida = lista_2[ef]
        del lista_2[ef]

        if pieza_comida == "Pawn":

            if "Pawn_%s" % ef[0] in menores_2:
                menores_2.remove("Pawn_%s" % ef[0])

            else:
                for i in range(1, 9):

                    j = "Pawn_%s" % i
                    if j in menores_2:
                        menores_2.remove(j)
                        break

        elif pieza_comida == "Rock":
            if eval(compar_1):
                mayores_2.remove("Rock_2")

            elif eval(compar_2):
                mayores_2.remove("Rock_1")

        elif pieza_comida == "Knight":
            if eval(compar_1):
                mayores_2.remove("Knight_2")

            elif eval(compar_2):
                mayores_2.remove("Knight_1")

        elif pieza_comida == "Bishop":
            if eval(compar_1):
                mayores_2.remove("Bishop_2")

            elif eval(compar_2):
                mayores_2.remove("Bishop_1")

        elif pieza_comida == "Queen":
            mayores_2.remove("Queen")

        elif pieza_comida == "King":
            mayores_2.remove("King")
        else:
            print "error"
            print pieza_comida
            print lista_2
