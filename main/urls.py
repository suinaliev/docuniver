from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Основные URLs
    path('', views.firstPage, name='firstPage'),
    path('home/', views.category_list, name='home'),  # Главная страница с категориями
    path('search/', views.search, name='search'),
    path('test/', views.test_page, name='test_page'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    path('categories/<slug:slug>/', views.category_detail, name='category_detail'),
    path('categories/<slug:slug>/documents/', views.category_documents, name='category_documents'),
    path('documents/category/<slug:category_slug>/', views.documents_by_category, name='documents_by_category'),
    
    # Document URLs
    path('documents/', views.document_list, name='document_list'),
    path('documents/create/', views.document_create, name='document_create'),
    path('documents/<int:pk>/update/', views.document_update, name='document_update'),
    path('documents/<int:pk>/delete/', views.document_delete, name='document_delete'),
    
    # Page URLs
    path('pages/', views.page_list, name='page_list'),
    path('pages/create/', views.page_create, name='page_create'),
    path('pages/<int:pk>/update/', views.page_update, name='page_update'),
    path('pages/<int:pk>/delete/', views.page_delete, name='page_delete'),
    
    # File URLs
    path('pages/<int:page_id>/files/', views.file_list, name='file_list'),
    path('pages/<int:page_id>/files/create/', views.file_create, name='file_create'),
    path('files/<int:pk>/update/', views.file_update, name='file_update'),
    path('files/<int:pk>/delete/', views.file_delete, name='file_delete'),
    
    # Дополнительные URLs
    path('dostijeniya/', views.dostijeniya, name='dostijeniya'),
    path('dostijeniya/create/', views.achievement_create, name='achievement_create'),
    path('dostijeniya/<int:pk>/update/', views.achievement_update, name='achievement_update'),
    path('dostijeniya/<int:pk>/delete/', views.achievement_delete, name='achievement_delete'),
    
    # URLs для программ мобильности
    path('mobilnost/', views.mobilnost, name='mobilnost'),
    path('mobilnost/create/', views.mobility_program_create, name='mobility_program_create'),
    path('mobilnost/<int:pk>/', views.mobility_program_detail, name='mobility_program_detail'),
    path('mobilnost/<int:pk>/update/', views.mobility_program_update, name='mobility_program_update'),
    path('mobilnost/<int:pk>/delete/', views.mobility_program_delete, name='mobility_program_delete'),
    path('mobilnost/<int:program_pk>/media/create/', views.mobility_media_create, name='mobility_media_create'),
    path('mobilnost/media/<int:pk>/delete/', views.mobility_media_delete, name='mobility_media_delete'),
    
    path('registration/', views.registration, name='registration'),
    
    # Общий URL для страниц должен быть последним
    path('<path:path>/', views.page_view, name='page_view'),
]
