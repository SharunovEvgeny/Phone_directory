from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api import views

urlpatterns = ([
    path("contactCreate/", views.ContactViewSet.as_view({'post': 'create'})),
    path("contacts/", views.ContactReadOnlyViewSet.as_view({'get': 'list'})),
    path("contactDelete/<str:name>&<str:surname>/", views.ContactViewSet.as_view({'delete': 'destroy'})),
])
