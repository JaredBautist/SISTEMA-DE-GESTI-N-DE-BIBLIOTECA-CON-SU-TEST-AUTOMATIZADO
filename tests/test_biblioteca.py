"""
Tests unitarios para la clase Biblioteca
"""
import pytest
from biblioteca.biblioteca import Biblioteca
from biblioteca.libro import Libro
from biblioteca.usuario import Usuario


class TestBiblioteca:
    """Suite de tests para la clase Biblioteca"""
    
    @pytest.fixture
    def biblioteca(self):
        """Fixture: Biblioteca vacía para tests"""
        return Biblioteca("Biblioteca de Pruebas")
    
    @pytest.fixture
    def libro_ejemplo(self):
        """Fixture: Libro de ejemplo"""
        return Libro("978-3-16-148410-0", "Clean Code", "Robert C. Martin")
    
    @pytest.fixture
    def usuario_ejemplo(self):
        """Fixture: Usuario de ejemplo"""
        return Usuario("U001", "Juan Pérez")
    
    # ==================== TESTS DE LIBROS ====================
    
    def test_crear_biblioteca(self, biblioteca):
        """Test: Crear biblioteca con nombre"""
        assert biblioteca.nombre == "Biblioteca de Pruebas"
        assert biblioteca.total_libros() == 0
        assert biblioteca.total_usuarios() == 0
    
    def test_agregar_libro_exitoso(self, biblioteca, libro_ejemplo):
        """Test: Agregar un libro al catálogo"""
        resultado = biblioteca.agregar_libro(libro_ejemplo)
        
        assert resultado is True
        assert biblioteca.total_libros() == 1
        assert biblioteca.buscar_libro_por_isbn("978-3-16-148410-0") == libro_ejemplo
    
    def test_agregar_libro_duplicado_falla(self, biblioteca, libro_ejemplo):
        """Test: Agregar libro duplicado debe fallar"""
        biblioteca.agregar_libro(libro_ejemplo)
        
        with pytest.raises(ValueError, match="ya existe en el catálogo"):
            biblioteca.agregar_libro(libro_ejemplo)
    
    def test_buscar_libro_por_isbn_existente(self, biblioteca, libro_ejemplo):
        """Test: Buscar libro por ISBN que existe"""
        biblioteca.agregar_libro(libro_ejemplo)
        
        libro = biblioteca.buscar_libro_por_isbn("978-3-16-148410-0")
        
        assert libro == libro_ejemplo
    
    def test_buscar_libro_por_isbn_inexistente(self, biblioteca):
        """Test: Buscar libro por ISBN que no existe"""
        libro = biblioteca.buscar_libro_por_isbn("ISBN-INEXISTENTE")
        
        assert libro is None
    
    def test_buscar_libros_por_titulo(self, biblioteca):
        """Test: Buscar libros por título (parcial)"""
        biblioteca.agregar_libro(Libro("ISBN-001", "Clean Code", "Robert Martin"))
        biblioteca.agregar_libro(Libro("ISBN-002", "Clean Architecture", "Robert Martin"))
        biblioteca.agregar_libro(Libro("ISBN-003", "Dirty Code", "Otro Autor"))
        
        resultados = biblioteca.buscar_libros_por_titulo("Clean")
        
        assert len(resultados) == 2
        assert all("Clean" in libro.titulo for libro in resultados)
    
    def test_buscar_libros_por_autor(self, biblioteca):
        """Test: Buscar libros por autor"""
        biblioteca.agregar_libro(Libro("ISBN-001", "Clean Code", "Robert C. Martin"))
        biblioteca.agregar_libro(Libro("ISBN-002", "Clean Architecture", "Robert C. Martin"))
        biblioteca.agregar_libro(Libro("ISBN-003", "Otro Libro", "Otro Autor"))
        
        resultados = biblioteca.buscar_libros_por_autor("Robert")
        
        assert len(resultados) == 2
    
    def test_libros_disponibles(self, biblioteca):
        """Test: Obtener libros disponibles"""
        libro1 = Libro("ISBN-001", "Libro 1", "Autor 1")
        libro2 = Libro("ISBN-002", "Libro 2", "Autor 2")
        biblioteca.agregar_libro(libro1)
        biblioteca.agregar_libro(libro2)
        libro1.prestar()
        
        disponibles = biblioteca.libros_disponibles()
        
        assert len(disponibles) == 1
        assert libro2 in disponibles
    
    # ==================== TESTS DE USUARIOS ====================
    
    def test_registrar_usuario_exitoso(self, biblioteca, usuario_ejemplo):
        """Test: Registrar un nuevo usuario"""
        resultado = biblioteca.registrar_usuario(usuario_ejemplo)
        
        assert resultado is True
        assert biblioteca.total_usuarios() == 1
        assert biblioteca.buscar_usuario("U001") == usuario_ejemplo
    
    def test_registrar_usuario_duplicado_falla(self, biblioteca, usuario_ejemplo):
        """Test: Registrar usuario duplicado debe fallar"""
        biblioteca.registrar_usuario(usuario_ejemplo)
        
        with pytest.raises(ValueError, match="ya está registrado"):
            biblioteca.registrar_usuario(usuario_ejemplo)
    
    def test_buscar_usuario_existente(self, biblioteca, usuario_ejemplo):
        """Test: Buscar usuario que existe"""
        biblioteca.registrar_usuario(usuario_ejemplo)
        
        usuario = biblioteca.buscar_usuario("U001")
        
        assert usuario == usuario_ejemplo
    
    def test_buscar_usuario_inexistente(self, biblioteca):
        """Test: Buscar usuario que no existe"""
        usuario = biblioteca.buscar_usuario("U999")
        
        assert usuario is None
    
    # ==================== TESTS DE PRÉSTAMOS ====================
    
    def test_prestar_libro_exitoso(self, biblioteca, libro_ejemplo, usuario_ejemplo):
        """Test: Realizar un préstamo exitoso"""
        biblioteca.agregar_libro(libro_ejemplo)
        biblioteca.registrar_usuario(usuario_ejemplo)
        
        prestamo = biblioteca.prestar_libro("978-3-16-148410-0", "U001")
        
        assert prestamo is not None
        assert prestamo.isbn_libro == "978-3-16-148410-0"
        assert prestamo.id_usuario == "U001"
        assert not libro_ejemplo.disponible
        assert "978-3-16-148410-0" in usuario_ejemplo.libros_prestados
    
    def test_prestar_libro_inexistente_falla(self, biblioteca, usuario_ejemplo):
        """Test: Prestar libro que no existe debe fallar"""
        biblioteca.registrar_usuario(usuario_ejemplo)
        
        with pytest.raises(ValueError, match="no existe en el catálogo"):
            biblioteca.prestar_libro("ISBN-INEXISTENTE", "U001")
    
    def test_prestar_libro_no_disponible_falla(self, biblioteca, libro_ejemplo, usuario_ejemplo):
        """Test: Prestar libro no disponible debe fallar"""
        biblioteca.agregar_libro(libro_ejemplo)
        biblioteca.registrar_usuario(usuario_ejemplo)
        biblioteca.registrar_usuario(Usuario("U002", "Otro Usuario"))
        biblioteca.prestar_libro("978-3-16-148410-0", "U001")
        
        with pytest.raises(ValueError, match="no está disponible"):
            biblioteca.prestar_libro("978-3-16-148410-0", "U002")
    
    def test_prestar_libro_usuario_inexistente_falla(self, biblioteca, libro_ejemplo):
        """Test: Prestar libro a usuario inexistente debe fallar"""
        biblioteca.agregar_libro(libro_ejemplo)
        
        with pytest.raises(ValueError, match="no está registrado"):
            biblioteca.prestar_libro("978-3-16-148410-0", "U999")
    
    def test_prestar_libro_usuario_limite_alcanzado_falla(self, biblioteca):
        """Test: Prestar libro cuando usuario alcanzó límite debe fallar"""
        usuario = Usuario("U001", "Juan Pérez", limite_prestamos=1)
        biblioteca.registrar_usuario(usuario)
        biblioteca.agregar_libro(Libro("ISBN-001", "Libro 1", "Autor 1"))
        biblioteca.agregar_libro(Libro("ISBN-002", "Libro 2", "Autor 2"))
        biblioteca.prestar_libro("ISBN-001", "U001")
        
        with pytest.raises(ValueError, match="ha alcanzado el límite"):
            biblioteca.prestar_libro("ISBN-002", "U001")
    
    def test_devolver_libro_exitoso(self, biblioteca, libro_ejemplo, usuario_ejemplo):
        """Test: Devolver un libro prestado"""
        biblioteca.agregar_libro(libro_ejemplo)
        biblioteca.registrar_usuario(usuario_ejemplo)
        biblioteca.prestar_libro("978-3-16-148410-0", "U001")
        
        resultado = biblioteca.devolver_libro("978-3-16-148410-0", "U001")
        
        assert resultado is True
        assert libro_ejemplo.disponible
        assert "978-3-16-148410-0" not in usuario_ejemplo.libros_prestados
    
    def test_devolver_libro_sin_prestamo_activo_falla(self, biblioteca, libro_ejemplo, usuario_ejemplo):
        """Test: Devolver libro sin préstamo activo debe fallar"""
        biblioteca.agregar_libro(libro_ejemplo)
        biblioteca.registrar_usuario(usuario_ejemplo)
        
        with pytest.raises(ValueError, match="No existe un préstamo activo"):
            biblioteca.devolver_libro("978-3-16-148410-0", "U001")
    
    def test_prestamos_activos(self, biblioteca):
        """Test: Obtener préstamos activos"""
        biblioteca.agregar_libro(Libro("ISBN-001", "Libro 1", "Autor 1"))
        biblioteca.agregar_libro(Libro("ISBN-002", "Libro 2", "Autor 2"))
        biblioteca.registrar_usuario(Usuario("U001", "Usuario 1"))
        biblioteca.prestar_libro("ISBN-001", "U001")
        prestamo2 = biblioteca.prestar_libro("ISBN-002", "U001")
        biblioteca.devolver_libro("ISBN-001", "U001")
        
        activos = biblioteca.prestamos_activos()
        
        assert len(activos) == 1
        assert prestamo2 in activos
    
    def test_prestamos_usuario(self, biblioteca):
        """Test: Obtener préstamos de un usuario específico"""
        biblioteca.agregar_libro(Libro("ISBN-001", "Libro 1", "Autor 1"))
        biblioteca.registrar_usuario(Usuario("U001", "Usuario 1"))
        biblioteca.registrar_usuario(Usuario("U002", "Usuario 2"))
        biblioteca.prestar_libro("ISBN-001", "U001")
        
        prestamos = biblioteca.prestamos_usuario("U001")
        
        assert len(prestamos) == 1
        assert prestamos[0].id_usuario == "U001"
    
    # ==================== TESTS DE ESTADÍSTICAS ====================
    
    def test_estadisticas_biblioteca_vacia(self, biblioteca):
        """Test: Estadísticas de biblioteca vacía"""
        stats = biblioteca.estadisticas()
        
        assert stats['total_libros'] == 0
        assert stats['libros_disponibles'] == 0
        assert stats['total_usuarios'] == 0
        assert stats['total_prestamos'] == 0
    
    def test_estadisticas_biblioteca_con_datos(self, biblioteca):
        """Test: Estadísticas con datos"""
        biblioteca.agregar_libro(Libro("ISBN-001", "Libro 1", "Autor 1"))
        biblioteca.agregar_libro(Libro("ISBN-002", "Libro 2", "Autor 2"))
        biblioteca.registrar_usuario(Usuario("U001", "Usuario 1"))
        biblioteca.prestar_libro("ISBN-001", "U001")
        
        stats = biblioteca.estadisticas()
        
        assert stats['total_libros'] == 2
        assert stats['libros_disponibles'] == 1
        assert stats['libros_prestados'] == 1
        assert stats['total_usuarios'] == 1
        assert stats['prestamos_activos'] == 1