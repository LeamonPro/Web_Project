from django.urls import path
from .views import upload_image, display_image
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('upload/', upload_image, name='upload_image'),
    path('display/<int:my_model_id>/<str:images>/', display_image, name='display_image')
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
 