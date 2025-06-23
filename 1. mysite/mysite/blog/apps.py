from django.apps import AppConfig

#! This includes the main configuration of the blog application
class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
