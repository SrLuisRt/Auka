from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.db.models import Q
from django.http import Http404
from .models import NewsItem
from .forms import NewsItemForm

def es_staff(user):
    return user.is_staff

def news_list(request):
    hoy = timezone.now().date()
    

    noticias = NewsItem.objects.filter(publicado=True)


    if not request.user.is_staff:
        noticias = noticias.filter(
            Q(fecha_expiracion__isnull=True) | Q(fecha_expiracion__gte=hoy)
        )

    return render(request, 'novedades/lista_de_novedades.html', {'noticias': noticias})

def news_detail(request, pk):
    hoy = timezone.now().date()
    

    noticia = get_object_or_404(NewsItem, pk=pk)


    if not request.user.is_staff:

        if not noticia.publicado:
            raise Http404("No encontrado")

        if noticia.fecha_expiracion and noticia.fecha_expiracion < hoy:
            raise Http404("Esta noticia ha expirado.")
    
    return render(request, 'novedades/novedades_detalles.html', {'noticia': noticia})

@login_required
@user_passes_test(es_staff)
def news_create(request):
    if request.method == 'POST':
        form = NewsItemForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('novedades:novedades_lista')
    else:
        form = NewsItemForm()
    return render(request, 'novedades/novedades_formulario.html', {'form': form, 'accion': 'Crear'})

@login_required
@user_passes_test(es_staff)
def news_update(request, pk):
    noticia = get_object_or_404(NewsItem, pk=pk)
    if request.method == 'POST':
        form = NewsItemForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            form.save()
           
            return redirect('novedades:novedades_detalles', pk=noticia.pk)
    else:
        form = NewsItemForm(instance=noticia)
    return render(request, 'novedades/novedades_formulario.html', {'form': form, 'accion': 'Editar'})

@login_required
@user_passes_test(es_staff)
def news_delete(request, pk):
    noticia = get_object_or_404(NewsItem, pk=pk)
    if request.method == 'POST':
        noticia.delete()
        return redirect('novedades:novedades_lista')
    return render(request, 'novedades/novedades_confirmar_eliminar.html', {'noticia': noticia})
