from dotenv import load_dotenv
from strands.telemetry import StrandsTelemetry

def set_telemetry():
    load_dotenv()
    strands_telemetry = StrandsTelemetry()
    strands_telemetry.setup_otlp_exporter()
