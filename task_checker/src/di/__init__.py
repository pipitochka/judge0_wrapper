from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from .providers import AppProvider
from config import app_settings


def setup_di(app):
    container = make_async_container(AppProvider(app_settings.get_database_url()))
    setup_dishka(container=container, app=app)
