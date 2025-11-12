from operator import ge
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from db.app import (
    get_performances,
    add_performance,
    remove_performance,
    update_performance,
)

# NOTE: TRACE IMPORT
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# NOTE: METRICS IMPORT
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor

# NOTE: LOGS IMPORT
# import logging
# from opentelemetry import logs
# from opentelemetry.sdk.logs import LoggerProvider, LoggingHandler
# from opentelemetry.sdk.logs.export import BatchLogRecordProcessor
# from opentelemetry.exporter.otlp.proto.grpc.log_exporter import OTLPLogExporter

# NOTE: TRACES
provider_trace = TracerProvider()
trace_exporter = OTLPSpanExporter(
    endpoint="otel-collector:4317",
    insecure=True,
)
span_exporter = BatchSpanProcessor(trace_exporter)
provider_trace.add_span_processor(span_exporter)
trace.set_tracer_provider(provider_trace)

tracer = trace.get_tracer(__name__)

# NOTE: METRICS
metric_exporter = OTLPMetricExporter(
    endpoint="otel-collector:4317",
    insecure=True,
)
reader = PeriodicExportingMetricReader(metric_exporter)

provider_metrics = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider_metrics)

SystemMetricsInstrumentor().instrument(meter_provider=provider_metrics)

app = FastAPI()

# NOTE: LOGS
# log_exporter = OTLPLogExporter(endpoint="otel-collector:4317", insecure=True)
# provider_logs = LoggerProvider()
# provider_logs.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
# logs.set_logger_provider(provider_logs)
#
# handler = LoggingHandler(level=logging.INFO)
# logging.getLogger().addHandler(handler)
# logging.getLogger().setLevel(logging.INFO)

FastAPIInstrumentor.instrument_app(app)

# NOTE: APP
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/debug_trace")
async def debug_trace():
    with tracer.start_as_current_span("debug-span"):
        return {"message": "Tracing works!"}


@app.get("/api/all_performance")
async def get_all_performance():
    result = get_performances()
    return JSONResponse(
        content=[
            {"id": r.id, "name": r.name, "time_taken": r.time_taken} for r in result
        ],
        status_code=200,
    )


@app.get("/api/scoreboard")
async def get_scoreboard():
    result = get_performances()
    sorted_result = sorted(result, key=lambda x: x.time_taken)[:10]
    return JSONResponse(
        content=[
            {"id": r.id, "name": r.name, "time_taken": r.time_taken}
            for r in sorted_result
        ],
        status_code=200,
    )


class addPerformanceRequest(BaseModel):
    name: str
    time_taken: int


@app.post("/api/add_performance")
async def add_Performance(content: addPerformanceRequest):
    performance = add_performance(name=content.name, time_taken=content.time_taken)
    return JSONResponse(
        content={
            "id": performance.id,
            "name": performance.name,
            "time_taken": performance.time_taken,
        },
        status_code=201,
    )


@app.delete("/api/remove_performance/{performance_id}")
async def remove_Performance(performance_id: int):
    result = remove_performance(performance_id)
    if result:
        return JSONResponse(content={"message": "Performance removed"}, status_code=200)
    else:
        return JSONResponse(
            content={"message": "Performance not found"}, status_code=404
        )


@app.put("/api/update_performance/{performance_id}")
async def update_Performance(performance_id: int, content: addPerformanceRequest):
    performance = update_performance(
        performance_id, name=content.name, time_taken=content.time_taken
    )
    if performance:
        return JSONResponse(
            content={
                "id": performance.id,
                "name": performance.name,
                "time_taken": performance.time_taken,
            },
            status_code=200,
        )
    else:
        return JSONResponse(
            content={"message": "Performance not found"}, status_code=404
        )
