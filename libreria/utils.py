import os
from fractions import Fraction

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def impresion_de_polinomio(polinomio):
    texto_polinomio = ""
    for i, coeficiente in enumerate(polinomio):
        exponente = len(polinomio) - 1 - i
        if i > 0:
            texto_polinomio += " + " if coeficiente >= 0 else " - "
            coeficiente = abs(coeficiente)
        if coeficiente == 1 and exponente > 0:
            texto_polinomio += f"x^{exponente}"
        elif exponente == 0:
            texto_polinomio += f"{coeficiente}"
        else:
            texto_polinomio += f"{coeficiente}x^{exponente}"
    return texto_polinomio

def obtener_valor_absoluto(coeficiente, posicion):
    return abs(coeficiente[posicion])

def obtencion_de_divisores(valor):
    valor = int(abs(valor))
    return [i * sgn for i in range(1, valor + 1) if valor % i == 0 for sgn in (1, -1)]

def obtencion_de_factores(lista_p, lista_q):
    return list({Fraction(p, q) for p in lista_p for q in lista_q})

def obtener_divisores_y_factores(coefficients):
    p = coefficients[-1]  # Ahora P es el último coeficiente
    q = coefficients[0]   # Y Q es el primer coeficiente
    divisores_p = obtencion_de_divisores(p)
    divisores_q = obtencion_de_divisores(q)
    factores = obtencion_de_factores(divisores_p, divisores_q)
    return p, q, divisores_p, divisores_q, factores

def realizar_division(polinomio_actual, factor_actual):
    polinomio_nuevo = [polinomio_actual[0]]
    for j in range(1, len(polinomio_actual)):
        polinomio_nuevo.append(polinomio_actual[j] + (factor_actual * polinomio_nuevo[j - 1]))
    return polinomio_nuevo

def probar_factores(polinomio_actual, factores):
    pasos = []  # Guardar los pasos de división
    while True:
        encontrado = False
        for factor_actual in factores:
            polinomio_nuevo = realizar_division(polinomio_actual, factor_actual)
            if polinomio_nuevo[-1] == 0:
                polinomio_nuevo.pop()  # Eliminar el último término si es cero
                pasos.append((factor_actual, polinomio_nuevo))
                polinomio_actual = polinomio_nuevo  # Actualiza el polinomio actual para la siguiente división
                encontrado = True
                break  # Rompe el bucle para reiniciar con el nuevo polinomio
        if not encontrado:
            mensaje = "Este polinomio tiene raíces complejas"  # Mensaje añadido
            break  # Si no se encontró un factor que reduzca, sal del bucle
    return pasos


def formatear_factores(factores):
    factores_formateados = []
    for factor in factores:
        # Si el denominador es 1 o -1, mostrar como entero; de lo contrario, como fracción
        if factor.denominator == 1:
            factores_formateados.append(str(factor.numerator))
        else:
            factores_formateados.append(f"{factor.numerator}/{factor.denominator}")
    return factores_formateados



def iniciar_division_sintetica_django(coefficients, factors):
    polinomioOriginal = coefficients[:]
    grado = len(coefficients) - 1
    exponents = list(range(grado, -1, -1))
    steps = []
    factores_validos = []
    mensaje = ""  # Variable para el mensaje de raíces complejas

    for factor in factors:
        factor = Fraction(factor)

        # Calcula y actualiza P, Q, divisores y factores en cada paso
        while len(coefficients) > 1:
            # Calcular P y Q para el polinomio actual
            p = abs(coefficients[-1])
            q = abs(coefficients[0])
            divisores_p = obtencion_de_divisores(p)
            divisores_q = obtencion_de_divisores(q)
            factores = obtencion_de_factores(divisores_p, divisores_q)

            resultado = [coefficients[0]]
            multiplications = [""]

            for coef in coefficients[1:]:
                mul = resultado[-1] * factor
                multiplications.append(mul)
                temp_result = coef + mul
                resultado.append(temp_result)

            if resultado[-1] == 0:
                factores_validos.append(str(factor))
                steps.append({
                    "factor": factor,
                    "polynomial": coefficients[:],
                    "polynomial_representation": impresion_de_polinomio(coefficients),
                    "exponents": exponents[:],
                    "multiplications": multiplications,
                    "resultado": resultado,
                    "p": p,
                    "q": q,
                    "divisores_p": divisores_p,
                    "divisores_q": divisores_q,
                    "factores": formatear_factores(factores)
                })

                resultado.pop()
                coefficients = resultado
                exponents = list(range(len(coefficients) - 1, -1, -1))
            else:
                break
    
    if not steps:
        mensaje = "Este polinomio tiene raíces complejas, no se puede resolver"

    polynomial_representation = ""
    for i, (coeff, exp) in enumerate (zip(polinomioOriginal, range(len(polinomioOriginal) - 1, -1, -1))):
        if i==0:
            if coeff ==1 and exp>0:
                polynomial_representation += f"x^{exp}" if exp > 1 else "x"
            elif exp == -1 and exp>0:
                polynomial_representation += f"-x^{exp}" if exp > 1 else "-x"
            elif exp == 0:
                polynomial_representation += f"{coeff}"
            else:
                polynomial_representation += f"{coeff}x^{exp}" if exp > 1 else f"{coeff}x"
        else:
            if coeff < 0:
                polynomial_representation += f" - {abs(coeff)}" if abs(coeff) != 1 else " - "
            else:
                polynomial_representation += f" + {coeff}" if coeff != 1 else " + "
            
            if exp > 1:
                polynomial_representation += f"x^{exp}"
            elif exp == 1:
                polynomial_representation += "x"

    return {
        "polynomial_representation": polynomial_representation,
        "steps": steps,
        "polinomioOriginal": polinomioOriginal,
        "factores_validos": factores_validos,
        "mensaje": mensaje
    }
