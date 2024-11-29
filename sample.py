from otel_config import init_config

def do_metric(meter):
    #{__name__="http_server_duration_milliseconds_bucket", http_flavor="1.1", http_method="GET", http_route="/", http_scheme="http", http_status_code="404", job="jeju_airport_45", le="75", net_host_name="localhost", net_host_port="8080"}

    work_counter = meter.create_counter(
        "http_server_duration_milliseconds_bucket", unit="1", description="test counter"
    )
    work_counter.add(1, {"work.type": "type hehe"})


def do_trace(tracer):
    @tracer.start_as_current_span("do_trace_internal")
    def do_trace_internal():
        pass

    do_trace_internal()


def main(meter, tracer):
    do_metric(meter)
    do_trace(tracer)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print(f"Usage {sys.argv[0]} [your service name]")
        exit(-1)
    service_name = sys.argv[1]

    meter, tracer = init_config(service_name, local=False)
    main(meter, tracer)