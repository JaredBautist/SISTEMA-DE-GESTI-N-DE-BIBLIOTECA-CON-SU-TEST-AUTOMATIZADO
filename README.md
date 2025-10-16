# 📚 Sistema de Gestión de Biblioteca

Sistema completo de gestión de biblioteca con suite de pruebas automatizadas desarrollado en Python.

## 🎯 Características

- ✅ Gestión completa de libros (CRUD)
- ✅ Registro y gestión de usuarios
- ✅ Sistema de préstamos y devoluciones
- ✅ Búsqueda avanzada por ISBN, título y autor
- ✅ Control de límites de préstamos por usuario
- ✅ Seguimiento de préstamos activos y vencidos
- ✅ Estadísticas del sistema

## 🏗️ Estructura del Proyecto

```
sistema-biblioteca/
│
├── biblioteca/           # Código fuente
│   ├── __init__.py
│   ├── libro.py         # Clase Libro
│   ├── usuario.py       # Clase Usuario
│   ├── prestamo.py      # Clase Prestamo
│   └── biblioteca.py    # Clase Biblioteca (sistema principal)
│
├── tests/               # Suite de pruebas
│   ├── test_libro.py
│   ├── test_usuario.py
│   ├── test_prestamo.py
│   ├── test_biblioteca.py
│   └── test_integracion.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio:**

```bash
git clone https://github.com/JaredBautist/SISTEMA-DE-GESTI-N-DE-BIBLIOTECA-CON-SU-TEST-AUTOMATIZADO.git
cd sistema-biblioteca
```

    2 .**Instalar dependencias:**

```bash
pip install -r requirements.txt
```

## 🧪 Ejecución de Pruebas

### Ejecutar todas las pruebas

```bash
pytest tests/ -v
```

### Ejecutar pruebas con reporte de cobertura

```bash
pytest tests/ -v --cov=biblioteca --cov-report=html
```

### Ver reporte de cobertura en navegador

Después de ejecutar las pruebas con cobertura:

```bash
# El reporte se genera en htmlcov/index.html
# Abrirlo con tu navegador favorito
```

### Ejecutar pruebas específicas

```bash
# Solo tests de una clase específica
pytest tests/test_libro.py -v

# Solo un test específico
pytest tests/test_biblioteca.py::TestBiblioteca::test_prestar_libro_exitoso -v
```

## 💻 Uso del Sistema

### Ejemplo Básico

```python
from biblioteca import Biblioteca, Libro, Usuario

# Crear biblioteca
biblioteca = Biblioteca("Mi Biblioteca")

# Agregar libros
libro = Libro("978-0-13-468599-1", "Clean Architecture", "Robert C. Martin")
biblioteca.agregar_libro(libro)

# Registrar usuario
usuario = Usuario("U001", "Juan Pérez", "juan@email.com")
biblioteca.registrar_usuario(usuario)

# Realizar préstamo
prestamo = biblioteca.prestar_libro("978-0-13-468599-1", "U001")
print(f"Préstamo creado: {prestamo}")

# Devolver libro
biblioteca.devolver_libro("978-0-13-468599-1", "U001")

# Ver estadísticas
stats = biblioteca.estadisticas()
print(stats)
```

## 📊 Cobertura de Pruebas

El proyecto incluye **más de 70 pruebas unitarias y de integración** que cubren:

- ✅ Creación y validación de objetos
- ✅ Manejo de excepciones
- ✅ Operaciones CRUD completas
- ✅ Flujos de negocio (préstamos, devoluciones)
- ✅ Búsquedas y filtros
- ✅ Límites y restricciones
- ✅ Pruebas parametrizadas
- ✅ Tests de integración

**Cobertura objetivo:** Mínimo 80%

## 🔍 Características Técnicas

### Clases Principales

1. **Libro:** Representa un libro con ISBN, título, autor y disponibilidad
2. **Usuario:** Maneja usuarios con límites de préstamos personalizables
3. **Prestamo:** Controla préstamos con fechas y seguimiento de vencimientos
4. **Biblioteca:** Sistema central que coordina todas las operaciones

### Funcionalidades Core

- Agregar libros al catálogo
- Prestar y devolver libros
- Buscar por ISBN, título y autor
- Control de disponibilidad
- Límites de préstamos por usuario
- Seguimiento de préstamos activos y vencidos
- Estadísticas del sistema

## 📈 Testing Manual vs Automatizado

### Tiempo Estimado: Testing Manual

- Configuración inicial: 10 min
- Prueba de cada funcionalidad: 5-8 min
- Total para 70+ escenarios: **~8 horas**
- Regresión completa por cambio: **4-6 horas**

### Tiempo Estimado: Testing Automatizado

- Configuración inicial: 2 min
- Ejecución completa de suite: **5-10 segundos**
- Regresión completa: **5-10 segundos**

### Beneficios del Testing Automatizado

✅ **Velocidad:** 1000x más rápido que testing manual
✅ **Consistencia:** Mismas pruebas cada vez
✅ **Confianza:** Detecta regresiones inmediatamente
✅ **Documentación:** Los tests documentan el comportamiento esperado
✅ **Refactoring seguro:** Permite mejorar código con confianza
