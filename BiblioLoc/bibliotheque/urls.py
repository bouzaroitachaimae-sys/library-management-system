from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from livres import views as livres_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('livres.urls')),
     path('accounts/register/', livres_views.register, name='register'),
    path('reservations/', include('reservations.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
