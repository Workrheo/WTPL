from django.contrib import admin
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('oldadmin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name="crmHome"), name='admin_redirect'),
    path('admin/', RedirectView.as_view(pattern_name="crmHome"), name='admin_redirect'),
    path('crm/', RedirectView.as_view(pattern_name="crmHome"), name='admin_redirect'),
    path('dashboard/', RedirectView.as_view(pattern_name="userDashboard"), name='user_redirect'),
    path('user/', RedirectView.as_view(pattern_name="userDashboard"), name='user_redirect'),
    path('', include('adminapp.urls')),
    path('', include('userapp.urls')),
    path('', include('authapp.urls')),
    path('', include('legals.urls')),
    path('', include('crm.urls')),
    path('', include('reports.urls')),
    path('', include('marketing.urls')),
    path('', include('order.urls')),
    path('', include('ai.urls')),
    
]

handler404 = 'authapp.views.error_404'
handler404 = 'adminapp.views.error_404'
handler404 = 'crm.views.error_404'
handler404 = 'userapp.views.error_404'
handler404 = 'settings.views.error_404'
handler404 = 'legals.views.error_404'
handler404 = 'reports.views.error_404'
handler404 = 'marketing.views.error_404'
handler404 = 'order.views.error_404'
handler404 = 'ai.views.error_404'

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   