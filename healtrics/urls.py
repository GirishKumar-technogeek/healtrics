from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('accounts/',include('accounts.urls')),
    path('admins/',include('admins.urls')),
    path('hospitals/',include('hospitals.urls')),
    path('blood_banks/',include('blood_banks.urls')),
    path('donors/',include('donors.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)