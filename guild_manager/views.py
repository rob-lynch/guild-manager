from django.shortcuts import redirect

def redirect_view(request):
    response = redirect('/accounts/discord/login/?process=login')
    return response