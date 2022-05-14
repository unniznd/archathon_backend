from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from coins import views as coin_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/',coin_views.Login.as_view(), name="login"),
    path('register/',coin_views.Register.as_view(), name="register"),

    path('profile/',coin_views.ProfileView.as_view(), name="profile"),

    path('price/',coin_views.MarketLiveView.as_view(), name="market-live"),
    path('price/<str:id>/',coin_views.MarketLiveView.as_view(), name="market-live-id"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
