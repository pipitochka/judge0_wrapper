from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka, FastapiProvider

from .providers import AppProvider


def setup_di(app):
    container = make_async_container(*[
        AppProvider(),
        FastapiProvider()
    ])
    setup_dishka(container=container, app=app)
