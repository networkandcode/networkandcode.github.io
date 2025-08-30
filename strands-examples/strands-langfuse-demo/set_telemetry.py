import os
import base64

from dotenv import load_dotenv
from strands.telemetry import StrandsTelemetry


def set_telemetry():
    load_dotenv()

    # Build Basic Auth header.
    LANGFUSE_AUTH = base64.b64encode(
        f"{os.environ.get('LANGFUSE_PUBLIC_KEY')}:{os.environ.get('LANGFUSE_SECRET_KEY')}".encode()
    ).decode()
    
    # Configure OpenTelemetry endpoint & headers
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"

    strands_telemetry = StrandsTelemetry()
    strands_telemetry.setup_otlp_exporter()
