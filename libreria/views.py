from django.shortcuts import render,redirect

# Create your views here.
from .utils import iniciar_division_sintetica_django, obtencion_de_divisores, obtencion_de_factores, formatear_factores


def inicio(request):
    return render(request, 'paginas/inicio.html')

def ingreso(request):
    return render(request, 'paginas/ingreso.html')

def resultados(request):
    return render(request, 'paginas/resultados.html')




def resultados(request):
    degree = int(request.POST.get('degree'))
    coefficients = request.POST.getlist('coefficients')
    coefficients = [int(coeff) for coeff in coefficients]

    # Calculamos los divisores, asignándolos de forma invertida
    p_divisores = obtencion_de_divisores(coefficients[0])
    q_divisores = obtencion_de_divisores(coefficients[-1])
    possible_factors = obtencion_de_factores(q_divisores, p_divisores)

    factores_formateados = formatear_factores(possible_factors)

    division_result = iniciar_division_sintetica_django(coefficients=coefficients, factors=possible_factors)

    context = {
        'degree': degree,
        'coefficients': coefficients,
        'polynomial_representation': division_result['polynomial_representation'],
        'steps': division_result['steps'],
        'polinomioOriginal': division_result['polinomioOriginal'],  # Agregar el polinomio original
        'p': abs(coefficients[-1]),
        'q': abs(coefficients[0]),
        'divisores_p': q_divisores,
        'divisores_q': p_divisores,
        'factores': factores_formateados,
        'factores_validos': division_result['factores_validos'],
        'mensaje': division_result.get('mensaje', '')  # Incluimos 'mensaje' en el contexto
    }

    return render(request, 'paginas/resultados.html', context)
