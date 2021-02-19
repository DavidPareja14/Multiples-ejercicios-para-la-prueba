"""
******Desarrollado por David Pareja Arango
------17-03-2021
Este código solo fue diseñado para realizar una prueba técnica, si va a ser utilizado con un
fin distinto a su revisión, primero debo saber con qué propósito se usará.

FUNCIONAMIENTO Y OBSERVACIONES:
* Este programa encuentra la máxima dimensión de un array, al ejecutarse la función dimension(), las demás funciones
serán fácil de ejecutarse, ya que a medida que se va recorriendo el array o Matriz, puedo realizar las otras
tareas.
* Los valores de la función straigth() no coinciden totalmente ya que, como le comenté al Señor Herman, se está
tomando en los resultados otorgados en la prueba técnica, como si los únicos elementos del array fuesen números,
pero las listas que estén anidadas también deben contar.
* La respuesta para f no es correcta, en el documento de la prueba técnica el resultado es 66, pero en realidad es 74
"""

class MyMatriz:
    matriz = [] #atributo de la clase que contendra la matriz pasada como parametro
    numerosParaSumar = [] #contendrá todos los números de la matriz, se llena en dimension()
    numeroElementosEnDimensiones = [] #Contiene la cantidad de elementos presente en cada dimension,
                                      #se llena en dimension()

    def __init__(self, matriz):
        #Verifico que se pase como parametro una lista y no otra cosa
        if (type(matriz) == list):
            self.matriz = matriz
        else:
            raise ValueError("Se debe pasar una matriz")

        self.numeroDimensionesMayor = 0
        self.numeroElementosEnDimensiones.append(len(self.matriz))

    def dimension(self):
        """
           Este ejercicio puede ser como una busqueda en profundidad, sin embargo, no se hace como tal
           Explicación:
           Por cada lista que encuentre dentro de otra lista, empiezo a a profundizar, por eso, necesito
           llevar un control de las listas que vayan apareciendo, para esto es listasPendientes.
           Básicamente, si existe una lista, hay una dimensión, por esta razón, la variable encargada del conteo 
           de las dimensiones, numeroDimensiones, se inicializa en 1, porque se supene que mi constructor recibe
           una lista (Es más, si no se envía una lista, se detiene el programa) y luego, cada vez que encuentre
           una lista, cuento una dimensión, pero de forma inteligente, ya que por ejemplo, en [[], [], []] hay 
           tres listas contenidas y esto no significa que exista 4 dimensiones, solo hay 2. Básicamente en el
           último for me encargo de esto.
           Para hacer un poco más eficiente el proceso, a medida que encuentro números enteros, los agrego al
           atributo numerosParaSumar, para luego sumarlos en la función pertinente
        """
        listasPendientes = []
        for elem in self.matriz:
            numeroDimensiones = 1
            if type(elem) == int:
                self.numerosParaSumar.append(elem)
            else:
                profundizarLista = True
                lista = elem
                numeroDimensiones += 1
                self.numeroElementosEnDimensiones.append(len(elem))
                while profundizarLista:
                    contarDimension = True
                    for e in lista:
                        if type(e) == int:
                            self.numerosParaSumar.append(e)
                        else:
                            listasPendientes.append(e)
                            self.numeroElementosEnDimensiones.append(len(e))
                            """
                            Practicamente verifico que una lista corresponde a una dimensión, pero 
                            si hay varias listas en una lista, esto contará como solo una dimensión
                            """
                            if contarDimension: 
                                contarDimension = False
                                numeroDimensiones += 1

                    if len(listasPendientes) >= 1:
                        lista = listasPendientes[0]
                        listasPendientes.pop(0) #Ya utilicé la primera lista, no la necesito más
                    else:
                        profundizarLista = False
                """
                Como estoy buscando la mayor profundidad para determinar la dimensión, debo de mantener
                cual es la mayor dimensión actualizada.
                """
                if self.numeroDimensionesMayor < numeroDimensiones: 
                    self.numeroDimensionesMayor = numeroDimensiones

        self.numeroDimensionesMayor = numeroDimensiones

        return self.numeroDimensionesMayor

    def straight(self):
        """
        Gracias a la función o método dimensión(), esta función es fácil, ya que según voy recorriendo la matriz
        para encontrar la dimensión, también puedo determinar la cantidad de elementos de cada dimension.
        -- self.numeroDimensionesMayor me sirve para saver si la matriz es unidimencional, en caso de ser 
        afirmativo, no tengo que compararla con otras dimensiones, por eso se retorna True
        -- self.numeroElementosEnDimensiones: lista que contiene la cantidad de elementos encontrada en 
        cada dimension, todos los valores deben ser iguales para retornar verdadero, de lo contrario, hay
        dimensiones con cantidad de elementos diferentes
        """
        if self.numeroDimensionesMayor == 1:
            return True
        else:
            numeroAComparar = self.numeroElementosEnDimensiones[0]
            for num in self.numeroElementosEnDimensiones:
                if num != numeroAComparar:
                    return False
            return True

    def compute(self):
        """
        En la función o método dimension(), lleno el atributo self.numerosParaSumar, el cual va a
        contoner todos los números que contenga la lista
        """
        try:
            suma = 0
            for num in self.numerosParaSumar:
                suma += num

            return suma
        except ValueError:
            print("La matriz debe contener numeros")

if __name__ == "__main__":
    #Matrices de prueba según el documento de la prueba técnica
    matriza = [1, 2]
    matrizb = [[1, 2], [2, 4]]
    matrizc = [[1, 2], [2, 4], [2, 4]]
    matrizd = [[[3, 4], [6, 5]]]
    matrize = [[[1, 2, 3]], [[5, 6, 7], [5, 4, 3]], [[3, 5, 6], [4, 8, 3], [2, 3]]]
    matrizf = [[[1, 2, 3], [2, 3, 4]], [[5, 6, 7], [5, 4, 3]], [[3, 5, 6], [4, 8, 3]]]

    #Matrices que yo realizo para hacer más pruebas, con los resultados que deben aparecer
    #Debe mostrar 5 dimensiones, Suma 40, straight False
    pruebaA = [[[1, 2, 3]], [[[1,2,7],[4, 3, 2], [[5, 3, 10]]]]] 

    #Debe dar 3 dimensiones, sumar 160, straight True
    pruebaB = [[[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4,4,4,4]],
                                [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4,4,4,4]],
                                [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4,4,4,4]],
                                [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4,4,4,4]]]
    #Debe dar 6 dimensiones, sumar 9 y el straight debe ser False
    pruebaC=[[[[2], [[[7]]]]]]

    #A continuacion, verifico que en realidad se cree un objeto, pasando una matriz
    try:
        o = MyMatriz(matrize) #->>>>>>>>>>>>CREO EL OBJETO CON LA MATRIZ QUE DESEE
        numDimensiones = o.dimension()

        print("\n-La matriz o arreglo tiene " + str(numDimensiones) + " dimension(es)")

        suma = o.compute()
        print("\n-La suma de los números de la matriz es: " + str(suma))

        lasDimensionesCantidadIgualDeElementos = o.straight()
        print("\n-Es verdad que las dimensiones tienen igual número de elementos: " + str(lasDimensionesCantidadIgualDeElementos))

    except ValueError as e:
        print(e)
