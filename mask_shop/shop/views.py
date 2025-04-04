from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def home(request):
    return render(request, 'shop/home.html')  # Обратите внимание на путь

def about(request):
    return render(request, 'shop/about.html')

def author(request):
    return render(request, 'shop/author.html')

  
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
import json
from pathlib import Path
from django.conf import settings

class QualificationViewSet(ViewSet):
    def list(self, request):
        """GET /spec/ - список всех квалификаций"""
        try:
            file_path = Path(settings.BASE_DIR) / 'dump.json'
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            qualifications = [
                {
                    "id": item["pk"],
                    "title": item["fields"]["title"],
                    "code": item["fields"]["code"],
                    "link": f"{request.build_absolute_uri('/')}spec/{item['pk']}/"
                }
                for item in data if item.get("model") == "data.skill"
            ]
            
            return Response({
                "count": len(qualifications),
                "results": qualifications,
                "links": {
                    "self": request.build_absolute_uri()
                }
            })
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        """GET /spec/<pk>/ - детали квалификации"""
        try:
            file_path = Path(settings.BASE_DIR) / 'dump.json'
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            qualification = next(
                (item for item in data 
                 if item.get("model") == "data.skill" and item["pk"] == int(pk)),
                None
            )
            
            if not qualification:
                return Response(
                    {"error": f"Квалификация с ID {pk} не найдена"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            return Response({
                "id": qualification["pk"],
                "code": qualification["fields"]["code"],
                "title": qualification["fields"]["title"],
                "specialty": qualification["fields"]["specialty"],
                "description": qualification["fields"]["desc"],
                "links": {
                    "list": request.build_absolute_uri('/') + "spec/",
                    "self": request.build_absolute_uri()
                }
            })
            
        except ValueError:
            return Response(
                {"error": "ID должен быть числом"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            