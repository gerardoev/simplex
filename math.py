def imprimeDivisores(num):
    divisores = f'Divisores del "{num}": '
    for divisor in range(2,num-1):
        if (num % divisor) == 0:
            divisores += f"{divisor}, "
    if len(divisores) == 0:
        divisores += "Número primo"
    return divisores
def obtenDivisores(num):
    divisores = []
    for divisor in range(2,abs(num)-1):
        if (num % divisor) == 0:
            divisores.append(divisor)
    if len(divisores) == 0:
        return None
    else:
        return divisores

def reduceFraccion(fraccion):
    if fraccion.getDividendo() == 0:
        return 0
    if fraccion.getDivisor() == fraccion.getDividendo():
        return 1
    divisores_dividendo = obtenDivisores(fraccion.getDividendo())
    if divisores_dividendo == None:
        #No se puede reducir porque el dividendo es primo
        return Frac(fraccion.getDividendo(),fraccion.getDivisor())
    divisores_divisor = obtenDivisores(fraccion.getDivisor())
    if divisores_divisor == None:
        #o se puede reducir porque el divisor es primo
        return Frac(fraccion.getDividendo(),fraccion.getDivisor())
    conjunto_dividendo = set(divisores_dividendo)
    conjunto_divisor = set(divisores_divisor)
    # Obtenemos la interseccion de estos conjuntos para saber si tienen divisores en común
    intersec = conjunto_dividendo & conjunto_divisor
    if intersec == set():
        #No se puede reducir más
        return  Frac(fraccion.getDividendo(),fraccion.getDivisor())
    else:
        mayor = max(intersec)
        return Frac(int(fraccion.getDividendo() / mayor),int(fraccion.getDivisor() / mayor))

class Frac:
    def __init__(self, dividendo,divisor):
        self.__dividendo = dividendo
        self.__divisor = divisor
    def __add__(self, other):
        if (self.__divisor != other.getDivisor()):
            nuevo_divisor = self.__divisor * other.getDivisor()
            sum1 = int(self.__dividendo * other.getDivisor())
            sum2 = int(self.__divisor * other.getDividendo())
            return(Frac(sum1 + sum2, nuevo_divisor))
        else:
            return(Frac(self.__dividendo + other.getDividendo(), self.__divisor))
    def __sub__(self, other):
        if (self.__divisor != other.getDivisor()):
            nuevo_divisor = self.__divisor * other.getDivisor()
            rest1 = int(self.__dividendo * other.getDivisor())
            rest2 = int(self.__divisor * other.getDividendo())
            return (Frac(rest1 - rest2, nuevo_divisor))
        else:
            return Frac(self.__dividendo - other.getDividendo(), self.__divisor)
    def __mul__(self, other):
        return Frac(self.__dividendo * other.getDividendo(), self.__divisor * other.getDivisor())
    def __str__(self):
        return(f"{self.__dividendo}/{self.__divisor}")
    def getDivisor(self):
        return self.__divisor
    def getDividendo(self):
        return self.__dividendo
    def getDecimal(self):
        return self.__dividendo/self.__divisor

class Renglon:
    def __init__(self, *elems):
        if len(elems) == 1:
            self.__elems = elems[0]
        elif len(elems) > 0:
            self.__elems = elems
    def __add__(self, other):
        other_els = other.getElems()
        if len(self.__elems) != len(other_els):
            raise RenglonesDiferentesTamaniosExcpetion
        nuevos_els = []
        for i,el in enumerate(self.__elems):
            if type(el) != Frac: #si el primer elemento es entero
                if type(other_els[i]) != Frac: #primero entero y segundo entero
                    nuevo_el = el + other_els[i]
                else: #el primero entero y segundo fraccion
                    nuevo_el = reduceFraccion(Frac(el * other_els[i].getDivisor(),other_els[i].getDivisor()) + other_els[i])
            else: #primer elemento es fraccion
                if type(other_els[i]) != Frac:  # primero fraccion y segundo entero
                    nuevo_el = reduceFraccion(el + Frac(el.getDivisor() * other_els[i],el.getDivisor()))
                else:  # el primero fraccion y segundo fraccion
                    nuevo_el = reduceFraccion(el + other_els[i])
            nuevos_els.append(nuevo_el)
        return Renglon(nuevos_els)
    def __sub__(self, other):
        other_els = other.getElems()
        if len(self.__elems) != len(other_els):
            raise RenglonesDiferentesTamaniosExcpetion
        nuevos_els = []
        for i, el in enumerate(self.__elems):
            if type(el) != Frac:  # si el primer elemento es entero
                if type(other_els[i]) != Frac:  # primero entero y segundo entero
                    nuevo_el = el - other_els[i]
                else:  # el primero entero y segundo fraccion
                    nuevo_el = reduceFraccion(Frac(el * other_els[i].getDivisor(), other_els[i].getDivisor()) - other_els[i])
            else:  # primer elemento es fraccion
                if type(other_els[i]) != Frac:  # primero fraccion y segundo entero
                    nuevo_el = reduceFraccion(el - Frac(el.getDivisor() * other_els[i], el.getDivisor()))
                else:  # el primero fraccion y segundo fraccion
                    nuevo_el = reduceFraccion(el - other_els[i])
            nuevos_els.append(nuevo_el)
        return Renglon(nuevos_els)
    def __mul__(self, other):
        tipo = type(other)
        if tipo != int and tipo != Frac:
            raise MultNoPosibleException
        nuevos_els = []
        for el in self.__elems:
            if type(el) == Frac:
                if tipo == Frac:
                    nuevo_el = reduceFraccion(el * other)
                else:
                    nuevo_el = reduceFraccion(Frac(el.getDividendo() * other, el.getDivisor()))
            else:
                if tipo == int: #entero y entero
                    nuevo_el = el * other
                else: #entero y fraccion
                    nuevo_el = reduceFraccion(Frac(other.getDividendo() * el, other.getDivisor()))
            nuevos_els.append(nuevo_el)
        return Renglon(nuevos_els)
    def getElems(self):
        return tuple(self.__elems)
    def getElemento(self, pos):
        return self.__elems[pos]
    def __str__(self):
        reng = ""
        for el in self.__elems:
            reng += f"{str(el)}    "
        return(reng)

class RenglonesDiferentesTamaniosExcpetion(Exception):
    pass
class MultNoPosibleException(Exception):
    pass

#print(Frac(-10,7) - Frac(-4,189))
#reduceFraccion(Frac(3,7) - Frac(4,189))
#print(reduceFraccion(Frac(6,20)))

#print(Renglon(1, 2, 4, Frac(1,2)))
#print(Renglon(1,2,Frac(1,4),Frac(6,2)) - Renglon(1,Frac(-1,2),4,Frac(4,2)))
#print(Renglon(1,2,Frac(1,4),Frac(6,4)) * Frac(1,5))

pivote = Renglon(Frac(1,7),1,Frac(1,7),0,0,Frac(-1,7),Frac(1,7),0,Frac(4,7))
print("pivote: "+str(pivote))
print(Renglon(4,1,0,1,0,0,0,1,3) - pivote)