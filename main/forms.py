from django import forms
from .models import Category, Document, Page, File, StudentAchievement, MobilityProgram, MobilityMedia

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent', 'slug', 'icon', 'color']

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'document', 'category', 'notes', 'index', 'timestore']

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'content', 'parent']

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['title', 'file', 'page', 'show_like_sub_document']

class StudentAchievementForm(forms.ModelForm):
    class Meta:
        model = StudentAchievement
        fields = ['student_name', 'group', 'photo', 'achievement_type', 'title', 
                 'description', 'date_received', 'is_important', 'document']
        widgets = {
            'date_received': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class MobilityProgramForm(forms.ModelForm):
    class Meta:
        model = MobilityProgram
        fields = ['title', 'program_type', 'university', 'country', 'description', 
                 'requirements', 'duration', 'start_date', 'end_date', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
        }

class MobilityMediaForm(forms.ModelForm):
    class Meta:
        model = MobilityMedia
        fields = ['media_type', 'title', 'description', 'file', 'video_url', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        media_type = cleaned_data.get('media_type')
        file = cleaned_data.get('file')
        video_url = cleaned_data.get('video_url')

        if media_type == 'photo' and not file:
            raise forms.ValidationError('Для фотографии необходимо загрузить файл')
        elif media_type == 'video' and not video_url and not file:
            raise forms.ValidationError('Для видео необходимо указать ссылку или загрузить файл')

        return cleaned_data 