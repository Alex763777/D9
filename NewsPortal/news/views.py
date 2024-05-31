import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from django.core.mail import send_mail, EmailMultiAlternatives, mail_admins
from .forms import PostForm, ArticlesForm
from .models import Post, BaseRegisterForm, Appointment, Category
from .filters import PostFilter

from django import forms


class AppointmentForm(forms.ModelForm):  # Форма для создания записи подписки
    class Meta:
        model = Appointment
        fields = ['client_name', 'date']


class NewsList(LoginRequiredMixin, ListView):
    model = Post  # Указываем модель, объекты которой мы будем выводить
    template_name = 'post_list.html'  # имя шаблона, все инструкции, как показаны наши объекты
    context_object_name = 'posts'  # имя списка, все объекты. Его надо указать, чтобы обратиться в html-шаблоне.
    ordering = '-date_in'
    paginate_by = 10  # количество записей на странице

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['is_not_premium'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class NewsDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    paginate_by = 10  # количество записей на странице


class NewsSearch(LoginRequiredMixin, ListView):
    model = Post  # Указываем модель, объекты которой мы будем выводить
    template_name = 'post_search.html'  # имя шаблона, все инструкции, как показаны наши объекты
    context_object_name = 'posts'  # Имя списка, все объекты. Его надо указать, чтобы обратиться в html-шаблоне.
    ordering = '-date_in'
    paginate_by = 10  # количество записей на странице

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    permission_required = ('news.add_post',)
    template_name = 'post_create.html'


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    permission_required = ('news.change_post',)
    template_name = 'post_edit.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class ArticlesCreate(LoginRequiredMixin, CreateView):
    form_class = ArticlesForm
    model = Post
    permission_required = ('news.add_articles',)
    template_name = 'articles_create.html'


class ArticlesUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = ArticlesForm
    model = Post
    permission_required = ('news.change_articles',)
    template_name = 'articles_edit.html'


class ArticlesDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('post_list')


class BaseRegisterView(CreateView):  # Класс представления для регистрации пользователей
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class IndexView(LoginRequiredMixin, TemplateView):  # Класс представления для главной страницы
    template_name = 'default.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_premium'] = not self.request.user.groups.filter(name='premium').exists()


class AddNewsPortal(PermissionRequiredMixin, CreateView):  # Класс представления для добавления новостей и статей
    model = Post
    form_class = PostForm
    permission_required = ('news.add_custom_post', 'news.change_custom_post', 'news.add_custom_articles',
                           'news.change_custom_articles',)
    template_name = 'post_create.html', 'articles_create.html', 'post_edit.html', 'articles_edit.html'
    success_url = reverse_lazy('post_list')


@login_required
def upgrade_me(request):  # Функция для обновления прав пользователя до группы "authors"
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    else:
        pass
    return redirect('/news/')

class CategoryListView(NewsList):  # подписка на категорию новостей
    model = Post
    template_name = 'news/category_search.html'  # на шаблон сос списком новостей
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})  # на шаблон успешной подписки

def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно отписались от рассылки новостей категории'
    return render(request, 'unsubscribe.html', {'category': category, 'message': message})  # на шаблон  отписки

def category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы выбрали категорию:  '
    return render(request, 'category_search.html', {'category': category, 'message': message})  # на шаблон успешной подписки


class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        client_name = request.POST.get('client_name')
        if client_name:
            appointment = Appointment(client_name=client_name, message=request.POST.get('message'))
            appointment.save()

            html_content = render_to_string(  # получаем наш html
                'appointment_created.html',
                {
                    'appointment': appointment,
                }
            )

            mail_admins(  # письмо админу
                subject=f'Подписка на новости: {appointment.client_name}',
                message=f'Пользователь {appointment.client_name} выполнил подписку.',
            )

            msg = EmailMultiAlternatives(
                subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',  # имя и дата записи
                body=appointment.message,  # сообщение с кратким описанием
                from_email=os.environ.get('from_email'),  # почта, с которой отправляется
                to=['alex1977.aka@gmail.com']  # список получателей
            )
            msg.attach_alternative(html_content, "text/html")  # добавляем html

            msg.send()

            return redirect('appointments:appointment_success')
        else:
            return redirect('appointments:make_appointment')


class AppointmentSuccessView(View):
    def get(self, request):
        return render(request, 'appointment_success.html')

class CategorySearch(LoginRequiredMixin, ListView):
    model = Post  # Указываем модель, объекты которой мы будем выводить
    template_name = 'category_search.html'  # имя шаблона, все инструкции, как показаны наши объекты
    context_object_name = 'posts'  # Имя списка, все объекты. Его надо указать, чтобы обратиться в html-шаблоне.
    ordering = '-date_in'
    # paginate_by = 10  # количество записей на странице