import numpy as np
import matplotlib.pyplot as plt
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

def graficar_funcion(funcion, expr_str, a, b, raiz=None, iteraciones=None):
   
    # Crear un rango de valores x más amplio que el intervalo [a, b]
    margen = (b - a) * 0.3
    x_min, x_max = a - margen, b + margen
    x = np.linspace(x_min, x_max, 1000)
    
    # Evaluar la función en ese rango
    try:
        y = funcion(x)
        
        # Crear figura y ejes
        plt.figure(figsize=(10, 6))
        
        # Graficar la función
        plt.plot(x, y, 'b-', label=f'f(x) = {expr_str}')
        
        # Graficar el eje x
        plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        
        # Marcar el intervalo inicial
        plt.axvline(x=a, color='g', linestyle='--', alpha=0.5, label=f'a = {a}')
        plt.axvline(x=b, color='r', linestyle='--', alpha=0.5, label=f'b = {b}')
        
        # Si se encontró una raíz, marcarla
        if raiz is not None:
            plt.plot(raiz, 0, 'ro', markersize=8, label=f'Raíz ≈ {raiz:.6f}')
        
        # Si se proporcionaron iteraciones, mostrarlas
        if iteraciones is not None:
            for i, punto in enumerate(iteraciones):
                plt.plot(punto, 0, 'yo', markersize=4, alpha=0.6)
                if i % 3 == 0:  # Etiquetar solo algunas iteraciones para no sobrecargar
                    plt.text(punto, funcion(punto), f'  it.{i+1}', fontsize=8)
        
        # Ajustes de la gráfica
        plt.grid(True, alpha=0.3)
        plt.title(f'Gráfica de la función y método de bisección')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.legend()
        
        # Ajustar límites para visualizar mejor cerca del eje x
        y_abs_max = max(abs(np.min(y)), abs(np.max(y)))
        plt.ylim(-y_abs_max * 1.1, y_abs_max * 1.1)
        
        # Mostrar la gráfica
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"Error al graficar la función: {e}")

def metodo_biseccion(funcion, expr_str, a, b, tol=1e-6, max_iter=100, mostrar_pasos=True):
   
    # Verificar condición inicial
    fa = funcion(a)
    fb = funcion(b)
    
    if fa * fb >= 0:
        print(f"Error: f({a}) y f({b}) deben tener signos opuestos.")
        print(f"f({a}) = {fa}, f({b}) = {fb}")
        return None, 0, []
    
    # Mostrar gráfica inicial
    graficar_funcion(funcion, expr_str, a, b)
    
    # Inicializar variables
    iteracion = 0
    error = b - a
    c = 0  # Inicializar c para que no dé error en caso de salir temprano
    puntos_medios = []
    
    # Tabla de resultados
    if mostrar_pasos:
        print("\n{:<5} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(
            "Iter", "a", "b", "c", "f(a)", "f(c)", "Error"))
        print("-" * 95)
    
    # Proceso iterativo
    while error > tol and iteracion < max_iter:
        # Calcular punto medio
        c = (a + b) / 2
        puntos_medios.append(c)
        fc = funcion(c)
        
        # Mostrar información de la iteración
        if mostrar_pasos:
            print("{:<5} {:<15.8f} {:<15.8f} {:<15.8f} {:<15.8f} {:<15.8f} {:<15.8f}".format(
                iteracion + 1, a, b, c, fa, fc, error))
        
        # Verificar si c es raíz
        if abs(fc) < tol:
            break
        
        # Actualizar intervalo
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
        
        # Actualizar error e iteración
        error = abs(b - a)
        iteracion += 1
    
    # Mostrar resultado final
    if iteracion == max_iter and error > tol:
        print("\nAdvertencia: Se alcanzó el número máximo de iteraciones sin convergencia.")
    
    print(f"\nRaíz aproximada: {c:.8f}")
    print(f"Valor de la función en la raíz: f({c:.8f}) = {funcion(c):.8f}")
    print(f"Error estimado: {error:.8f}")
    print(f"Iteraciones realizadas: {iteracion}")
    
    # Graficar resultado final
    graficar_funcion(funcion, expr_str, a, b, raiz=c, iteraciones=puntos_medios)
    
    return c, iteracion, puntos_medios

def mostrar_menu():
   
    print("\n=== MENÚ PRINCIPAL ===")
    print("1. Resolver con método de bisección")
    print("2. Salir")
    
    while True:
        try:
            opcion = int(input("Selecciona una opción: "))
            if opcion in [1, 2]:
                return opcion
            else:
                print("Opción no válida. Intenta nuevamente.")
        except ValueError:
            print("Por favor, ingresa un número.")

def main():
    
    print("=" * 50)
    print("   MÉTODO DE BISECCIÓN CON VISUALIZACIÓN GRÁFICA")
    print("=" * 50)
    
    while True:
        opcion = mostrar_menu()
        
        if opcion == 1:
            # Captar los datos necesarios
            funcion, expr_str = captar_funcion()
            a, b = captar_intervalo()
            tol, max_iter = captar_parametros()
            
            # Ejecutar método de bisección
            metodo_biseccion(funcion, expr_str, a, b, tol, max_iter)
            
        elif opcion == 2:
            print("\n¡Gracias por usar el programa! Hasta pronto.")
            break

if __name__ == "__main__":
    main()