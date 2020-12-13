from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'home/home.html')

def consulta_cedis(request):
    return render(request,'cedis/home.html')

def consulta_tiie(request):
    return render(request,'tiie/home.html')
