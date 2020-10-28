import numpy as np
import simplex_ext as pl
import proglin_herr as herr

def simplex(n_variables,restricciones,objetivo,var_ext,base_v):
    """
        Recibe
            n_variables: (int) el número de variables originales
            restricciones: ()
    """

    variables, renglones = pl.crearTabla(restricciones,var_ext,n_variables,objetivo,base_v)

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
    #añadimos las de exceso
    rest = pl.añadirArtif(rest)
    rest, _ = pl.convertirEstandar(rest)

    #Fase 1

    #Fase 2

n_restricciones, n_variables, restricciones, objetivo, maxmin = herr.generaProblema(1)
#convertimos a estándar
base = pl.generarBase(0,n_restricciones)
dosFases(restricciones)


#print(simplex(n_variables,rest,objetivo,n_restricciones,base))