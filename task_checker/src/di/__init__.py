from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from .providers import AppProvider


def setup_di(app):
    container = make_async_container(AppProvider())
    setup_dishka(container=container, app=app)
