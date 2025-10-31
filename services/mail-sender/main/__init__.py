from flask import Flask
from .config import Settings


def create_app():
    app = Flask(__name__)
    settings = Settings()
    app.config.from_mapping(settings.model_dump())

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    return app
