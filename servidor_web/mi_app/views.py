from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import lista

# ------------------------------
# REGISTRO
# ------------------------------
def registro(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")

        if not username:
            return render(request, 'mi_app/registro.html', {
                "error": "El nombre de usuario no puede estar vacío."
            })

        if password != password1:
            return render(request, 'mi_app/registro.html', {
                "error": "Las contraseñas no coinciden."
            })

        user = User.objects.create_user(username=username, password=password)
        return redirect('login')

    return render(request, 'mi_app/registro.html')

# ------------------------------
# LOGIN
# ------------------------------
def inicio_sesion(request):
    if request.method == "POST":
        username = request.POST.get("user_login")
        password = request.POST.get("pass_login")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('lista_tareas')

        return render(request, 'mi_app/login.html', {"error": "Credenciales incorrectas"})

    return render(request, 'mi_app/login.html')

# ------------------------------
# LOGOUT
# ------------------------------
def salir(request):
    logout(request)
    return redirect('login')

# ------------------------------
# LISTA DE TAREAS (REQUIERE LOGIN)
# ------------------------------
@login_required
def lista_tareas(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        if nombre:
            lista.objects.create(
                nombre=nombre,
                usuario=request.user
            )

    tareas = lista.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'mi_app/index.html', {'tareas': tareas})

# ------------------------------
# MARCAR COMO COMPLETADA
# ------------------------------
@login_required
def completar_tarea(request, tarea_id):
    tarea = lista.objects.get(id=tarea_id, usuario=request.user)
    tarea.completada = True
    tarea.save()
    return redirect('lista_tareas')


# ------------------------------
# ELIMINAR TAREA
# ------------------------------
@login_required
def eliminar_tarea(request, tarea_id):
    tarea = lista.objects.get(id=tarea_id, usuario=request.user)
    tarea.delete()
    return redirect('lista_tareas')

