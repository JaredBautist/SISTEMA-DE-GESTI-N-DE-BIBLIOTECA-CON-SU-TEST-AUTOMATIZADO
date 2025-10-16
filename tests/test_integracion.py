"""
Tests de integración para el sistema completo de biblioteca
"""
import pytest
from biblioteca.biblioteca import Biblioteca
from biblioteca.libro import Libro
from biblioteca.usuario import Usuario


class TestIntegracion:
    """Suite de tests de integración"""
    
    @pytest.fixture
    def sistema_biblioteca(self):
        """Fixture: Sistema de biblioteca completo con datos de prueba"""
        biblioteca = Biblioteca("Biblioteca Central")
        
        # Agregar libros
        biblioteca.agregar_libro(Libro("978-0-13-468599-1", "Clean Architecture", "Robert C. Martin"))
        biblioteca.agregar_libro(Libro("978-0-13-235088-4", "Clean Code", "Robert C. Martin"))
        biblioteca.agregar_libro(Libro("978-0-201-63361-0", "Design Patterns", "Gang of Four"))
        biblioteca.agregar_libro(Libro("978-0-13-475759-9", "Refactoring", "Martin Fowler"))
        
        # Registrar usuarios
        biblioteca.registrar_usuario(Usuario("U001", "Ana García", "ana@email.com"))
        biblioteca.registrar_usuario(Usuario("U002", "Carlos López", "carlos@email.com", limite_prestamos=2))
        biblioteca.registrar_usuario(Usuario("U003", "María Rodríguez", "maria@email.com"))
        
        return biblioteca
    
    def test_flujo_completo_prestamo_y_devolucion(self, sistema_biblioteca):
        """Test: Flujo completo de préstamo y devolución"""
        # 1. Verificar estado inicial
        assert sistema_biblioteca.total_libros() == 4
        assert len(sistema_biblioteca.libros_disponibles()) == 4
        
        # 2. Realizar préstamo
        prestamo = sistema_biblioteca.prestar_libro("978-0-13-468599-1", "U001")
        assert prestamo is not None
        
        # 3. Verificar cambios después del préstamo
        libro = sistema_biblioteca.buscar_libro_por_isbn("978-0-13-468599-1")
        usuario = sistema_biblioteca.buscar_usuario("U001")
        assert not libro.disponible
        assert "978-0-13-468599-1" in usuario.libros_prestados
        assert len(sistema_biblioteca.libros_disponibles()) == 3
        
        # 4. Devolver libro
        resultado = sistema_biblioteca.devolver_libro("978-0-13-468599-1", "U001")
        assert resultado is True
        
        # 5. Verificar estado final
        assert libro.disponible
        assert "978-0-13-468599-1" not in usuario.libros_prestados
        assert len(sistema_biblioteca.libros_disponibles()) == 4
    
    def test_multiples_prestamos_simultaneos(self, sistema_biblioteca):
        """Test: Usuario con múltiples préstamos simultáneos"""
        usuario = sistema_biblioteca.buscar_usuario("U001")
        
        # Realizar múltiples préstamos
        sistema_biblioteca.prestar_libro("978-0-13-468599-1", "U001")
        sistema_biblioteca.prestar_libro("978-0-13-235088-4", "U001")
        sistema_biblioteca.prestar_libro("978-0-201-63361-0", "U001")
        
        # Verificar
        assert usuario.numero_prestamos() == 3
        assert not usuario.puede_prestar()
        assert len(sistema_biblioteca.prestamos_activos()) == 3
    
    def test_busqueda_y_prestamo_por_titulo(self, sistema_biblioteca):
        """Test: Buscar libro por título y prestarlo"""
        # Buscar libros de "Clean"
        libros = sistema_biblioteca.buscar_libros_por_titulo("Clean")
        assert len(libros) == 2
        
        # Prestar el primero encontrado
        libro = libros[0]
        prestamo = sistema_biblioteca.prestar_libro(libro.isbn, "U002")
        
        assert prestamo.isbn_libro == libro.isbn
        assert not libro.disponible
    
    def test_busqueda_y_prestamo_por_autor(self, sistema_biblioteca):
        """Test: Buscar libros por autor y prestarlos"""
        # Buscar libros de Robert C. Martin
        libros = sistema_biblioteca.buscar_libros_por_autor("Robert C. Martin")
        assert len(libros) == 2
        
        # Prestar ambos libros a diferentes usuarios
        sistema_biblioteca.prestar_libro(libros[0].isbn, "U001")
        sistema_biblioteca.prestar_libro(libros[1].isbn, "U002")
        
        # Verificar que ninguno está disponible
        libros_actualizados = sistema_biblioteca.buscar_libros_por_autor("Robert C. Martin")
        assert all(not libro.disponible for libro in libros_actualizados)
    
    def test_limite_prestamos_usuario(self, sistema_biblioteca):
        """Test: Validar límite de préstamos por usuario"""
        # Usuario U002 tiene límite de 2 préstamos
        usuario = sistema_biblioteca.buscar_usuario("U002")
        
        # Prestar 2 libros
        sistema_biblioteca.prestar_libro("978-0-13-468599-1", "U002")
        sistema_biblioteca.prestar_libro("978-0-13-235088-4", "U002")
        
        # Intentar prestar un tercero debe fallar
        with pytest.raises(ValueError, match="ha alcanzado el límite"):
            sistema_biblioteca.prestar_libro("978-0-201-63361-0", "U002")
        
        # Devolver uno y poder prestar otro
        sistema_biblioteca.devolver_libro("978-0-13-468599-1", "U002")
        prestamo = sistema_biblioteca.prestar_libro("978-0-201-63361-0", "U002")
        assert prestamo is not None
    
    def test_intentar_prestar_libro_ya_prestado(self, sistema_biblioteca):
        """Test: Intentar prestar un libro ya prestado debe fallar"""
        # Usuario 1 presta el libro
        sistema_biblioteca.prestar_libro("978-0-13-468599-1", "U001")
        
        # Usuario 2 intenta prestar el mismo libro
        with pytest.raises(ValueError, match="no está disponible"):
            sistema_biblioteca.prestar_libro("978-0-13-468599-1", "U002")
    
    @pytest.mark.parametrize("termino_busqueda,resultados_esperados", [
        ("Clean", 2),
        ("Design", 1),
        ("Python", 0),
        ("Refactoring", 1),
        ("", 4),  # Búsqueda vacía debería retornar todos
    ])
    def test_busqueda_parametrizada_titulos(self, sistema_biblioteca, termino_busqueda, resultados_esperados):
        """Test: Búsqueda de libros con diferentes términos (parametrizado)"""
        resultados = sistema_biblioteca.buscar_libros_por_titulo(termino_busqueda)
        assert len(resultados) == resultados_esperados
    
    @pytest.mark.parametrize("autor,resultados_esperados", [
        ("Robert C. Martin", 2),
        ("Martin Fowler", 1),
        ("Gang of Four", 1),
        ("Inexistente", 0),
    ])
    def test_busqueda_parametrizada_autores(self, sistema_biblioteca, autor, resultados_esperados):
        """Test: Búsqueda por autor con diferentes términos (parametrizado)"""
        resultados = sistema_biblioteca.buscar_libros_por_autor(autor)
        assert len(resultados) == resultados_esperados
    
    def test_estadisticas_sistema_completo(self, sistema_biblioteca):
        """Test: Validar estadísticas del sistema con actividad"""
        # Realizar algunas operaciones
        sistema_biblioteca.prestar_libro("978-0-13-468599-1", "U001")
        sistema_biblioteca.prestar_libro("978-0-13-235088-4", "U002")
        sistema_biblioteca.devolver_libro("978-0-13-468599-1", "U001")
        
        # Obtener estadísticas
        stats = sistema_biblioteca.estadisticas()
        
        assert stats['total_libros'] == 4
        assert stats['libros_disponibles'] == 3
        assert stats['libros_prestados'] == 1
        assert stats['total_usuarios'] == 3
        assert stats['total_prestamos'] == 2
        assert stats['prestamos_activos'] == 1