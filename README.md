# 📘 Backend - Proyecto Análisis Numérico

Este backend proporciona los cálculos numéricos necesarios para la aplicación del proyecto final del curso de Análisis Numérico. Está diseñado para funcionar junto a un frontend separado, usando FastAPI como servidor web.

---

## 📚 Capítulos y Métodos

### 🔹 Capítulo 1: Métodos para encontrar raíces de ecuaciones no lineales

| Método              | Parámetros requeridos                         |
|---------------------|-----------------------------------------------|
| Bisección           | `f(x)`, `a`, `b`, `tol`, `max_iter`           |
| Regla Falsa         | `f(x)`, `a`, `b`, `tol`, `max_iter`           |
| Punto Fijo          | `g(x)`, `x0`, `tol`, `max_iter`               |
| Newton-Raphson      | `f(x)`, `x0`, `tol`, `max_iter`, `f'(x)`*     |
| Secante             | `f(x)`, `x0`, `x1`, `tol`, `max_iter`         |
| Raíces Múltiples    | `f(x)`, `x0`, `tol`, `max_iter`, `f'(x)`, `f''(x)`* |

> \* Las derivadas pueden ser calculadas automáticamente si no se proporcionan.

---

### 🔹 Capítulo 2: Solución de sistemas de ecuaciones lineales

| Método          | Parámetros requeridos                            |
|------------------|--------------------------------------------------|
| Jacobi           | `matriz_A`, `vector_b`, `x0`, `tol`, `max_iter` |
| Gauss-Seidel     | `matriz_A`, `vector_b`, `x0`, `tol`, `max_iter` |
| SOR              | `matriz_A`, `vector_b`, `x0`, `tol`, `max_iter`, `omega` |

> Se aceptan matrices de hasta 7x7.

---

### 🔹 Capítulo 3: Interpolación

| Método              | Parámetros requeridos         |
|---------------------|-------------------------------|
| Vandermonde         | Lista de puntos `(x, y)`      |
| Newton Interpolante | Lista de puntos `(x, y)`      |
| Lagrange            | Lista de puntos `(x, y)`      |
| Spline Lineal       | Lista de puntos `(x, y)`      |
| Spline Cúbico       | Lista de puntos `(x, y)`      |

> Se aceptan hasta 8 puntos para interpolación.

---

## 🔀 Opción 2 - Interfaz Dinámica por Modo de Uso

El backend está diseñado para soportar dos modos principales de operación, definidos por el cliente (frontend):

### 🧪 1. **Modo Individual**
El usuario elige un método específico para resolver un problema.

- El backend recibe únicamente los parámetros requeridos por ese método.
- Retorna:
  - Tabla de iteraciones o polinomio
  - Gráfica (como datos para renderizar)
  - Errores y mensajes explicativos

### 📊 2. **Modo Comparativo**
El usuario solicita **comparar todos los métodos** de un capítulo sobre un mismo problema.

- El frontend debe enviar **todos los parámetros requeridos para todos los métodos del capítulo.**
- Si algún método no tiene parámetros suficientes, **será omitido automáticamente** en la comparación y se notificará.
- El backend:
  - Ejecuta todos los métodos con los datos disponibles
  - Compara tiempo de ejecución, número de iteraciones, precisión, etc.
  - Retorna un informe con:
    - Tabla resumen de todos los métodos
    - Mejor método determinado según criterios
    - Detalles de ejecución de cada uno

---

## 🛠️ Funcionalidades Backend

- 📈 Cálculo de tablas y gráficas
- 🔁 Derivación automática con SymPy
- 🧠 Verificación de convergencia (ej. radio espectral en Cap. 2)
- 📄 Generación de informe automático (JSON, PDF opcional)
- 📦 APIs organizadas por capítulo y método

---

## 🚀 Cómo iniciar

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  #  ---> En Windows: venv\Scripts\activate <---

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor -- ojo pues, tienen que estar en la carpeta app jajjaja
python main.py
