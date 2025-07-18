from .celery import app as celery_app

# ? ensuring it is loaded when django starts
__all__ = ['celery_app']