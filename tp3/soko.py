import copy
from copy import deepcopy
from operator import mul
PARED = "#"
CAJA = "$"
JUGADOR = "@"
OBJETIVO = "."
OBJETIVO_MAS_CAJA = "*"
OBJETIVO_MAS_JUGADOR = "+"
ESPACIO_VACIO = " "

def crear_grilla(desc):

    '''Crea una grilla a partir de la descripción del estado inicial.
    '''

    grilla = []
    for i in desc:
      grilla.append(list(i))
    return grilla



def dimensiones(grilla):
    '''Devuelve una tupla con la cantidad de columnas y filas de la grilla.'''
    return len(grilla[0]), len(grilla)



def hay_pared(grilla, c, f):
    '''Devuelve True si hay una pared en la columna y fila (c, f).'''
    return PARED in grilla[f][c]


def hay_objetivo(grilla, c, f):
    '''Devuelve True si hay un objetivo en la columna y fila (c, f).'''
    return OBJETIVO in grilla[f][c] or OBJETIVO_MAS_CAJA in grilla[f][c] or OBJETIVO_MAS_JUGADOR in grilla[f][c]



def hay_caja(grilla, c, f):
    '''Devuelve True si hay una caja en la columna y fila (c, f).'''
    return CAJA in grilla[f][c] or OBJETIVO_MAS_CAJA in grilla[f][c]


def hay_espacio_vacio(grilla, c, f):
    '''Devuelve True si hay un espacio vacio en la columna y fila (c, f).'''
    return ESPACIO_VACIO in grilla[f][c]


def hay_jugador(grilla, c, f):
    '''Devuelve True si el jugador está en la columna y fila (c, f).'''
    return JUGADOR in grilla[f][c] or OBJETIVO_MAS_JUGADOR in grilla[f][c]


def juego_ganado(grilla):
    '''Devuelve True si el juego está ganado.'''

    for linea in grilla:
      for item in linea:
        if item == OBJETIVO or item == OBJETIVO_MAS_JUGADOR:
          return False
    return True



def posicion_jugador(grilla):
    """
    Devuelve la ubicacion actual del jugador al pasarle una grilla
    """
    posicion_actual_jugador = (0,0)

    for fila in range(len(grilla)):
      for columna in range(len(grilla[0])):
        if hay_jugador(grilla, columna, fila):
          return (columna,fila)


def movimiento_posible(grilla,columna,fila,columna_siguiente,fila_siguiente):
    """
    Recibe una grilla con las posiciones originales y las posiciones a moverse, devuelve True si el movimiento es posible y False si no lo es
    """
    if hay_pared(grilla,columna,fila):
        return False
    if (hay_caja(grilla,columna,fila) and hay_pared(grilla,columna_siguiente,fila_siguiente)):
        return False
    if (hay_caja(grilla,columna,fila) and hay_caja(grilla,columna_siguiente,fila_siguiente)):
        return False
    return True



def mover(grilla, direccion):
    '''
    Mueve el jugador en la dirección indicada. La función debe devolver una grilla representando el estado siguiente al
    movimiento efectuado.
    '''
    #creo nueva grilla para no modificar la anterior
    nueva_grilla = deepcopy(grilla)

    direccion_c, direccion_f = direccion
    jugador_c, jugador_f = posicion_jugador(nueva_grilla)
    nueva_posicion_c, nueva_posicion_f = jugador_c + direccion_c, jugador_f + direccion_f
    nueva_posicion_caja_c, nueva_posicion_caja_f = jugador_c + direccion_c*2, jugador_f + direccion_f*2

    if (movimiento_posible(nueva_grilla,nueva_posicion_c,nueva_posicion_f,nueva_posicion_caja_c,nueva_posicion_caja_f)):
        if hay_caja(nueva_grilla,nueva_posicion_c,nueva_posicion_f):
            if hay_objetivo(grilla,nueva_posicion_caja_c,nueva_posicion_caja_f):
                nueva_grilla[nueva_posicion_caja_f][nueva_posicion_caja_c] = OBJETIVO_MAS_CAJA
            else:
                nueva_grilla[nueva_posicion_caja_f][nueva_posicion_caja_c] = CAJA

        if hay_objetivo(nueva_grilla,nueva_posicion_c,nueva_posicion_f):
            nueva_grilla[nueva_posicion_f][nueva_posicion_c] = OBJETIVO_MAS_JUGADOR
        else:
            nueva_grilla[nueva_posicion_f][nueva_posicion_c] = JUGADOR
        #si el jugador comienza en un objetivo
        if nueva_grilla[jugador_f][jugador_c] == OBJETIVO_MAS_JUGADOR:
            nueva_grilla[jugador_f][jugador_c] = OBJETIVO
        else:
            nueva_grilla[jugador_f][jugador_c] = ESPACIO_VACIO

        return nueva_grilla

    return nueva_grilla
