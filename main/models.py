from django.db import models
from django.db.models import TextField
from django.contrib.auth.models import User
from django.utils import timezone


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название категории")
    slug = models.SlugField(unique=True, verbose_name="Слаг")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE, verbose_name="Родительская категория")
    icon = models.CharField(max_length=50, default='fas fa-folder', verbose_name="Иконка")
    color = models.CharField(max_length=7, default='#667eea', verbose_name="Цвет")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} → {self.name}"
        return self.name

    def get_absolute_url(self):
        if self.parent:
            return f"/categories/{self.parent.slug}/{self.slug}/"
        return f"/categories/{self.slug}/"

    def get_level(self):
        level = 0
        parent = self.parent
        while parent:
            level += 1
            parent = parent.parent
        return level

    def get_children_count(self):
        return self.children.filter(is_active=True).count()

    def get_documents_count(self):
        count = self.documents.count()
        for child in self.children.filter(is_active=True):
            count += child.get_documents_count()
        return count

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['order', 'name']


class Document(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    document = models.FileField(upload_to='documents/', null=True, blank=True, verbose_name="Файл")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='documents', verbose_name="Категория", null=True, blank=True)
    index = models.CharField(max_length=20, null=True, blank=True, verbose_name="Индекс")
    timestore = models.CharField(max_length=20, null=True, blank=True, verbose_name="Срок хранения")
    notes = models.TextField(null=True, blank=True, verbose_name="Примечания")
    tags = models.CharField(max_length=500, blank=True, null=True, verbose_name="Теги (через запятую)")
    is_important = models.BooleanField(default=False, verbose_name="Важный документ")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Создал")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_file_type(self):
        if self.document:
            ext = self.document.name.split('.')[-1].lower()
            if ext == 'pdf':
                return {'icon': '📕', 'type': 'PDF'}
            elif ext in ['doc', 'docx']:
                return {'icon': '📘', 'type': 'Word'}
            elif ext in ['xls', 'xlsx']:
                return {'icon': '📗', 'type': 'Excel'}
            elif ext in ['ppt', 'pptx']:
                return {'icon': '📙', 'type': 'PowerPoint'}
            elif ext in ['jpg', 'jpeg', 'png', 'gif']:
                return {'icon': '🖼️', 'type': 'Изображение'}
            elif ext in ['zip', 'rar', '7z']:
                return {'icon': '📦', 'type': 'Архив'}
            else:
                return {'icon': '📄', 'type': 'Документ'}
        return {'icon': '📄', 'type': 'Без файла'}

    def get_tags_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        ordering = ['-created_at']


class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = TextField(blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    show_like_document = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.parent:
            return f"{self.parent.get_absolute_url()}/{self.slug}"
        return f"/{self.slug}"

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
        ordering = ['title']


class File(models.Model):
    page = models.ForeignKey(Page, related_name='documents', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/',  blank=True, null=True)
    show_like_sub_document = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"
        ordering = ['-created_at']


class StudentAchievement(models.Model):
    ACHIEVEMENT_TYPES = [
        ('olympiad', 'Олимпиада'),
        ('certificate', 'Сертификат'),
        ('award', 'Награда'),
        ('other', 'Другое'),
    ]

    student_name = models.CharField(max_length=255, verbose_name='ФИО студента')
    group = models.CharField(max_length=50, verbose_name='Группа')
    photo = models.ImageField(upload_to='achievements/photos/', blank=True, null=True, verbose_name='Фото студента')
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPES, verbose_name='Тип достижения')
    title = models.CharField(max_length=255, verbose_name='Название достижения')
    description = models.TextField(blank=True, verbose_name='Описание')
    date_received = models.DateField(verbose_name='Дата получения')
    is_important = models.BooleanField(default=False, verbose_name='Важное достижение')
    document = models.FileField(upload_to='achievements/documents/', blank=True, null=True, verbose_name='Подтверждающий документ')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Достижение студента'
        verbose_name_plural = 'Достижения студентов'
        ordering = ['-date_received']

    def __str__(self):
        return f"{self.student_name} - {self.title}"


class MobilityProgram(models.Model):
    PROGRAM_TYPES = [
        ('exchange', 'Программа обмена'),
        ('internship', 'Стажировка'),
        ('practice', 'Практика'),
        ('other', 'Другое'),
    ]

    title = models.CharField(max_length=255, verbose_name='Название программы')
    program_type = models.CharField(max_length=20, choices=PROGRAM_TYPES, verbose_name='Тип программы')
    university = models.CharField(max_length=255, verbose_name='Университет/Организация')
    country = models.CharField(max_length=100, verbose_name='Страна')
    description = models.TextField(verbose_name='Описание программы')
    requirements = models.TextField(verbose_name='Требования к участникам')
    duration = models.CharField(max_length=100, verbose_name='Продолжительность')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    is_active = models.BooleanField(default=True, verbose_name='Активная программа')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.university} ({self.country})"

    class Meta:
        verbose_name = 'Программа мобильности'
        verbose_name_plural = 'Программы мобильности'
        ordering = ['-start_date']


class MobilityMedia(models.Model):
    MEDIA_TYPES = [
        ('photo', 'Фотография'),
        ('video', 'Видео'),
    ]

    program = models.ForeignKey(MobilityProgram, on_delete=models.CASCADE, related_name='media', verbose_name='Программа')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, verbose_name='Тип медиа')
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    file = models.FileField(upload_to='mobility/media/', verbose_name='Файл')
    video_url = models.URLField(blank=True, verbose_name='Ссылка на видео (YouTube, Vimeo)')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_media_type_display()} - {self.title}"

    class Meta:
        verbose_name = 'Медиа мобильности'
        verbose_name_plural = 'Медиа мобильности'
        ordering = ['order', '-created_at']