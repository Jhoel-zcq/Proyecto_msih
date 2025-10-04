from django.shortcuts import render , redirect
from django.http import HttpResponse
# Create your views here.

#paginas html
def index(request):
    return render(request,'prueba/index.html' )

def funcion(request):
    return render(request,"prueba/funcion.html")

def ejercitar(request):
    return render(request,"prueba/ejercitar.html")

def sandbox(request):
    return render(request, "prueba/sandbox.html")

def inicio(request):
    return render(request, 'prueba/index.html')

# blog/views.py
from .models import Post

def lista_posts(request):#es el inicio
    posts = Post.objects.all()  
    return render(request, 'prueba/lista_posts.html', {'posts': posts})

# vista para crear un post
from .forms import PostForm

def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():  # Valida datos automáticamente
            form.save()      # Guarda en la base de datos
            return redirect('lista_posts')
    else:
        form = PostForm()
    return render(request, 'prueba/crear_post.html', {'form': form})
