from django.urls import path
from api import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('categories/', views.categories),
    path('shares/', views.ShareView.as_view()),

    path('categories/<int:id>/shares/', views.shares_by_category),
    path('companies/<int:id>/shares/', views.shares_by_company),
    path('order/', views.order_share),

    path('categories/<int:id>/', views.category),
    path('shares/<int:id>/', views.ShareDetailedView.as_view()),
    
    path('order/<int:id>/', views.OrderInfo.as_view()),
    path('orders/completed/', views.orders_completed),
    path('orders/declined/', views.orders_declined),
    path('orders/in_progress/', views.orders_in_progress),
    
    path('brokers/', views.broker_list),
    path('brokers/need_to_fire/', views.broker_to_fire_list),
    path('brokers/<int:id>/', views.broker_detailed),

    path('login/', obtain_jwt_token),
    path('file_upload/', views.simple_upload),
]