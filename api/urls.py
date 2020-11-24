from django.urls import path

from api import views

urlpatterns = ([
    path("contactCreate/", views.ContactViewSet.as_view({'post': 'create'})),
    path("contactUpdate/<str:name>&<str:surname>/", views.ContactViewSet.as_view({'put': 'update'})),
    path("contacts/", views.ContactReadOnlyViewSet.as_view({'get': 'list'})),
    path("contactDelete/<str:name>&<str:surname>/", views.ContactViewSet.as_view({'delete': 'destroy'})),
])
