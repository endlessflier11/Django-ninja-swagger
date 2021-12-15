"""character_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from character_api.role_api import role_router
from character_api.character_api import character_router
from ninja import NinjaAPI
from django.core.exceptions import ObjectDoesNotExist


api = NinjaAPI(csrf=True)
api.add_router('/role', role_router)
# Router for the character API
api.add_router('/character', character_router)


@api.exception_handler(ObjectDoesNotExist)
def entity_request_missing(request, exc):
    message = ", ".join([f"{k}={v}" for k, v in request.resolver_match.kwargs.items()])
    return api.create_response(
        request,
        {"message": f"Error: Query for {message} not found."},
        status=404,
    )


urlpatterns = [
    path('api/', api.urls),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls'))
]
