from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, vendor, booking

from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

from app.db.session import engine

import logging
from app.utils.logging import OpenTelemetryLoggingFilter

# Logging setup with trace context
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s [%(name)s] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s] %(message)s'
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
handler.addFilter(OpenTelemetryLoggingFilter())

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Tracer setup
trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "vendor-booking-api"}))
)
tracer = trace.get_tracer(__name__)

# Export spans via HTTP OTLP
otlp_exporter = OTLPSpanExporter(endpoint="otel-collector:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# App setup
app = FastAPI(title="Vendor Booking API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FastAPIInstrumentor.instrument_app(app)
SQLAlchemyInstrumentor().instrument(engine=engine.sync_engine)

@app.get("/")
def read_root():
    logger.info("Health check hit on root endpoint")
    return {"msg": "Vendor Booking API is running"}

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(vendor.router, prefix="/vendors", tags=["Vendors"])
app.include_router(booking.router, prefix="/bookings", tags=["Bookings"])
