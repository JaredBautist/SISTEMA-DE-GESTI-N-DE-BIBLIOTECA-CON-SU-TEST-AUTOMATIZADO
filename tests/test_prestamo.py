"""
Tests unitarios para la clase Prestamo
"""
import pytest
from datetime import datetime, timedelta
from biblioteca.prestamo import Prestamo


class TestPrestamo:
    """Suite de tests para la clase Prestamo"""
    
    def test_crear_prestamo_exitoso(self):
        """Test: Crear un préstamo con parámetros válidos"""
        prestamo = Prestamo("P001", "978-3-16-148410-0", "U001")
        
        assert prestamo.id == "P001"
        assert prestamo.isbn_libro == "978-3-16-148410-0"
        assert prestamo.id_usuario == "U001"
        assert prestamo.fecha_devolucion is None
        assert prestamo.dias_prestamo == 14
    
    def test_crear_prestamo_con_dias_personalizados(self):
        """Test: Crear préstamo con días personalizados"""
        prestamo = Prestamo("P001", "ISBN-001", "U001", dias_prestamo=7)
        
        assert prestamo.dias_prestamo == 7
    
    def test_crear_prestamo_sin_id_falla(self):
        """Test: Crear préstamo sin ID debe lanzar ValueError"""
        with pytest.raises(ValueError, match="El ID del préstamo no puede estar vacío"):
            Prestamo("", "ISBN-001", "U001")
    
    def test_crear_prestamo_sin_isbn_falla(self):
        """Test: Crear préstamo sin ISBN debe lanzar ValueError"""
        with pytest.raises(ValueError, match="El ISBN del libro no puede estar vacío"):
            Prestamo("P001", "", "U001")
    
    def test_crear_prestamo_sin_usuario_falla(self):
        """Test: Crear préstamo sin usuario debe lanzar ValueError"""
        with pytest.raises(ValueError, match="El ID del usuario no puede estar vacío"):
            Prestamo("P001", "ISBN-001", "")
    
    def test_crear_prestamo_dias_invalidos_falla(self):
        """Test: Crear préstamo con días inválidos debe fallar"""
        with pytest.raises(ValueError, match="Los días de préstamo deben ser al menos 1"):
            Prestamo("P001", "ISBN-001", "U001", dias_prestamo=0)
    
    def test_prestamo_esta_activo_inicialmente(self):
        """Test: Préstamo recién creado está activo"""
        prestamo = Prestamo("P001", "ISBN-001", "U001")
        
        assert prestamo.esta_activo() is True
    
    def test_devolver_prestamo_exitoso(self):
        """Test: Devolver un préstamo activo"""
        prestamo = Prestamo("P001", "ISBN-001", "U001")
        
        resultado = prestamo.devolver()
        
        assert resultado is True
        assert prestamo.esta_activo() is False
        assert prestamo.fecha_devolucion is not None
    
    def test_devolver_prestamo_ya_devuelto_falla(self):
        """Test: Devolver un préstamo ya devuelto debe fallar"""
        prestamo = Prestamo("P001", "ISBN-001", "U001")
        prestamo.devolver()
        
        with pytest.raises(ValueError, match="ya fue devuelto"):
            prestamo.devolver()
    
    def test_dias_transcurridos_sin_devolver(self):
        """Test: Calcular días transcurridos de préstamo activo"""
        prestamo = Prestamo("P001", "ISBN-001", "U001")
        # El préstamo se crea con fecha actual
        
        dias = prestamo.dias_transcurridos()
        
        assert dias == 0  # Mismo día
    
    def test_prestamo_no_vencido_inicialmente(self):
        """Test: Préstamo recién creado no está vencido"""
        prestamo = Prestamo("P001", "ISBN-001", "U001", dias_prestamo=14)
        
        assert prestamo.esta_vencido() is False
    
    def test_dias_restantes_prestamo_activo(self):
        """Test: Calcular días restantes de préstamo activo"""
        prestamo = Prestamo("P001", "ISBN-001", "U001", dias_prestamo=14)
        
        dias_restantes = prestamo.dias_restantes()
        
        assert dias_restantes == 14  # Mismo día de creación
    
    def test_dias_restantes_prestamo_devuelto(self):
        """Test: Días restantes de préstamo devuelto es 0"""
        prestamo = Prestamo("P001", "ISBN-001", "U001")
        prestamo.devolver()
        
        assert prestamo.dias_restantes() == 0
    
    def test_prestamo_vencido_no_esta_activo(self):
        """Test: Préstamo devuelto no puede estar vencido"""
        prestamo = Prestamo("P001", "ISBN-001", "U001", dias_prestamo=1)
        prestamo.devolver()
        
        assert prestamo.esta_vencido() is False
    
    def test_str_representation_activo(self):
        """Test: Representación en string de préstamo activo"""
        prestamo = Prestamo("P001", "ISBN-001", "U001")
        
        str_prestamo = str(prestamo)
        
        assert "P001" in str_prestamo
        assert "ISBN-001" in str_prestamo
        assert "U001" in str_prestamo
        assert "Activo" in str_prestamo
    
    def test_str_representation_devuelto(self):
        """Test: Representación en string de préstamo devuelto"""
        prestamo = Prestamo("P001", "ISBN-001", "U001")
        prestamo.devolver()
        
        str_prestamo = str(prestamo)
        
        assert "Devuelto" in str_prestamo