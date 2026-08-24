import os

from django.core.wsgi import get_wsgi_application
from opentelemetry.instrumentation.django import DjangoInstrumentor

from .telemetry import configurar_telemetria


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "miproyecto.settings"
)

configurar_telemetria()

DjangoInstrumentor().instrument()

application = get_wsgi_application()