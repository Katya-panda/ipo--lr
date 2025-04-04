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
from pathlib import Path
from django.conf import settings
import json
import logging
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class QualificationViewSet(ViewSet):
    def get_data_path(self):
        """Определяем путь к файлу данных"""
        return Path(settings.BASE_DIR).parent / 'dump.json'  # Файл в корне репозитория

    def _load_data(self):
        """Загрузка данных из JSON файла"""
        file_path = self.get_data_path()
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            logger.error(f"Файл не найден: {file_path}")
            raise Exception(f"Файл данных не найден по пути: {file_path}")
        except json.JSONDecodeError:
            logger.error("Ошибка чтения JSON файла")
            raise Exception("Файл содержит некорректные JSON данные")

    def list(self, request):
        """GET /spec/ - список всех квалификаций"""
        try:
            data = self._load_data()
            
            qualifications = [
                {
                    "id": item["pk"],
                    "title": item["fields"]["title"],
                    "code": item["fields"]["code"],
                    "link": urljoin(request.build_absolute_uri('/'), f"spec/{item['pk']}/")
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
            data = self._load_data()
            
            qualification = next(
                (item for item in data 
                 if item.get("model") == "data.skill" and str(item["pk"]) == str(pk)),
                None
            )
            
            if not qualification:
                available_ids = [item["pk"] for item in data if item.get("model") == "data.skill"]
                return Response(
                    {
                        "error": f"Квалификация с ID {pk} не найдена",
                        "available_ids": available_ids
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            
            return Response({
                "id": qualification["pk"],
                "code": qualification["fields"]["code"],
                "title": qualification["fields"]["title"],
                "specialty": qualification["fields"].get("specialty"),
                "description": qualification["fields"].get("desc"),
                "links": {
                    "list": urljoin(request.build_absolute_uri('/'), "spec/"),
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