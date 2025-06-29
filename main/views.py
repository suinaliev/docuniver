from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Document, Page, File, Teacher, Category, StudentAchievement, MobilityProgram, MobilityMedia
from django.contrib import messages
from .decorators import admin_required, teacher_required
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from .forms import CategoryForm, DocumentForm, PageForm, FileForm, StudentAchievementForm, MobilityProgramForm, MobilityMediaForm

# Document views for teachers (read-only)
@teacher_required
def document_list(request):
    documents = Document.objects.all().order_by('-created_at')
    for doc in documents:
        if doc.document and doc.document.url.endswith(".pdf"):
            doc.icon = "📕"
        elif doc.document and (doc.document.url.endswith(".doc") or doc.document.url.endswith(".docx")):
            doc.icon = "📘"
        elif doc.document and (doc.document.url.endswith(".jpg") or doc.document.url.endswith(".png")):
            doc.icon = "🖼️"
        else:
            doc.icon = "📄"
    return render(request, 'main/document_list.html', {
        'documents': documents,
        'is_admin': request.user.is_staff
    })


@admin_required
def document_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        document = request.FILES.get('document')
        notes = request.POST.get('notes')
        tags = request.POST.get('tags')
        index = request.POST.get('index')
        timestore = request.POST.get('timestore')
        is_important = request.POST.get('is_important') == 'on'
        category_id = request.POST.get('category')
        category = get_object_or_404(Category, id=category_id) if category_id else None
        Document.objects.create(
            name=name, 
            document=document, 
            notes=notes,
            tags=tags,
            index=index,
            timestore=timestore,
            is_important=is_important,
            category=category,
            created_by=request.user
        )
        messages.success(request, 'Документ успешно создан')
        return redirect('category_list')
    categories = Category.objects.filter(is_active=True).order_by('order', 'name')
    return render(request, 'main/document_form.html', {'categories': categories})

@admin_required
def document_update(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        document.name = request.POST.get('name')
        if 'document' in request.FILES:
            document.document = request.FILES['document']
        document.notes = request.POST.get('notes')
        document.tags = request.POST.get('tags')
        document.index = request.POST.get('index')
        document.timestore = request.POST.get('timestore')
        document.is_important = request.POST.get('is_important') == 'on'
        category_id = request.POST.get('category')
        document.category = get_object_or_404(Category, id=category_id) if category_id else None
        document.save()
        messages.success(request, 'Документ успешно обновлен')
        return redirect('category_list')
    categories = Category.objects.filter(is_active=True).order_by('order', 'name')
    return render(request, 'main/document_form.html', {'document': document, 'categories': categories})

@admin_required
def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Документ успешно удален')
        return redirect('document_list')
    return render(request, 'main/document_confirm_delete.html', {'document': document})

# Page views for teachers (read-only)
@teacher_required
def page_list(request):
    pages = Page.objects.filter(parent=None)
    return render(request, 'main/page_list.html', {
        'pages': pages,
        'is_admin': request.user.is_staff
    })

# Page CRUD operations for admin
@admin_required
def page_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        content = request.POST.get('content')
        parent_id = request.POST.get('parent')
        parent = None if not parent_id else get_object_or_404(Page, id=parent_id)
        Page.objects.create(title=title, slug=slug, content=content, parent=parent)
        messages.success(request, 'Страница успешно создана')
        return redirect('page_list')
    pages = Page.objects.all()
    return render(request, 'main/page_form.html', {'pages': pages})

@admin_required
def page_update(request, pk):
    page = get_object_or_404(Page, pk=pk)
    if request.method == 'POST':
        page.title = request.POST.get('title')
        page.slug = request.POST.get('slug')
        page.content = request.POST.get('content')
        parent_id = request.POST.get('parent')
        page.parent = None if not parent_id else get_object_or_404(Page, id=parent_id)
        page.save()
        messages.success(request, 'Страница успешно обновлена')
        return redirect('page_list')
    pages = Page.objects.exclude(id=pk)
    return render(request, 'main/page_form.html', {'page': page, 'pages': pages})

@admin_required
def page_delete(request, pk):
    page = get_object_or_404(Page, pk=pk)
    if request.method == 'POST':
        page.delete()
        messages.success(request, 'Страница успешно удалена')
        return redirect('page_list')
    return render(request, 'main/page_confirm_delete.html', {'page': page})

# File views for teachers (read-only)
@teacher_required
def file_list(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    files = File.objects.filter(page=page)
    return render(request, 'main/file_list.html', {
        'files': files,
        'page': page,
        'is_admin': request.user.is_staff
    })

# File CRUD operations for admin
@admin_required
def file_create(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES.get('file')
        show_like_sub_document = request.POST.get('show_like_sub_document') == 'on'
        File.objects.create(
            page=page,
            title=title,
            file=file,
            show_like_sub_document=show_like_sub_document
        )
        messages.success(request, 'Файл успешно добавлен')
        return redirect('file_list', page_id=page_id)
    return render(request, 'main/file_form.html', {'page': page})

@admin_required
def file_update(request, pk):
    file = get_object_or_404(File, pk=pk)
    if request.method == 'POST':
        file.title = request.POST.get('title')
        if 'file' in request.FILES:
            file.file = request.FILES['file']
        file.show_like_sub_document = request.POST.get('show_like_sub_document') == 'on'
        file.save()
        messages.success(request, 'Файл успешно обновлен')
        return redirect('file_list', page_id=file.page.id)
    return render(request, 'main/file_form.html', {'file': file})

@admin_required
def file_delete(request, pk):
    file = get_object_or_404(File, pk=pk)
    page_id = file.page.id
    if request.method == 'POST':
        file.delete()
        messages.success(request, 'Файл успешно удален')
        return redirect('file_list', page_id=page_id)
    return render(request, 'main/file_confirm_delete.html', {'file': file})

# Public views
def firstPage(request):
    # Если пользователь аутентифицирован, перенаправляем на список категорий
    if request.user.is_authenticated:
        return redirect('category_list')
    return render(request, 'firstPage.html')

def test_page(request):
    """Тестовая страница для отладки"""
    try:
        root_category = Category.objects.get(parent=None, is_active=True)
        categories = root_category.children.filter(is_active=True)
    except Category.DoesNotExist:
        categories = Category.objects.filter(parent=None, is_active=True)
    
    return render(request, 'main/test_page.html', {
        'categories': categories,
        'is_admin': request.user.is_staff if request.user.is_authenticated else False
    })

def dostijeniya(request):
    achievements = StudentAchievement.objects.all().order_by('student_name', '-date_received')
    # Group achievements by student
    students_achievements = {}
    for achievement in achievements:
        if achievement.student_name not in students_achievements:
            students_achievements[achievement.student_name] = {
                'name': achievement.student_name,
                'group': achievement.group,
                'photo': achievement.photo,
                'achievements': [],
                'last_updated': achievement.updated_at,
                'has_important': False
            }
        students_achievements[achievement.student_name]['achievements'].append(achievement)
        if achievement.is_important:
            students_achievements[achievement.student_name]['has_important'] = True
        if achievement.updated_at > students_achievements[achievement.student_name]['last_updated']:
            students_achievements[achievement.student_name]['last_updated'] = achievement.updated_at

    context = {
        'students_achievements': students_achievements.values(),
        'is_admin': request.user.is_staff
    }
    return render(request, 'dostijeniya.html', context)

def mobilnost(request):
    programs = MobilityProgram.objects.filter(is_active=True).order_by('-start_date')
    context = {
        'programs': programs,
        'is_admin': request.user.is_staff
    }
    return render(request, 'mobilnost.html', context)

@teacher_required
def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        department = request.POST.get('department')
        position = request.POST.get('position')

        if password1 != password2:
            messages.error(request, 'Пароли не совпадают')
            return redirect('registration')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return redirect('registration')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует')
            return redirect('registration')

        try:
            with transaction.atomic():
                # Создаем пользователя
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Создаем профиль учителя
                Teacher.objects.create(
                    user=user,
                    department=department,
                    position=position
                )
                
                messages.success(request, 'Регистрация успешно завершена. Теперь вы можете войти в систему.')
                return redirect('login')
                
        except Exception as e:
            messages.error(request, 'Произошла ошибка при регистрации. Попробуйте позже.')
            return redirect('registration')

    return render(request, 'registration/registration.html')

@teacher_required
def page_view(request, path):
    slug_list = path.strip('/').split('/')
    page = None
    for slug in slug_list:
        page = get_object_or_404(Page, slug=slug, parent=page)

    files = page.documents.all()
    return render(request, 'page_item.html', {
        'page': page,
        'files': files,
        'is_admin': request.user.is_staff
    })

@teacher_required
def search(request):
    query = request.GET.get('q', '')
    results = {
        'documents': [],
        'pages': [],
        'files': [],
        'categories': []
    }
    
    if query:
        # Поиск по документам
        results['documents'] = Document.objects.filter(
            Q(name__icontains=query) |
            Q(notes__icontains=query) |
            Q(tags__icontains=query)
        ).order_by('-created_at')

        # Поиск по страницам
        results['pages'] = Page.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).order_by('-created_at')

        # Поиск по файлам
        results['files'] = File.objects.filter(
            Q(title__icontains=query) |
            Q(page__title__icontains=query)
        ).order_by('-created_at')

        # Поиск по категориям
        results['categories'] = Category.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query),
            is_active=True
        ).order_by('order', 'name')

    return render(request, 'main/search_results.html', {
        'query': query,
        'results': results,
        'is_admin': request.user.is_staff
    })

# Category views
@teacher_required
def category_list(request):
  
    try:

        root_category = Category.objects.get(parent=None, is_active=True)
       
        categories = root_category.children.filter(is_active=True).order_by('order', 'name')
    except Category.DoesNotExist:
 
        categories = Category.objects.filter(parent=None, is_active=True).order_by('order', 'name')
    
    return render(request, 'main/category_list.html', {
        'categories': categories,
        'is_admin': request.user.is_staff
    })

@teacher_required
def category_detail(request, slug):

    category = get_object_or_404(Category, slug=slug, is_active=True)
    subcategories = category.children.filter(is_active=True).order_by('order', 'name')
    documents = category.documents.all().order_by('-created_at')
    
    for doc in documents:
        file_info = doc.get_file_type()
        doc.icon = file_info['icon']
        doc.file_type = file_info['type']
    
    # Хлебные крошки
    breadcrumbs = []
    current = category
    while current:
        breadcrumbs.insert(0, current)
        current = current.parent
    
    return render(request, 'main/category_detail.html', {
        'category': category,
        'subcategories': subcategories,
        'documents': documents,
        'breadcrumbs': breadcrumbs,
        'is_admin': request.user.is_staff
    })

@teacher_required
def category_documents(request, slug):

    category = get_object_or_404(Category, slug=slug, is_active=True)
    

    def get_category_documents(cat):
        docs = list(cat.documents.all())
        for child in cat.children.filter(is_active=True):
            docs.extend(get_category_documents(child))
        return docs
    
    documents = get_category_documents(category)
    documents.sort(key=lambda x: x.created_at, reverse=True)
    

    for doc in documents:
        file_info = doc.get_file_type()
        doc.icon = file_info['icon']
        doc.file_type = file_info['type']
    
    # Хлебные крошки
    breadcrumbs = []
    current = category
    while current:
        breadcrumbs.insert(0, current)
        current = current.parent
    
    return render(request, 'main/category_documents.html', {
        'category': category,
        'documents': documents,
        'breadcrumbs': breadcrumbs,
        'is_admin': request.user.is_staff
    })


@teacher_required
def documents_by_category(request, category_slug=None):
    """Документы по категориям в плиточном виде"""
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        documents = category.documents.all().order_by('-created_at')
        subcategories = category.children.filter(is_active=True).order_by('order', 'name')
        
        # Хлебные крошки
        breadcrumbs = []
        current = category
        while current:
            breadcrumbs.insert(0, current)
            current = current.parent
    else:
        category = None
        documents = Document.objects.filter(category__isnull=True).order_by('-created_at')
        subcategories = Category.objects.filter(parent=None, is_active=True).order_by('order', 'name')
        breadcrumbs = []
    
    # Добавляем иконки для документов
    for doc in documents:
        file_info = doc.get_file_type()
        doc.icon = file_info['icon']
        doc.file_type = file_info['type']
    
    return render(request, 'main/documents_by_category.html', {
        'category': category,
        'documents': documents,
        'subcategories': subcategories,
        'breadcrumbs': breadcrumbs,
        'is_admin': request.user.is_staff
    })

# Category CRUD operations for admin
@admin_required
def category_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        parent_id = request.POST.get('parent')
        icon = request.POST.get('icon')
        color = request.POST.get('color')
        order = request.POST.get('order', 0)
        
        parent = None
        if parent_id:
            parent = get_object_or_404(Category, id=parent_id)
        
        Category.objects.create(
            name=name,
            slug=slug,
            description=description,
            parent=parent,
            icon=icon or 'fas fa-folder',
            color=color or '#667eea',
            order=int(order) if order else 0
        )
        messages.success(request, 'Категория успешно создана')
        return redirect('category_list')
    

    categories = Category.objects.filter(is_active=True).order_by('order', 'name')
    return render(request, 'main/category_form.html', {'categories': categories})

@admin_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.slug = request.POST.get('slug')
        category.description = request.POST.get('description')
        parent_id = request.POST.get('parent')
        category.parent = get_object_or_404(Category, id=parent_id) if parent_id else None
        category.icon = request.POST.get('icon') or 'fas fa-folder'
        category.color = request.POST.get('color') or '#667eea'
        category.order = int(request.POST.get('order', 0)) if request.POST.get('order') else 0
        category.is_active = request.POST.get('is_active') == 'on'
        category.save()
        messages.success(request, 'Категория успешно обновлена')
        return redirect('category_list')
    
    categories = Category.objects.filter(is_active=True).exclude(id=category.id).order_by('order', 'name')
    return render(request, 'main/category_form.html', {'category': category, 'categories': categories})

@admin_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Категория успешно удалена')
        return redirect('category_list')
    return render(request, 'main/category_confirm_delete.html', {'category': category})

@admin_required
def achievement_create(request):
    if request.method == 'POST':
        form = StudentAchievementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Достижение успешно добавлено')
            return redirect('dostijeniya')
    else:
        form = StudentAchievementForm()
    
    return render(request, 'main/achievement_form.html', {
        'form': form,
        'title': 'Добавление достижения'
    })

@admin_required
def achievement_update(request, pk):
    achievement = get_object_or_404(StudentAchievement, pk=pk)
    
    if request.method == 'POST':
        form = StudentAchievementForm(request.POST, request.FILES, instance=achievement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Достижение успешно обновлено')
            return redirect('dostijeniya')
    else:
        form = StudentAchievementForm(instance=achievement)
    
    return render(request, 'main/achievement_form.html', {
        'form': form,
        'title': 'Редактирование достижения'
    })

@admin_required
def achievement_delete(request, pk):
    achievement = get_object_or_404(StudentAchievement, pk=pk)
    
    if request.method == 'POST':
        achievement.delete()
        messages.success(request, 'Достижение успешно удалено')
        return redirect('dostijeniya')
    
    return render(request, 'main/achievement_confirm_delete.html', {
        'achievement': achievement
    })

@admin_required
def mobility_program_create(request):
    if request.method == 'POST':
        form = MobilityProgramForm(request.POST)
        if form.is_valid():
            program = form.save()
            messages.success(request, 'Программа мобильности успешно создана')
            return redirect('mobility_program_detail', pk=program.pk)
    else:
        form = MobilityProgramForm()
    
    return render(request, 'main/mobility_program_form.html', {
        'form': form,
        'title': 'Добавление программы мобильности'
    })

@admin_required
def mobility_program_update(request, pk):
    program = get_object_or_404(MobilityProgram, pk=pk)
    
    if request.method == 'POST':
        form = MobilityProgramForm(request.POST, instance=program)
        if form.is_valid():
            program = form.save()
            messages.success(request, 'Программа мобильности успешно обновлена')
            return redirect('mobility_program_detail', pk=program.pk)
    else:
        form = MobilityProgramForm(instance=program)
    
    return render(request, 'main/mobility_program_form.html', {
        'form': form,
        'title': 'Редактирование программы мобильности'
    })

@admin_required
def mobility_program_delete(request, pk):
    program = get_object_or_404(MobilityProgram, pk=pk)
    
    if request.method == 'POST':
        program.delete()
        messages.success(request, 'Программа мобильности успешно удалена')
        return redirect('mobilnost')
    
    return render(request, 'main/mobility_program_confirm_delete.html', {
        'program': program
    })

def mobility_program_detail(request, pk):
    program = get_object_or_404(MobilityProgram, pk=pk)
    media = program.media.all().order_by('order', '-created_at')
    
    context = {
        'program': program,
        'media': media,
        'is_admin': request.user.is_staff
    }
    return render(request, 'main/mobility_program_detail.html', context)

@admin_required
def mobility_media_create(request, program_pk):
    program = get_object_or_404(MobilityProgram, pk=program_pk)
    
    if request.method == 'POST':
        form = MobilityMediaForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.program = program
            media.save()
            messages.success(request, 'Медиафайл успешно добавлен')
            return redirect('mobility_program_detail', pk=program.pk)
    else:
        form = MobilityMediaForm()
    
    return render(request, 'main/mobility_media_form.html', {
        'form': form,
        'program': program,
        'title': 'Добавление медиафайла'
    })

@admin_required
def mobility_media_delete(request, pk):
    media = get_object_or_404(MobilityMedia, pk=pk)
    program_pk = media.program.pk
    
    if request.method == 'POST':
        media.delete()
        messages.success(request, 'Медиафайл успешно удален')
        return redirect('mobility_program_detail', pk=program_pk)
    
    return render(request, 'main/mobility_media_confirm_delete.html', {
        'media': media
    })

