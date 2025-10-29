from operator import ge
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from db.app import (
    get_db,
    get_performances,
    add_performance,
    remove_performance,
    update_performance,
)
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


provider = TracerProvider() # Set up OpenTelemetry Tracer Provider
processor = BatchSpanProcessor(OTLPSpanExporter(
    endpoint="otel-collector:4317",
    insecure=True,
)) # Set up Span Processor with OTLP Exporter
provider.add_span_processor(processor) # Add Span Processor to Provider
trace.set_tracer_provider(provider) # Set the global Tracer Provider

tracer = trace.get_tracer(__name__)

app = FastAPI()

FastAPIInstrumentor.instrument_app(app, tracer_provider=provider) # Instrument FastAPI app with OpenTelemetry

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
    db_gen = get_db()
    db = next(db_gen)

    result = get_performances(db)
    return JSONResponse(
        content=[
            {"id": r.id, "name": r.name, "time_taken": r.time_taken} for r in result
        ],
        status_code=200,
    )


@app.get("/api/scoreboard")
async def get_scoreboard():
    db_gen = get_db()
    db = next(db_gen)
    result = get_performances(db)
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
    db_gen = get_db()
    db = next(db_gen)
    performance = add_performance(db, name=content.name, time_taken=content.time_taken)
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
    db_gen = get_db()
    db = next(db_gen)
    result = remove_performance(db, performance_id)
    if result:
        return JSONResponse(content={"message": "Performance removed"}, status_code=200)
    else:
        return JSONResponse(
            content={"message": "Performance not found"}, status_code=404
        )


@app.put("/api/update_performance/{performance_id}")
async def update_Performance(performance_id: int, content: addPerformanceRequest):
    db_gen = get_db()
    db = next(db_gen)
    performance = update_performance(
        db, performance_id, name=content.name, time_taken=content.time_taken
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

