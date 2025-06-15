from opentelemetry.trace import get_current_span
import logging

class OpenTelemetryLoggingFilter(logging.Filter):
    def filter(self, record):
        span = get_current_span()
        span_context = span.get_span_context()

        # Set trace_id and span_id if available, else fallback
        record.otelTraceID = format(span_context.trace_id, '032x') if span_context.trace_id else "N/A"
        record.otelSpanID = format(span_context.span_id, '016x') if span_context.span_id else "N/A"

        return True
