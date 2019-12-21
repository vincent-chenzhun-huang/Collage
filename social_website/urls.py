"""social_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Include all the url patterns in different parts of the website
urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('images/', include('images.urls', namespace='images')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
Django will serve these static files only debug mode. Update after 1.6

What is serving a static file: from stackoverflow
It means that the file content will be sent to the client (usually a browser) as 
is without server intervention. By contrast, a dynamic file is parsed by the server which then renders a new set of 
data based on the dynamic file template. A dynamic file will typically use some form of server-side code to let the 
server know what type of modifications need to be made. 
"""
