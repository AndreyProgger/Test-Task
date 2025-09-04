from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("auth/", include("accounts.urls")),
    # Этот путь предоставляет доступ к сырой спецификации OpenAPI вашего API в формате JSON
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    #  Этот путь предоставляет доступ к интерактивному интерфейсу Swagger UI
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("profiles/", include("profiles.urls")),
    path("blog/", include("blog.urls")),
    path("blog/v2/", include("blog_v2.urls")),
]
