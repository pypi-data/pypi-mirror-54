from django.urls import include, path


urlpatterns = [
    path('', include('wagtail_resume.urls', namespace='wagtail_resume')),
]
