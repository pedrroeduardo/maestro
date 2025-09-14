from django.shortcuts import render

# modules/core/views.py
from django.contrib import messages
from django.shortcuts import render

def demo(request):
    messages.success(request, "Login realizado com sucesso!")
    messages.info(request, "Você está no ambiente de testes do Maestro.")
    return render(request, "core/demo.html")

