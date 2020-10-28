def toString(n_variables,restricciones,objetivo,maxmin):
    """
    Función que convierte a string un problema para ser impreso

    :param n_restricciones: número de restricciones del problema
    :param n_variables:  número de variables del problema
    :param restricciones: una lista de listas donde cada lista interna es una restriccione
    :param objetivo: una lsita con los coeficientes de la función objetivo
    :param relaciones: una lista con valores del 1 al 3, donde 1 es "=", 2 es "<=" y 3 es ">="
    :param maxmin: int que indica si el problema es de maximización o minimización
    :return problema: un string representando el problema
    """
    problema = "z = "

    if maxmin == 0:
        problema = f"max z = "
    elif maxmin == 1:
        problema = "min z = "
    problema += coefToString(objetivo) + "\n"
    y =1
    for (pos,rest) in enumerate(restricciones):
        if rest[1] == 1:
            restS = coefToString(rest[0])
            if rest[-1] != 0:
                restS += f" + {rest[-1]}s{y}"
                y+=1
            problema += restS+" = "+str(rest[-2])+"\n"
        elif rest[1] == 2:
            restS = coefToString(rest[0])
            if rest[-1] != 0:
                restS += f" + {rest[-1]}s{y}"
                y += 1
            problema += restS+ " <= " + str(rest[-2]) + "\n"
        elif rest[1] == 3:
            restS = coefToString(rest[0])
            if rest[-1] != 0:
                restS += f" + {rest[-1]}s{y}"
                y += 1
            problema += restS + " >= " + str(rest[-2]) + "\n"
    return problema

def coefToString(coefs):
    cadena = ""
    for coef in range(len(coefs)):
        if coefs[coef] == 0:
            continue
        if coef != 0:
            if coefs[coef] > 0:
                cadena += " + "
        cadena += str(coefs[coef]) + f"x{coef+1}"
    return cadena

def imprimirTabla(variables, tabla):
    base = list(tabla.keys())
    tam_col = 10

    vbls =""
    for var in variables.values(): #cada variable
        vbls += var + (" "*(tam_col-len(var)))
    print("\t\t  " +vbls)
    reng = ""
    for var in base: ##cada renglon
        reng += var + "        "
        for valor in list(tabla[var]):
            reng += str(valor) + (" "*(tam_col-len(str(valor))))
        reng += "\n"
    print(reng)

def mult_rest_menos_uno(rest):
    nueva_rest =[]
    nvos_coefs = []
    for coef in rest[0]:
        nvos_coefs.append(coef * -1)
    nueva_rest.append(nvos_coefs)
    if rest[1] == 2:
        nueva_rest.append(3)
    elif rest[1] == 3:
        nueva_rest.append(2)
    else:
        nueva_rest.append(1)
    nueva_rest.append(rest[2] * -1)
    return nueva_rest

def genFila(rest,holg_ex, pos):
    fila = []
    fila.extend(rest[0]) #agregamos los coef originales
    ceros = [0]*holg_ex
    ceros[pos] = 1
    fila.extend(ceros)
    fila.append(rest[2])
    return fila

def genFilaObjetivo(variables,obj):
    """
        Recibe
            variables: (dict) {0:x1,1:x2...} un diccionario con las variables del tableau ordenadas
            obj: (dict) {x1: 1, y1: -1, ...} un diccionario con los coefs de la f.o.
        Regresa
            fila [list] [0,1,1,...] una lista que representa la fila objetivo
    """
    fila = []
    for var in variables.values:
        if variables.get(var) != None:
            fila.append(variables[var])
        else:
            fila.append(0)
    fila.append(0) # z inicial es cero
    return fila

def generaProblema(problema):
    if problema == 0:
        return(3,2, [[[1,0],2,5,0],[[1,1],2,8,0],[[0,1],2,4,0,0]],{"X1":1,"X2":3},0)
    if problema == 1:
        return(2, 2, [[[1, 1], 3, 4, 0], [[1, 2], 2, 2, 0,0]], {"X1":1, "X2":1}, 0)

def generarVariables(restricciones):
    """
        Devuelve
            vars: (dict) {0: "x1", 1: "x2",...}  todas las variables ordenadas
    """
    vars = {}
    clave = 0
    for i in range(len(restricciones[0][0])):
        clave += 1
        vars[i] = f'X{i+1}'
    for i,rest in enumerate(restricciones):
        if rest[3] != 0:
            clave += 1
            vars[clave] = f'S{i+1}'
    for i,rest in enumerate(restricciones):
        if rest[4] != 0:
            clave += 1
            vars[clave] = f'Y{i+1}'
    return vars