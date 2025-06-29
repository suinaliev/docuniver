from django.core.management.base import BaseCommand
from main.models import Category


class Command(BaseCommand):
    help = 'Создает структуру категорий документов'

    def handle(self, *args, **options):
        # Очищаем существующие категории
        Category.objects.all().delete()

        # Создаем основные категории
        categories_data = [
            {
                'name': 'Номенклатурные документы',
                'slug': 'nomenclature-documents',
                'icon': 'fas fa-file-alt',
                'color': '#667eea',
                'children': [
                    {
                        'name': 'Приказы и положения',
                        'slug': 'orders-and-regulations',
                        'icon': 'fas fa-gavel',
                        'color': '#4facfe',
                        'children': [
                            {
                                'name': 'Приказы МОН и Р',
                                'slug': 'orders-mon-r',
                                'icon': 'fas fa-university',
                                'color': '#43e97b',
                                'children': [
                                    {
                                        'name': 'Приказы и другие распорядительные акты',
                                        'slug': 'orders-and-acts',
                                        'icon': 'fas fa-file-signature',
                                        'color': '#fa709a'
                                    },
                                    {
                                        'name': 'Государственные образовательные стандарты',
                                        'slug': 'state-educational-standards',
                                        'icon': 'fas fa-graduation-cap',
                                        'color': '#a8edea'
                                    }
                                ]
                            },
                            {
                                'name': 'Приказы по университету',
                                'slug': 'university-orders',
                                'icon': 'fas fa-building',
                                'color': '#ff9a9e',
                                'children': [
                                    {
                                        'name': 'Приказы, указы, решения учебных отделов',
                                        'slug': 'academic-departments-orders',
                                        'icon': 'fas fa-scroll',
                                        'color': '#ffecd2'
                                    }
                                ]
                            },
                            {
                                'name': 'Инструкции',
                                'slug': 'instructions',
                                'icon': 'fas fa-list-ul',
                                'color': '#667eea',
                                'children': [
                                    {
                                        'name': 'Инструкции о правах и обязанностях',
                                        'slug': 'rights-and-duties-instructions',
                                        'icon': 'fas fa-balance-scale',
                                        'color': '#4facfe'
                                    }
                                ]
                            },
                            {
                                'name': 'Положения',
                                'slug': 'regulations',
                                'icon': 'fas fa-file-contract',
                                'color': '#43e97b',
                                'children': [
                                    {
                                        'name': 'Типовые регламенты и правила',
                                        'slug': 'standard-regulations',
                                        'icon': 'fas fa-clipboard-list',
                                        'color': '#fa709a'
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'name': 'Планы',
                        'slug': 'plans',
                        'icon': 'fas fa-calendar-alt',
                        'color': '#a8edea',
                        'children': [
                            {
                                'name': 'Учебная работа',
                                'slug': 'academic-work',
                                'icon': 'fas fa-book',
                                'color': '#ff9a9e',
                                'children': [
                                    {
                                        'name': 'Базовые учебные планы',
                                        'slug': 'basic-curriculum',
                                        'icon': 'fas fa-file-alt',
                                        'color': '#ffecd2'
                                    },
                                    {
                                        'name': 'Перечень элективных курсов',
                                        'slug': 'elective-courses',
                                        'icon': 'fas fa-list',
                                        'color': '#667eea'
                                    }
                                ]
                            },
                            {
                                'name': 'Индивидуальные планы',
                                'slug': 'individual-plans',
                                'icon': 'fas fa-user-graduate',
                                'color': '#4facfe',
                                'children': [
                                    {
                                        'name': 'Индивидуальные планы ППС',
                                        'slug': 'individual-faculty-plans',
                                        'icon': 'fas fa-chalkboard-teacher',
                                        'color': '#43e97b'
                                    }
                                ]
                            },
                            {
                                'name': 'Профориентация',
                                'slug': 'career-orientation',
                                'icon': 'fas fa-compass',
                                'color': '#fa709a',
                                'children': [
                                    {
                                        'name': 'Планы профориентационной работы',
                                        'slug': 'career-orientation-plans',
                                        'icon': 'fas fa-route',
                                        'color': '#a8edea'
                                    }
                                ]
                            },
                            {
                                'name': 'Научно-исследовательская деятельность',
                                'slug': 'research-activity',
                                'icon': 'fas fa-microscope',
                                'color': '#ff9a9e',
                                'children': [
                                    {
                                        'name': 'Планы научно-исследовательской работы',
                                        'slug': 'research-work-plans',
                                        'icon': 'fas fa-project-diagram',
                                        'color': '#ffecd2'
                                    }
                                ]
                            },
                            {
                                'name': 'Издательская деятельность',
                                'slug': 'publishing-activity',
                                'icon': 'fas fa-book-open',
                                'color': '#667eea',
                                'children': [
                                    {
                                        'name': 'Утвержденные издательские планы',
                                        'slug': 'approved-publishing-plans',
                                        'icon': 'fas fa-stamp',
                                        'color': '#4facfe'
                                    }
                                ]
                            },
                            {
                                'name': 'Педагогическая нагрузка',
                                'slug': 'pedagogical-load',
                                'icon': 'fas fa-weight-hanging',
                                'color': '#43e97b',
                                'children': [
                                    {
                                        'name': 'Расчет часов и распределение нагрузки',
                                        'slug': 'hours-calculation',
                                        'icon': 'fas fa-calculator',
                                        'color': '#fa709a'
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'name': 'Отчеты',
                        'slug': 'reports',
                        'icon': 'fas fa-chart-bar',
                        'color': '#a8edea',
                        'children': [
                            {
                                'name': 'Учебная и учебно-методическая деятельность',
                                'slug': 'educational-methodical-activity',
                                'icon': 'fas fa-graduation-cap',
                                'color': '#ff9a9e',
                                'children': [
                                    {
                                        'name': 'Протоколы заседания департаментов',
                                        'slug': 'department-meeting-protocols',
                                        'icon': 'fas fa-file-signature',
                                        'color': '#ffecd2'
                                    },
                                    {
                                        'name': 'Входящие протоколы департаментов',
                                        'slug': 'incoming-department-protocols',
                                        'icon': 'fas fa-inbox',
                                        'color': '#667eea'
                                    }
                                ]
                            },
                            {
                                'name': 'Научно-исследовательская работа',
                                'slug': 'research-work-reports',
                                'icon': 'fas fa-flask',
                                'color': '#4facfe',
                                'children': [
                                    {
                                        'name': 'Годовые отчеты НИР',
                                        'slug': 'annual-research-reports',
                                        'icon': 'fas fa-calendar-check',
                                        'color': '#43e97b'
                                    },
                                    {
                                        'name': 'Утвержденные итоговые отчеты',
                                        'slug': 'approved-final-reports',
                                        'icon': 'fas fa-check-circle',
                                        'color': '#fa709a'
                                    }
                                ]
                            },
                            {
                                'name': 'Производственная практика',
                                'slug': 'internship-reports',
                                'icon': 'fas fa-hard-hat',
                                'color': '#a8edea',
                                'children': [
                                    {
                                        'name': 'Отчеты о прохождении практики',
                                        'slug': 'internship-completion-reports',
                                        'icon': 'fas fa-clipboard-check',
                                        'color': '#ff9a9e'
                                    }
                                ]
                            },
                            {
                                'name': 'Аттестация и комиссии',
                                'slug': 'certification-commissions',
                                'icon': 'fas fa-medal',
                                'color': '#ffecd2',
                                'children': [
                                    {
                                        'name': 'Отчеты аттестационных комиссий',
                                        'slug': 'certification-commission-reports',
                                        'icon': 'fas fa-award',
                                        'color': '#667eea'
                                    },
                                    {
                                        'name': 'Базы данных успеваемости',
                                        'slug': 'academic-performance-databases',
                                        'icon': 'fas fa-database',
                                        'color': '#4facfe'
                                    }
                                ]
                            },
                            {
                                'name': 'Научная деятельность',
                                'slug': 'scientific-activity-reports',
                                'icon': 'fas fa-atom',
                                'color': '#43e97b',
                                'children': [
                                    {
                                        'name': 'Отчеты о работе ППС',
                                        'slug': 'faculty-work-reports',
                                        'icon': 'fas fa-user-tie',
                                        'color': '#fa709a'
                                    },
                                    {
                                        'name': 'Графики взаимопосещений',
                                        'slug': 'mutual-visit-schedules',
                                        'icon': 'fas fa-calendar-alt',
                                        'color': '#a8edea'
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'name': 'Договоры',
                        'slug': 'contracts',
                        'icon': 'fas fa-handshake',
                        'color': '#ff9a9e',
                        'children': [
                            {
                                'name': 'По практике',
                                'slug': 'internship-contracts',
                                'icon': 'fas fa-file-contract',
                                'color': '#ffecd2',
                                'children': [
                                    {
                                        'name': 'Договоры о сотрудничестве',
                                        'slug': 'cooperation-agreements',
                                        'icon': 'fas fa-hands-helping',
                                        'color': '#667eea'
                                    }
                                ]
                            },
                            {
                                'name': 'По научному сотрудничеству',
                                'slug': 'scientific-cooperation',
                                'icon': 'fas fa-microscope',
                                'color': '#4facfe',
                                'children': [
                                    {
                                        'name': 'Переписка по университету',
                                        'slug': 'university-correspondence',
                                        'icon': 'fas fa-envelope',
                                        'color': '#43e97b'
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'name': 'Портфолио',
                        'slug': 'portfolio',
                        'icon': 'fas fa-briefcase',
                        'color': '#fa709a',
                        'children': [
                            {
                                'name': 'Портфолио ППС',
                                'slug': 'faculty-portfolio',
                                'icon': 'fas fa-user-graduate',
                                'color': '#a8edea',
                                'children': [
                                    {
                                        'name': 'Портфолио ППС',
                                        'slug': 'faculty-portfolio-docs',
                                        'icon': 'fas fa-folder-open',
                                        'color': '#ff9a9e'
                                    }
                                ]
                            },
                            {
                                'name': 'Курсовые и проекты студентов',
                                'slug': 'student-projects',
                                'icon': 'fas fa-graduation-cap',
                                'color': '#ffecd2',
                                'children': [
                                    {
                                        'name': 'Курсовые работы студентов',
                                        'slug': 'student-coursework',
                                        'icon': 'fas fa-book-open',
                                        'color': '#667eea'
                                    },
                                    {
                                        'name': 'Проекты студентов',
                                        'slug': 'student-projects-docs',
                                        'icon': 'fas fa-project-diagram',
                                        'color': '#4facfe'
                                    }
                                ]
                            },
                            {
                                'name': 'Учебные и научные публикации',
                                'slug': 'academic-publications',
                                'icon': 'fas fa-book',
                                'color': '#43e97b',
                                'children': [
                                    {
                                        'name': 'Статьи и публикации',
                                        'slug': 'articles-publications',
                                        'icon': 'fas fa-newspaper',
                                        'color': '#fa709a'
                                    },
                                    {
                                        'name': 'Учебные пособия',
                                        'slug': 'textbooks',
                                        'icon': 'fas fa-book-reader',
                                        'color': '#a8edea'
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]

        def create_category(data, parent=None, order=0):
            category = Category.objects.create(
                name=data['name'],
                slug=data['slug'],
                icon=data['icon'],
                color=data['color'],
                parent=parent,
                order=order
            )
            
            if 'children' in data:
                for i, child_data in enumerate(data['children']):
                    create_category(child_data, category, i)
            
            return category

        # Создаем структуру категорий
        for i, category_data in enumerate(categories_data):
            create_category(category_data, order=i)

        self.stdout.write(
            self.style.SUCCESS('Структура категорий успешно создана!')
        ) 