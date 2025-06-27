from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class StoreAPIView(APIView):
    """
    API endpoint qui fournit les données de la boutique.
    """
    
    @swagger_auto_schema(
        operation_description="Récupérer les éléments de la boutique",
        operation_summary="Obtenir les données de la boutique",
        responses={
            200: openapi.Response(
                description="Succès",
                examples={
                    "application/json": [
                        {
                            "section": "Boutique",
                            "items": [
                                {"id": 1, "label": "Cadeau journalier", "crowns": 10}
                            ]
                        },
                        {
                            "section": "Partenaires",
                            "items": [
                                {"id": 2, "label": "Bon d'achat Puy du Fou 5%", "crowns": 35},
                                {"id": 3, "label": "Carte cadeau Fnac 10€", "crowns": 90}
                            ]
                        },
                        {
                            "section": "Couronnes",
                            "items": [
                                {"id": 101, "amount": 10, "price": "1,19 €"},
                                {"id": 102, "amount": 25, "price": "2,79 €"}
                            ]
                        }
                    ]
                }
            )
        }
    )
    def get(self, request, format=None):
        """
        Renvoie les données de la boutique.
        """
        store_data = [
            {
                "section": "Boutique",
                "items": [
                    {"id": 1, "label": "Cadeau journalier", "crowns": 10}
                ]
            },
            {
                "section": "Partenaires",
                "items": [
                    {"id": 2, "label": "Bon d'achat Puy du Fou 5%", "crowns": 35},
                    {"id": 3, "label": "Carte cadeau Fnac 10€", "crowns": 90}
                ]
            },
            {
                "section": "Couronnes",
                "items": [
                    {"id": 101, "amount": 10, "price": "1,19 €"},
                    {"id": 102, "amount": 25, "price": "2,79 €"}
                ]
            }
        ]
        
        return Response(store_data)
