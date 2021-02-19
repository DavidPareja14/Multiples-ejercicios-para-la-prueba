"""
******Desarrollado por David Pareja Arango
-----19-03-2021
Este código solo fue diseñado para realizar una prueba técnica, si va a ser utilizado con un
fin distinto a su revisión, primero debo saber con qué propósito se usará.
"""

"""
SOBRE EL PROGRAMA:
* Este programa sirve para las 4 operaciones básicas (+,-,*,/) con paréntesis, pero si hay paréntesis 
anidados, no funcionará, solo sirve con paréntesis no anidados
* Si hay por ejemplo, 1 2 3, estos números separados por espacio, el programa los interpreta como 123, es decir
como si se tratase de un solo número
* Los paréntesis se verifican en la expresión regular, no en compute
"""

import re


class MyArray:
	cadena = str
	operacionAritmetica = []

	def __init__(self, cadena):
		self.cadena = cadena

	"""PARAMETROS:
	finalizar: Ya que una operación puede finalizar en ) o un número, debo saber en cual finalizo.
	completarCierreParentesis: Si la operacion termina en numero, no debe haber ningun parentesis abierto
	cadenaSinEspacios: Procesa la operacion sin ningun espacio
	"""
	def expresionRegularReconoceOperacion(self, finalizar, completarCierreParentesis, cadenaSinEspacios):
		operacion  = "(\d+[-+*/])+" #reconoce perfectamente una operación artimetica sin parentesis
		operacionConParentesis = "\(" + operacion + "\d+\)"

		patron  = re.match("(" + operacionConParentesis + "[-+*/]|" 
									+ operacionConParentesis[:-2] + completarCierreParentesis + "|"
									 + operacion + ")+" + finalizar + "$", cadenaSinEspacios)
		return patron

	def operation(self):
		cadenaSinEspacios = self.cadena.replace(" ", "") #Es más eficiente procesar sin espacios
		if cadenaSinEspacios[-1] == ")":
			esCorrectaLaOperacion = self.expresionRegularReconoceOperacion("\)", "", cadenaSinEspacios)
		else:
			esCorrectaLaOperacion = self.expresionRegularReconoceOperacion("\d+", "\)[-+*/]", cadenaSinEspacios)

		#Este condicional parece redundante, pero da más claridad, ya que de lo contrario se retornaría un objeto
		if esCorrectaLaOperacion:
			return True
		else:
			return False

	def realizarOperacion(self, a, b, operador):
		if operador == "+":
			return float(a) + float(b)
		elif operador == "-":
			return float(a) - float(b)
		elif operador == "*":
			return float(a) * float(b)
		elif operador == "/":
			return float(a) / float(b)

	def convertirCadenaEnLista(self):
		cadenaProcesada = self.cadena.replace(" ", "") #Al quitar espacios, el procesamiento es más rápido
		numero = "" #Parece ironico que sea string, pero es para tomar cada numero que esta en cadena
		listaConValoresDeCadena = []
		huboElOtroParentesis = False #El otro parentesis es )
		"""
		El siguiente for es creado principalmente para encontrar los valores numéricos entre la cadena 
		pasada como parámetro, ya que puede ser un número de un solo dígito o de varios dígitos
		"""
		for caracter in cadenaProcesada:
			try:
				int(caracter) #Si no se puede convertir en entero el caracter, es porque aquí finaliza un número
				numero += caracter
			except:
				if (caracter != "(") and (not huboElOtroParentesis):
					listaConValoresDeCadena.append(numero)
				if caracter == ")":
					"""
					Esta parte es fundamental, ya que numero puede ser vacio y si esto ocurre, no lo
					puedo insertar, básicamente debo mirar cuando no insertar numero, para esto utilizo 
					huboElOtroParentesis...
					"""
					huboElOtroParentesis = True
				else:
					huboElOtroParentesis = False

				numero = ""
				listaConValoresDeCadena.append(caracter)
		if cadenaProcesada[-1] != ")":
			listaConValoresDeCadena.append(numero)
		return listaConValoresDeCadena

	def tomarValoresYOperar(self, posActual, operador, listaOperacionAritmetica):
		"""
		Cada vez que se encuentre un operador, tomo los valores correspondientes y opero con
		ellos, luego, el resultado lo guardo en la posición del primer operando, después elimino
		los valores que ya no necesito 
		"""
		a = listaOperacionAritmetica[posActual - 1]
		b = listaOperacionAritmetica[posActual + 1]
		listaOperacionAritmetica[posActual - 1] = self.realizarOperacion(a, b, operador)
		listaOperacionAritmetica.pop(posActual)
		listaOperacionAritmetica.pop(posActual)

	def realizarOperacionSegunPrioridad(self, listaOperacionAritmetica):
		for operador in ["/", "*", "-", "+"]:
			for posActual, caracter in enumerate(listaOperacionAritmetica):
				if caracter == operador:
					self.tomarValoresYOperar(posActual, operador, listaOperacionAritmetica)
					try:
						while listaOperacionAritmetica[posActual] == operador:
							self.tomarValoresYOperar(posActual, operador, listaOperacionAritmetica)
					except:
						continue
		return listaOperacionAritmetica[0]

	def buscarOperacionEntreParentesis(self, posiscionParentisisAbertura):
		operacionEntreParentesis = []
		for posiscionParentisisCierre, elemento in enumerate(self.operacionAritmetica[posiscionParentisisAbertura+1:]):
			if elemento == ")":
				break
			operacionEntreParentesis.append(elemento)
		resultadoOperacionEntreParentesis = self.realizarOperacionSegunPrioridad(operacionEntreParentesis)

		return (resultadoOperacionEntreParentesis, posiscionParentisisCierre)

	def compute(self):
		if self.operation():
			self.operacionAritmetica = self.convertirCadenaEnLista()
			for pos, elemento in enumerate(self.operacionAritmetica):
				if elemento == "(":
					resultadoOperacionEntreParentesis, posiscionParentisisCierre = self.buscarOperacionEntreParentesis(pos)
					self.operacionAritmetica[pos] = resultadoOperacionEntreParentesis
					del self.operacionAritmetica[pos + 1 : 2 + pos + posiscionParentisisCierre]

			return self.realizarOperacionSegunPrioridad(self.operacionAritmetica)
		else:
			return False
"""
Cadenas que funcionaron (Se verificaron con calculadora):

PARA OPERATION:
Todo retorna True

PARA COMPUTE:
"""
prueba1 = "5 - 5 + 8 - 9 + 10 +20 - 1- 55/2+30*40" # = 1200.5
prueba2 = "5 - 5 + 5 + 5 - 100000" #= -99990
prueba3 = "5 - 5 + 8 - 9 + 10 + 20 - 1 - 55" # = -27
prueba4 = "5 - 5 / 4 + 1 + 10 + 20" # = 34.75
prueba5 = "5 - 5 / (4 + 1) + 10 * (5/3 + 2*5) + 20" # = 140.6666666666
prueba6 = "(4 -100) / (80 * 3) - (89 + 100)" # = -189.4
"""
De la prueba Tecnica, estas operaciones también funcionan:

PARA OPERATION:
Todo retorna True

PARA COMPUTE
"""
prueba7 = "2 + 10 / 2 - 20" # = -13
prueba8 = "(2 + 10) / 2 - 20" # = -14

#OPERACIONES QUE NO FUNCIONAN
prueba9 = "Hello world"
prueba10 = "(2 + 10 / 2 - 20"
prueba11 = "(1 - 3 + 2) 1 * 4" #Le hace falta el operador matemático después del paréntesis de cierre
prueba12 = "1 +1 - 20 + (1 +2 33) -"


o = MyArray(prueba7)
print("\n----------------->El resultado de la operación es : "+str(o.compute()))