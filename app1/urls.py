from django.contrib import admin
from django.urls import path,include # to include blank path to the app
from app1 import views


urlpatterns = [
    path("",views.home,name="home"),
    path("login",views.all_login,name="login"),
    path("user_register",views.user_register,name="user_register"),
    path("sp_register",views.sp_register,name="sp_register"),
    path("reset_password",views.reset_password,name="reset_password"),
    path("plumber_service",views.pumber_service,name="pumber_service"),
    path("user_page",views.user_page,name="user_page"),
    path("log_out",views.log_out,name="log_out"),
    path("vaction/<str:pk>",views.vaction,name='vaction'),
    path("vconfirm",views.vconfirm,name='vconfirm'),
    path("admin_user_dash",views.admin_user_dash,name="admin_user_dash"),
    path("admin_vendor_delete",views.admin_vendor_delete,name="admin_vendor_delete"),
    path("dashboard",views.dashboard,name="dashboard"),
    path("vendor_delete/<str:pk>",views.vendor_delete,name="vendor_delete"),
    path("service_bookings/<str:pk>",views.service_bookings,name="service_bookings"),
    path("admin_bookings",views.admin_bookings,name="admin_bookings"),
    path("booking_confirm/<str:pk>",views.booking_confirm,name="booking_confirm"),
    path("admin_home",views.admin_home,name="admin_home"),
    path("sp_dash_main",views.sp_dash_main,name="sp_dash_main"),
    path("sp_dash_bookings",views.sp_dash_bookings,name="sp_dash_bookings"),
    path("sp_dash_profile",views.sp_dash_profile,name="sp_dash_profile"),
    path("sp_dash_profile_edit/<str:pk>",views.sp_dash_profile_edit,name="sp_dash_profile_edit"),
    path("elecrision",views.elecrision,name="elecrision"),
    path("user_profile",views.user_profile,name="user_profile"),
    path("user_bookings",views.user_bookings,name="user_bookings"),

    ]