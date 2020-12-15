from django.shortcuts import render
from datetime import datetime

# Create your views here.
def index(request):
    return render(request,'home/home.html')

def consulta_udis(request):
    hoy = datetime.today().strftime("%d-%m-%Y")
    return render(request,'udis/home.html',{'hoy':hoy})

def consulta_tiie(request):
    hoy = datetime.today().strftime("%d-%m-%Y")
    return render(request,'tiie/home.html',{'hoy':hoy})
