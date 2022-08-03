
from base.api import urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/', admin.site.urls),
    path('',  include('base.urls'), name='base'),
    path('chat/', include('chat.urls'), name='chat'),
    path('shop/', include('shop.urls'), name='shop'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
