
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('api/', include('api.urls')),
]

admin.site.site_header = "MIT WPU Summit"
admin.site.site_title = "MIT WPU Summit"
admin.site.index_title = "Welcome to MIT WPU Summit Admin Panel"