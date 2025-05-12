import numpy as np
from sympy import symbols, sympify, lambdify

def captar_funcion():
   
    print("\n=== ENTRADA DE FUNCIÓN ===")
    print("Ingresa la función matemática en términos de x")
    print("Ejemplos: x**2 - 4, sin(x) + cos(x), exp(-x) - x")
    
    while True:
        try:
            # Capturar la expresión matemática como texto
            expresion = input("f(x) = ")
            
            # Convertir la expresión a una forma simbólica usando SymPy
            x = symbols('x')
            expr_simbolica = sympify(expresion)
            
            # Convertir la expresión simbólica a una función numérica
            funcion = lambdify(x, expr_simbolica, modules=['numpy'])
            
            # Verificar que la función se puede evaluar
            try:
                funcion(1.0)  # Prueba con un valor simple
                print(f"Función captada correctamente: f(x) = {expr_simbolica}")
                return funcion, str(expr_simbolica)
            except Exception as e:
                print(f"Error al evaluar la función: {e}")
                continue
                
        except Exception as e:
            print(f"Error al procesar la expresión: {e}")
            print("Por favor, verifica tu sintaxis e intenta nuevamente.")

def captar_intervalo():
    
    print("\n=== INTERVALO INICIAL ===")
    
    while True:
        try:
            a = float(input("Valor de a: "))
            b = float(input("Valor de b: "))
            
            if a >= b:
                print("Error: 'a' debe ser menor que 'b'.")
                continue
                
            return a, b
        except ValueError:
            print("Error: ingresa valores numéricos válidos.")

def captar_parametros():
   
    print("\n=== PARÁMETROS ===")
    
    while True:
        try:
            tol = float(input("Tolerancia (ej. 0.0001): "))
            max_iter = int(input("Máximo de iteraciones (ej. 100): "))
            
            if tol <= 0 or max_iter <= 0:
                print("Error: tanto la tolerancia como el máximo de iteraciones deben ser positivos.")
                continue
                
            return tol, max_iter
        except ValueError:
            print("Error: ingresa valores numéricos válidos.")