from django.shortcuts import redirect, render

def main(request):
    if request.user.is_authenticated:
        return redirect('/cedis/consulta_udis')
    else:
        return redirect('/cedis/login')
    
