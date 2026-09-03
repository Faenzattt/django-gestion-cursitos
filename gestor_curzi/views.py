from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Curso, Leccion

def lista_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'lista_cursos.html', {'cursos': cursos})

def crear_curso(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        nivel = request.POST.get('nivel')
        
        if not titulo or not descripcion:
            return render(request, 'crear_curso.html', {
                'error': 'Este campo es obligatorio',
                'titulo': titulo,
                'descripcion': descripcion
            })
            
        Curso.objects.create(titulo=titulo, descripcion=descripcion, nivel=nivel)
        messages.success(request, f'Curso "{titulo}" creado con éxito.')
        return redirect('lista_cursos')
        
    return render(request, 'crear_curso.html')

def detalle_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    lecciones = curso.lecciones.all().order_by('fecha_creacion')
    return render(request, 'detalle_curso.html', {'curso': curso, 'lecciones': lecciones})

def crear_leccion(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    
    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        contenido = request.POST.get('contenido', '').strip()
        duracion = request.POST.get('duracion', 0)
        estado = request.POST.get('estado', 'Borrador')
        
        if not titulo or not contenido:
            return render(request, 'crear_leccion.html', {
                'curso': curso,
                'error': 'Este campo es obligatorio',
                'titulo': titulo,
                'contenido': contenido
            })
            
        Leccion.objects.create(
            curso=curso,
            titulo=titulo,
            contenido=contenido,
            duracion=duracion,
            estado=estado
        )
        messages.success(request, f'Lección "{titulo}" agregada correctamente.')
        return redirect('detalle_curso', pk=curso.pk)

    return render(request, 'crear_leccion.html', {'curso': curso})
        
        
def editar_leccion(request, pk):
    leccion = get_object_or_404(Leccion, pk=pk)
    curso = leccion.curso
    
    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        contenido = request.POST.get('contenido', '').strip()
        duracion = request.POST.get('duracion', 0)
        estado = request.POST.get('estado', 'Borrador')
        
        if not titulo:
            return render(request, 'editar_leccion.html', {
                'leccion': leccion,
                'curso': curso,
                'error': 'Este campo es obligatorio'
            })
            
        leccion.titulo = titulo
        leccion.contenido = contenido
        leccion.duracion = duracion
        leccion.estado = estado
        leccion.save()
        messages.success(request, f'Lección "{leccion.titulo}" actualizada correctamente.')
        return redirect('detalle_curso', pk=curso.pk)
        
    return render(request, 'editar_leccion.html', {'leccion': leccion, 'curso': curso})

def eliminar_leccion(request, pk):
    leccion = get_object_or_404(Leccion, pk=pk)
    curso = leccion.curso
    
    if request.method == 'POST':
        titulo = leccion.titulo
        leccion.delete()
        messages.success(request, f'Lección "{titulo}" eliminada correctamente.')
        return redirect('detalle_curso', pk=curso.pk)
        
    return render(request, 'eliminar_leccion.html', {'leccion': leccion, 'curso': curso})