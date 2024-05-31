from .views import IndexView, BaseRegisterView, upgrade_me, AppointmentView, AppointmentSuccessView, CategoryListView, \
    subscribe, unsubscribe, CategorySearch
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import NewsList, NewsDetail, NewsSearch, PostCreate, PostUpdate, PostDelete, ArticlesUpdate, ArticlesDelete, ArticlesCreate

app_name = 'appointments'

urlpatterns = [
    path('news/', NewsList.as_view(), name='post_list'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='post_detail'),
    path('news/search/', NewsSearch.as_view(), name='post_search'),
    path('news/create/', PostCreate.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', ArticlesUpdate.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name='sign/signup.html'), name='signup'),
    path('sign/upgrade/', upgrade_me, name='upgrade'),
    path('appointments/make_appointment/', AppointmentView.as_view(), name='make_appointment'),
    path('appointments/appointment_success/', AppointmentSuccessView.as_view(), name='appointment_success'),
    path('categories/<int:pk>', CategorySearch.as_view(), name='category_search'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
    # path('categories/<int:pk>', CategoryListView.as_view(), name='category_list')
]
