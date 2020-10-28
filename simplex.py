import numpy as np
import simplex_ext as pl
import proglin_herr as herr

def simplex(n_variables,restricciones,objetivo):

    nuevas_rest,holg_ex = pl.convertirEstandar(restricciones)

    variables, renglones = pl.crearTabla(restricciones,holg_ex,n_variables,objetivo)

    positivos = False

    while positivos == False:
        pl.toString(n_variables,renglones,objetivo,0)
        fo = renglones["ro"]
        # obtenemos el coef más negativo
        menor = min(fo)

        # obtenemos su pos en el vector
        pos_col = np.where(fo == menor)[0][0]
        #Pivotear
        renglones, err = pl.nuevoTableau(renglones,pos_col, variables)

        if err != False:
            print("Solución optima no acotada")
            break;
        # Comprobar si los coef ya son positivos
        positivos = pl.todosPositivos(renglones["ro"])
    return (renglones)

def dosFases(restricciones):
    rest = restricciones.copy()

    #convertimos a estándar
    rest = pl.convertirEstandar(restricciones)
    #añadimos las de exceso
    rest = pl.añadirExceso(rest)

    #Fase 1

    #Fase 2

_, n_variables, restricciones, objetivo, maxmin = herr.generaProblema(1)
dosFases(restricciones)