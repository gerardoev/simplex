import copy
import numpy as np
from proglin_herr import *

def todosPositivos(fo):
    for el in fo:
        if el < 0:
            return False
    return True

def ingresaProblema():
    """
    Función para ingresa el problema por consola
    Regresa -> (2, 2, [[[1, 1], 3, 4, 0], [[1, 2], 2, 2, 0]], [1, 1], 0)
    :return n_restricciones: (int) el número de restricciones ingresadas
    :return n_variables: (int) el número de variables dle problema
    :return restricciones: (list) una de tamaño n_restricciones que contiene cada restricción representada como otra lista.
                            Esta lista contiene, los coeficientes(List), la relación(int), el lado derecho(int) y 0 (int variables de exceso y holgura)
    :return objetivo: (list) una lista con los coeficientes de la función objetivo
    :return maxmin: 0, si es de maximizar. 1, si es de minimizar
    """

    #Inicializaciiones
    n_restricciones = -1
    n_variables = -1
    maxmin = -1
    restricciones = []
    objetivo = []

    while (n_restricciones < 0):
        n_restricciones = int(input("Ingresa el número de restricciones"))
    while (n_variables < 0):
        n_variables = int(input("Ingresa el número de variables"))
    while (maxmin != 0 and maxmin != 1):
        maxmin = int(input("Ingrese si el problema es de maximización o minimización:\n0 Si es maximización\n1 si es minimización"))

    #Ingresar las restricciones
    # se creara un objeto tipo [[1,1,1],2,200]
    for res in range(n_restricciones):
        rest = []
        coefs = []
        for var in range(n_variables):
            print(f'------------- restricción {res+1}--------------')
            coefs.append(int(input(f"Ingresa el coeficiente de x{var+1}")))
        rest.append(coefs)
        tipo=int(input(f'Selecciona la el tipo de restricción\n1.\t=\n2.\t<=\n3.\t>='))
        rest.append(tipo)
        der = int(input(f"Ingresa el lado derecho"))
        rest.append(der)
        rest.append(0) #0 variables de holgura y exceso al inicio
        restricciones.append(rest)
    #Ingresar la función objetivo
    for var in range(n_variables):
        print(f'-------------FUNCIÓN OBJETIVO--------------')
        objetivo.append(int(input(f"Ingresa el coeficiente de x{var + 1}")))

    return (n_restricciones,n_variables,restricciones,objetivo,maxmin)

def crearTabla(restricciones,n_var_ext,n_var,objetivo,base):
    """
        Recibe:
            restricciones
            n_var_ext: (int) el número de variables que se agregaron ya sean exceso, holgura o y
            n_var: (int) el número de variables originales
            objetivo: (list) los coef de la f.o.
            base: (dict) las variables que estrán en la base
    """
    variables = {}
    renglones = {}

    # Generar vars
    pos = 0
    for var in range(n_var):
        variables[pos] = f'x{var+1}'
        pos += 1

    #Generamos el renglón con la función objetivo pero con signos cambiados
    renglones['ro'] = np.array(genFilaObjetivo(objetivo,n_var_ext)) *-1
    #Generar renglones
    for reng in range(len(restricciones)):
        renglones[base[reng]] = (np.array(genFila(restricciones[reng],n_var_ext,reng)))

    return (variables, renglones)

def convertirEstandar(restricciones):
    nuevas_rest = copy.deepcopy(restricciones)
    holg_ex = 0
    for (pos,rest) in enumerate(nuevas_rest):
        if rest[2] < 0: #Si es negativo el lado derecho, multiplicamos por menos 1
            nuevas_rest[pos] = mult_rest_menos_uno(rest)
        if rest[1] == 2: #Si es de tipo <=
            rest[3] = 1
            rest[1] = 1 #convertimos a =
            holg_ex += 1
        elif rest[1] == 3:
            rest[3] = -1
            rest[1] = 1
            holg_ex += 1
    return nuevas_rest, holg_ex

def nuevoTableau(renglones,pos_col,variables):
  renglones_copy = copy.deepcopy(renglones)

  # Encontramos la columna
  clave_col = variables[pos_col]
  # Encontramos la fila
  clave_fil, pivote,err = encuentraPivote(pos_col, renglones)
  if err == True:
      fo_temp = list(renglones["ro"])
      fo_temp.pop(pos_col)
      menor = min(fo_temp)
      if menor >= 0: ## Si ya no hay negativos
          return None, True
      else:
          pos_col = np.where(renglones["ro"] == menor)[0][0]
          return nuevoTableau(renglones,pos_col,variables)
  #hacemos el cambio (actualizar clave)
  renglones_copy[clave_col] = renglones_copy.pop(clave_fil)
  #Hacer 1 el pivote
  clave_pivote, renglones_copy = convertirFilaPivote(renglones_copy,pivote,clave_col)
  #Hacer 0s arriba y abajo del pivote
  renglones_copy = hacerCeros(clave_pivote, pos_col, renglones_copy)
  return renglones_copy, False

def hacerCeros(clave_pivote, col, tableau):
    """
    Hace ceros una columna pivote, basandose en una fila pivote
    :param clave_pivote: la clave (str) de la fila pivote
    :param col: la posición (int) de la columna pivote
    :param tableau: el tableau actual
    :return:
    """
    nuevo_tableau = copy.deepcopy(tableau)
    base = copy.copy(nuevo_tableau)

    #eliminamos el pivote para iterar en el resto de filas
    base.pop(clave_pivote)

    for (clave,fila) in base.items():
        nuevo_tableau[clave] = np.round_(fila - (fila[col]*nuevo_tableau[clave_pivote]), 3)
    return nuevo_tableau

def convertirFilaPivote(tableau,pivote,clave_fil):
    """
    Convierte el pivote en 1 y multiplicando toda la fila por su inverso
    :return:
    """
    nuevo_tableau = copy.deepcopy(tableau)
    inverso = 1

    if pivote != 1:
        inverso = 1/pivote
    nuevo_tableau[clave_fil] = np.round_(nuevo_tableau[clave_fil] * inverso,3)
    clave_pivote = clave_fil
    return clave_pivote, nuevo_tableau

def encuentraPivote(col,renglones):
    """
    Divide la columna z entre cada elemento de la columna pivote, y devuelve el menor
    :param col:  posición (Int) en el array de la columna pivote
    :param renglones: El tableau actual
    :return:
    """
    divisioness = []
    #[[True,4,25,x1],[False,-1,-1,x2]]
    for renglon in renglones:
        reng = []
        if renglon == "ro":
            continue
        fila_actual = renglones[renglon]
        if fila_actual[col] <= 0:
            reng.append(False)
            reng.append(-1)
            reng.append(-1)
            reng.append(list(renglones.keys())[col])
            divisioness.append(reng)
        else:
            reng.append(True)
            reng.append(fila_actual[-1] / fila_actual[col])
            reng.append(fila_actual[col])
            reng.append(renglon)
            divisioness.append(reng)
    #Verificar si hay un pivote válido
    validos = []
    for el in divisioness:
        if el[0] == True:
            validos.append(el)
    if len(validos) == 0:
        return "", -1,True

    #Si si hay alguno valido
    menor = validos[0]
    for el in validos:
        if el[1] < menor[1]:
            menor = el

    return menor[3], menor[2], False

def añadirArtif(restricciones):
    """
        Recibe:
            restricciones: (list)[[[coefs],igualdad,ladoDer,holg-ex],[res2]]
    """
    rest_copy = copy.deepcopy(restricciones)
    for rest in rest_copy:
        if rest[1] == 1 or rest[1] == 3:
            rest.append(1)
        else:
            rest.append(0)
    return rest_copy

def genZ(rests):
    objetivo = []
    for rest in rests:
        if rest[-1] != 0:
            objetivo.append(-1)
    return objetivo


def generarBase(tipo, n_restricciones):
    """
        Recibe:
            tipo: (int) 0 si es simplex, 1 Si es 2 fases
            n_restricciones: (int) el número de restricciones
    """
    #{0:"S1",1:"S2",2:"S3"}
    base = {}
    if tipo == 0:#Tableau Simplex
        for i in range(n_restricciones):
            base[i] = f"S{i+1}"
    return base