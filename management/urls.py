from . import views
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
        path('',  views.home , name='home'),
        path("signin/",views.signin, name="signin"),
        path("signup/", views.signup, name="signup"),
        path("signout/", views.signout, name="logout"),
        path("details-doctors/", views.details_doctors, name="logout"),
        path("doctor-dashboard/", views.doctors_dashboard, name="doctor_dashboard"),
        path("profile/", views.profile, name="profile"),
        path("add-details/", views.add_details, name="add_details"),
        path("edit-details/", views.edit_details, name="edit_details"),
        path('blog/', include('blog.urls')),
        path('update/', views.update ,name='update'),
        path('book-appointment/<int:doctor_id>', views.book_appointment ,name='book_appointment'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)