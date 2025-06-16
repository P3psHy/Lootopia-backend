from django.http import JsonResponse

def home_view(request):
    return JsonResponse({"message": "Bienvenue sur l'API Lootopia 🚀"})
