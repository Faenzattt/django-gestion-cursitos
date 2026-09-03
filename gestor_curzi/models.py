from django.db import models

class Curso(models.Model):
    NIVELES = [
        ('Principiante', 'Principiante'),
        ('Intermedio', 'Intermedio'),
        ('Avanzado', 'Avanzado'),
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    nivel = models.CharField(max_length=20, choices=NIVELES, default='Principiante')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class Leccion(models.Model):
    ESTADOS = [
        ('Borrador', 'Borrador'),
        ('Publicado', 'Publicado'),
    ]
    
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='lecciones')
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    duracion = models.PositiveIntegerField(default=0, help_text="Duración en minutos")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Borrador')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.curso.titulo}"