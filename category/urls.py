"""category URL Configuration

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

from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.home, name='index'),
    path('create/', views.create, name='create'),
    path('post/', views.check_post, name='post'),
    path('update/<int:pk>', views.Student_update.as_view(), name='update'),
    path('delete/<int:pk>', views.Student_delete.as_view(), name='delete'),
    path('search', views.search, name='search'),
]