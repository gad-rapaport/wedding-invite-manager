from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics

db = SQLAlchemy()
metrics = PrometheusMetrics.for_app_factory()


def create_app(test_config: dict = None):
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    metrics.init_app(app)

    with app.app_context():
        from app.models import guest, event, message_log
        db.create_all()

    from app.routes.api_routes import api_bp
    from app.routes.ui_routes import ui_bp
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(ui_bp)

    return app
