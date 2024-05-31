from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    class Meta:  # В Meta классе мы должны указать Django модель, в которой будем фильтровать записи.
        model = Post
        fields = [  # В fields мы описываем по каким полям модели будет производиться фильтрация.
            'title',
            'author',
            'date_in',
            'category'
        ]


class ArticlesFilter(FilterSet):
    class Meta:  # В Meta классе мы должны указать Django модель, в которой будем фильтровать записи.
        model = Post
        fields = [  # В fields мы описываем по каким полям модели будет производиться фильтрация.
            'title',
            'author',
            'date_in',
            'category'
        ]
