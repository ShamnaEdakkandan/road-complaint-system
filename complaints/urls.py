from django.urls import path
from .views import register,login_view,forgot_password,user_dashboard,engineer_dashboard,add_complaint,my_complaints,update_status,logout_view

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('user-dashboard/', user_dashboard, name='user_dashboard'),
    path('engineer-dashboard/', engineer_dashboard, name='engineer_dashboard'),
    path('add-complaint/', add_complaint, name='add_complaint'),
    path('my-complaints/', my_complaints, name='my_complaints'),
    path('update-status/<int:id>/', update_status, name='update_status'),
    path('logout/', logout_view, name='logout'),
]