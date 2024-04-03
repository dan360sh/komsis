from django.urls import path

from .views import CategoryView, PostView

urlpatterns = [
    path('category/<slug>/', CategoryView.as_view(),
         name='category'),
    path('<category_slug>/<slug>/', PostView.as_view(),
         name='post'),
]
