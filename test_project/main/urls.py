from django.urls import path
from .views import index, show_all_entries


urlpatterns = [
    path('', index, name='index'),
    path('entries/', show_all_entries, name='entries'),

]
