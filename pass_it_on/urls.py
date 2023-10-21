"""
URL configuration for pass_it_on project.

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
from django.contrib import admin
from django.urls import path

from pass_it_on_app.views import IndexView, UserLoginView, UserRegisterView, DonationAddView, UserLogoutView, \
    DonationConfirmView, AdminMenuView, UserListView, InstitutionListView, InstitutionUpdateView, InstitutionAddView, \
    UserAddView, UserUpdateView, InstitutionDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name="index"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', UserLogoutView.as_view(), name="logout"),
    path('register/', UserRegisterView.as_view(), name="register"),
    path('donate/', DonationAddView.as_view(), name="donation-add"),
    path('donation-confirmed/', DonationConfirmView.as_view(), name="donation-confirmation"),

    path('admin-menu/', AdminMenuView.as_view(), name="admin-menu"),

    path('users/', UserListView.as_view(), name="user-list"),
    path('user/add/', UserAddView.as_view(), name="user-add"),
    path('user/update/<int:user_id>', UserUpdateView.as_view(), name="user-update"),

    path('institutions/', InstitutionListView.as_view(), name="institution-list"),
    path('institution/add/', InstitutionAddView.as_view(), name="institution-add"),
    path('institution/update/<pk>', InstitutionUpdateView.as_view(), name="institution-update"),
    path('institution/delete/<int:institution_id>', InstitutionDeleteView.as_view(), name="institution-delete"),
]
