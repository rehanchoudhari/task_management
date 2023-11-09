"""
URL configuration for main_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from user_app import routers as user_api_router
from task_app import routers as task_api_router
from django.conf.urls.static import static
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from task_app.views import TaskCompletionReport


auth_api_url = [
    path(r'', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    auth_api_url.append(path('verify/', include('rest_framework.urls')))

api_url_patterns = [
    path('auth/', include([*auth_api_url, 
                                path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                                path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                                path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
                           ])),
                           
    path('accounts/', include(user_api_router.router.urls)),
    path('tasks/', include(task_api_router.router.urls)),
    path('dashboard-report/', TaskCompletionReport.as_view(), name='dashBoardReport'),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_url_patterns)),
    path('docs/', include_docs_urls(title='Task Management')),
    path('schema', get_schema_view(title="Task Management", description="API for all Task …", version="1.0.0"), name='openapi-schema'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)