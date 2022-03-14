from soko import crear_grilla, hay_caja, hay_pared, hay_jugador, hay_objetivo, mover, juego_ganado, dimensiones
import gamelib
from copy import deepcopy
import time


#clases a utilizar
class _Nodo:
    def __init__(self, dato, prox=None):
        self.dato = dato
        self.prox = prox

class Pila:
    def __init__(self):
        self.tope = None

    def apilar(self, dato):
        nodo = _Nodo(dato, self.tope)
        self.tope = nodo

    def ver_tope(self):
        """
        Devuelve el elemento que está en el tope de la pila.
        Pre: la pila NO está vacía.
        """
        if self.esta_vacia():
            raise ValueError("pila vacía")
        return self.tope.dato

    def desapilar(self):
        """
        Desapila el elemento que está en el tope de la pila
        y lo devuelve.
        Pre: la pila NO está vacía.
        Pos: el nuevo tope es el que estaba abajo del tope anterior
        """
        if self.esta_vacia():
            raise ValueError("pila vacía")
        dato = self.tope.dato
        self.tope = self.tope.prox
        return dato

    def esta_vacia(self):
        return self.tope is None

INSTRUCCIONES = {
'NORTE': (0,-1),
'SUR': (0,1),
'ESTE': (1,0),
'OESTE': (-1,0),
'REINICIAR': "r",
'SALIR': 'esc'
}

PIXELES_OBJETO = 64

def agregar_vacios(nivel):
    """
    Recibe un nivel y devuelve el mismo pero con espacios vacios de manera
    que todas las filas igualen en longitud a la fila de longitud maxima.
    """
    long_max = max([len(fila) for fila in nivel])
    for fila in nivel:
        if len(fila) < long_max:
            for i in range(long_max-len(fila)):
                fila.append(" ")
    return nivel

def cargar_niveles():
    """Devuelve un diccionario con todas los niveles del juego"""
    dict_niveles = {}
    titulos_niveles = {}
    with open('niveles.txt','r') as niveles:
        contador_niveles = 1
        lista = []
        for linea in niveles:
            if not linea[0].isalpha() and linea[0] != "'" and linea != '\n':
                lista.append(linea.rstrip("\n"))
            if linea[0] == "'":
                titulos_niveles[contador_niveles] = linea.rstrip("\n")
            if linea == '\n':
                dict_niveles[contador_niveles] = agregar_vacios(crear_grilla(lista))
                contador_niveles += 1
                lista = []
        else:
            dict_niveles[contador_niveles] = agregar_vacios(crear_grilla(lista))

    return dict_niveles,titulos_niveles



def lector_teclas():
    CONJUNTO_TECLAS = {}
    """lee el archivo teclas.txt introduciendo los datos en un diccionario"""
    with open('teclas.txt','r') as teclas:
        for linea in teclas:
            if linea != '\n':
                lista_linea = linea.rstrip("\n").split("=")
                CONJUNTO_TECLAS[lista_linea[0]] = lista_linea[1]

    return CONJUNTO_TECLAS




def mostrar_juego(juego):
    """Actualiza la ventana"""
    columnas,filas = dimensiones(juego)

    #ajusto ventana al tamaño del nivel
    gamelib.resize(columnas*PIXELES_OBJETO, filas*PIXELES_OBJETO)

    for fila in range(filas):
      for columna in range(columnas):
          gamelib.draw_image('img/ground.gif', columna*PIXELES_OBJETO, fila*PIXELES_OBJETO)
          if hay_caja(juego, columna, fila):
              gamelib.draw_image('img/box.gif', columna*PIXELES_OBJETO, fila*PIXELES_OBJETO)
          if hay_objetivo(juego, columna, fila):
              gamelib.draw_image('img/goal.gif', columna*PIXELES_OBJETO, fila*PIXELES_OBJETO)
          if hay_pared(juego, columna, fila):
              gamelib.draw_image('img/wall.gif', columna*PIXELES_OBJETO, fila*PIXELES_OBJETO)
          if hay_jugador(juego, columna, fila):
              gamelib.draw_image('img/player.gif', columna*PIXELES_OBJETO, fila*PIXELES_OBJETO)


def tiene_titulo(numero_nivel,dict_niveles,dict_titulos):
    "Muestra en pantalla el titulo del nivel en caso de poseer uno"


    dim = dimensiones(dict_niveles[numero_nivel])
    mitad = ((dim[0]*PIXELES_OBJETO)//2,(dim[1]*PIXELES_OBJETO)//2)


    if numero_nivel in dict_titulos:
        gamelib.draw_begin()
        gamelib.draw_text(dict_titulos[numero_nivel], mitad[0], mitad[1])
        gamelib.draw_end()
        time.sleep(2)







def estado_a_inmutable(estado):
    """Transforma el estado actual a una representacion inmutable del mismo en forma de cadena"""
    cadena = ""
    for fila in estado:
        for caracter in fila:
            cadena += caracter
        cadena+= ";"

    return cadena[:-1]




def buscar_solucion(estado_inicial):
    """Pasandole un estado devuelve una pila con las acciones que llevan a la solucion"""
    visitados = set()
    pila_acciones = Pila()
    return backtrack(estado_inicial, visitados, pila_acciones), pila_acciones

def backtrack(estado,visitados,pila_acciones):
    """Funcion recursiva que plantea soluciones candidatas y va descartando
    las que se determina que no son soluciones"""

    movimientos = [(0,-1),(0,1),(1,0),(-1,0)]

    visitados.add(estado_a_inmutable(estado))

    if juego_ganado(estado):
        # ¡encontramos la solución!
        return True

     #Para toda acción posible `a` desde el estado:
    for a in movimientos:
        nuevo_estado = mover(estado, a)

        if estado_a_inmutable(nuevo_estado) in visitados:
            continue

        if backtrack(nuevo_estado, visitados, pila_acciones):
            pila_acciones.apilar(a)
            return True


    return False

def main():

    solucion_activa = False
    CONJUNTO_TECLAS = lector_teclas()
    carga_niveles = cargar_niveles()
    niveles = carga_niveles[0]
    NIVEL_FINAL = len(niveles)
    # Inicializar el estado del juego
    nivel = 1
    grilla = niveles[nivel]


    tiene_titulo(nivel,carga_niveles[0],carga_niveles[1])
    pila_deshacer = Pila()


    while gamelib.is_alive():


        gamelib.draw_begin()
        mostrar_juego(grilla)
        gamelib.draw_end()


        if pila_deshacer.esta_vacia():
            pila_deshacer.apilar(grilla)
        if not pila_deshacer.esta_vacia() and grilla != pila_deshacer.ver_tope():
            pila_deshacer.apilar(grilla)


        ev = gamelib.wait(gamelib.EventType.KeyPress)
        if not ev:
            break

        tecla = ev.key

        # Actualizar el estado del juego, según la `tecla` presionada

        if tecla in CONJUNTO_TECLAS:
            if tecla == 'r':
                grilla = niveles[nivel]
            elif tecla == 'Escape':
                break

            elif tecla == 'u':

                if not pila_deshacer.esta_vacia():
                    pila_deshacer.desapilar()
                    if pila_deshacer.esta_vacia():
                        continue
                    grilla = pila_deshacer.ver_tope()

            elif tecla == 'h':
                if solucion_activa == False:
                    solucion_activa = buscar_solucion(grilla)



                else:
                    if solucion_activa[1].esta_vacia():
                        solucion_activa = False
                        continue
                    next = solucion_activa[1].desapilar()

                    grilla = mover(grilla,next)

            else:
                tecla_a_valor_tecla = CONJUNTO_TECLAS[tecla]
                valor_tecla_a_instruccion = INSTRUCCIONES[tecla_a_valor_tecla]
                grilla = mover(grilla,valor_tecla_a_instruccion)
                solucion_activa = 0

        if juego_ganado(grilla) or tecla == '5':
            if nivel == NIVEL_FINAL:
                dim = dimensiones(grilla)
                mitad = ((dim[0]*PIXELES_OBJETO)//2,(dim[1]*PIXELES_OBJETO)//2)
                gamelib.draw_begin()
                gamelib.draw_text('GANASTE!', mitad[0], mitad[1])
                gamelib.draw_end()
                time.sleep(3)
                break
            pila_deshacer = Pila()
            grilla = niveles[nivel+1]
            nivel += 1
            tiene_titulo(nivel,carga_niveles[0],carga_niveles[1])



gamelib.init(main)
