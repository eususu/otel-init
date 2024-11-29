################## Common
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.resources import SERVICE_NAME
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

################## METRIC
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
################## TRACE
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)


def init_config(service_name:str, local:bool):
    resource = Resource(
        attributes={
            SERVICE_NAME: service_name,
        }
    )
    url='http://localhost:4317'
    span_exporter = OTLPSpanExporter(
        endpoint=url,
        insecure=True
    )

    metric_exporter = OTLPMetricExporter(
        endpoint=url,
        insecure=True,
    )

    if local:
        span_exporter = ConsoleSpanExporter()
        metric_exporter = ConsoleMetricExporter()

    meter = init_metric(resource, metric_exporter)
    tracer = init_trace(resource, span_exporter)

    return meter, tracer

def init_metric(resource:Resource, exporter):

    metric_reader = PeriodicExportingMetricReader(exporter)
    provider = MeterProvider(metric_readers=[metric_reader], resource=resource)

    # Sets the global default meter provider
    metrics.set_meter_provider(provider)

    # Creates a meter from the global meter provider
    meter = metrics.get_meter("http_server_duration_milliseconds_bucket")
    return meter


def init_trace(resource:Resource, exporter):

    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)

    # Sets the global default tracer provider
    trace.set_tracer_provider(provider)

    # Creates a tracer from the global tracer provider
    tracer = trace.get_tracer("my.tracer.name")
    return tracer

