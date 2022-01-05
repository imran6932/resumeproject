from django.urls import path 
from api import views
from .views import ResumeAPI
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    #path('',views.index,name="index"),
    #path('result',views.result,name="result"),
    path('api',ResumeAPI.as_view(),name="ResumeAPI"),
   
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)