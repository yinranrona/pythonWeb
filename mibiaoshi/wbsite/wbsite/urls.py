"""wbsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import url
from wbsapp.views.indexView import project, project_delete, project_add, project_modifiedSave, detail, detail_comment
from wbsapp.views.loginView import login, logout
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^project', project, name='project'),
    url(r'^detail/(?P<task_id>\d+)/delete$', project_delete, name='delete'),
    url(r'^add', project_add, name='add'),
    url(r'^modifiedSave', project_modifiedSave, name='modifiedSave'),
    url(r'^detail/(?P<page_num>\d+)$', detail, name='detail'),
    url(r'^detail/(?P<page_num>\d+)/comment$', detail_comment, name='comment'),

    url(r'^login', login, name='login'),
    url(r'^logout', logout, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
