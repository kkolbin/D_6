from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post, Category, PostCategory
from .templatetags.censor import censor
from django.contrib.auth.models import User


def news_list(request):
    news = Post.objects.order_by('-created_at')  # Сортировка от более свежих к старым по полю created_at
    context = {'news': news}
    return render(request, 'news/news_list.html', context)


def article_detail(request, article_id):
    article = get_object_or_404(Post, pk=article_id)
    context = {'article': article}
    return render(request, 'news/article_detail.html', context)


def create_categories(request):
    categories_data = [
        'Политика',
        'Технологии',
        'Спорт',
    ]

    for name in categories_data:
        Category.objects.get_or_create(name=name)

    return HttpResponse('Категории успешно созданы')


def create_articles(request):
    # Получение автора статей
    author = User.objects.get(username='john_doe')

    # Создание статей
    articles_data = [
        {
            'title': 'ЧТО ТАКОЕ СПОРТ?',
            'content': 'Спорт. Всего одно слово, а как много оно значит! Занятие спортом - определенный вид '
                       'деятельности людей, направленная на достижение заданного результата в физическом развитии '
                       'человека.',
            'rating': 8,  # Установите значение для поля "rating"
            'category': 'Спорт',
        },
        {
            'title': 'Каким станет городской транспорт в будущем',
            'content': 'Наука и технологии развиваются сейчас всё стремительнее. Поэтому совсем скоро у людей будет '
                       'возможность увидеть в некотором смысле совершенно новый транспорт.',
            'rating': 7,  # Установите значение для поля "rating"
            'category': 'Технологии',
        },
        {
            'title': 'Китайцы обожают Швецию. Издалека',
            'content': 'В поисках лучших условий труда и терпимого общества молодые китайцы переезжают в Швецию. '
                       'Благодаря социальным сетям молодежь называет Скандинавию «идеальным вторым домом». Но приехав '
                       'в Швецию, китайцы понимают, что жизнь здесь сложнее, чем кажется в интернете. Некоторых это '
                       'заставляет пересмотреть взгляды не только на Швецию, но и на собственную страну',
            'rating': 6,  # Установите значение для поля "rating"
            'category': 'Политика',
        },
        {
            'title': 'Спортивное питание',
            'content': 'Как правильно питаться во время занятий спортом. Речь в данной статье пойдет не о "спортивном'
                       ' питании", т.е. анаболических препаратах и различных БАДах, информацию о которых можно найти '
                       'на специализированных ресурсах, а именно о том, как правильно питаться обычной пищей во время '
                       'занятия спортом.',
            'rating': 8,  # Установите значение для поля "rating"
            'category': 'Спорт',
        },
        {
            'title': 'Этот чип превратит лампочки в вашем доме в ретранслятор WiFi',
            'content': 'Интеграция этой технологии не за горами Компания pureLiFi планирует принести технологию LiFi '
                       'в дома. Что станет идеальным подспорьем для домашнего Wi-Fi, чтобы наконец-то покрыть ту часть'
                       ' дома, где никогда не было интернета.',
            'rating': 7,  # Установите значение для поля "rating"
            'category': 'Технологии',
        },
        {
            'title': 'Китай+5',
            'content': 'Новый механизм сотрудничества между КНР и странами Центральной Азии будет создан по итогам '
                       'саммита в формате Китай+5, который состоится 18-19 мая в Сиане. Он включает Казахстан, '
                       'Кыргызстан, Туркменистан, Таджикистан, Узбекистан.',
            'rating': 6,  # Установите значение для поля "rating"
            'category': 'Политика',
        },
        {
            'title': 'Детское закаливание',
            'content': 'Закаливание маленьких детей полезно начинать практически с самого рождения. Детское закаливание'
                       ' особенно важно для малышей раннего возраста и ослабленных детей (недоношенных, страдающих '
                       'гипотрофией, рахитом, диатезом или другими аллергическими заболеваниями). Детское закаливание '
                       'основано на свойстве организма постепенно приспосабливаться к необычным условиям.',
            'rating': 8,  # Установите значение для поля "rating"
            'category': 'Спорт',
        },
        {
            'title': 'Что такое «дополненный интеллект»',
            'content': 'Людям необходимо сейчас сделать выбор между двумя вариантами. Первый - это автоматизация '
                       'различных процессов и замена человека роботом, второй - использование технологий для '
                       'усовершенствования способностей человека (дополненный интеллект).',
            'rating': 7,  # Установите значение для поля "rating"
            'category': 'Технологии',
        },
        {
            'title': 'Китай дедолларизует ВЭД',
            'content': 'Китайский юань в марте впервые стал основной валютой обслуживания внешнеэкономической '
                       'деятельности КНР, обогнав доллар. По данным государственного валютного управления КНР, 48,4% '
                       'трансграничных расчетов страны обслуживались в национальной валюте, тогда как на валюту '
                       'американскую пришлось 46,7%.',
            'rating': 6,  # Установите значение для поля "rating"
            'category': 'Политика',
        },
        {
            'title': 'История проведения Олимпийских игр',
            'content': 'Одним из самых ярких и массовых событий планеты являются Олимпийские игры. Любой спортсмен, '
                       'сумевший занять пьедестал на Олимпийских состязаниях, получает статус Олимпийского чемпиона на '
                       'всю жизнь и его достижения остаются в мировой истории спорта на века.',
            'rating': 8,  # Установите значение для поля "rating"
            'category': 'Спорт',
        },
    ]

    for data in articles_data:
        title = data['title']
        content = data['content']
        rating = data['rating']
        category_name = data['category']

        category = Category.objects.get(name=category_name)
        post = Post.objects.create(author=author, title=title, content=content, rating=rating, post_type='article')
        PostCategory.objects.create(post=post, category=category)

    return HttpResponse('Статьи успешно созданы')

