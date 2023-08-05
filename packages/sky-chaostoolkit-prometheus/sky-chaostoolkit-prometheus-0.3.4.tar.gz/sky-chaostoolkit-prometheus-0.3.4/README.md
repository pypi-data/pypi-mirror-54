# chaostoolkit-prometheus

[Prometheus][prometheus] support for the [Chaos Toolkit][chaostoolkit].

[prometheus]: https://prometheus.io/
[chaostoolkit]: http://chaostoolkit.org/

## Install

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

[chaostoolkit]: https://github.com/chaostoolkit/chaostoolkit

```
$ pip install sky-chaostoolkit-prometheus
```

## Usage

To use this package, you must have access to a Prometheus instance via
HTTP and be allowed to connect to it.

This package only exports probes to query for some aspects of your system as
monitored by Prometheus.  It can also query for active alerts for a given metric using the
`query_alerts_exist_for_job` function

Here is an example of querying Prometheus at a given moment

```json
{
    "type": "probe",
    "name": "fetch-cpu-just-2mn-ago",
    "provider": {
        "type": "python",
        "module": "chaosprometheus.probes",
        "func": "query",
        "arguments": {
            "query": "process_cpu_seconds_total{job='websvc'}",
            "when": "2 minutes ago"
        }
    }
}
```

You can also ask for an interval as follows:

```json
{
    "type": "probe",
    "name": "fetch-cpu-over-interval",
    "provider": {
        "type": "python",
        "module": "chaosprometheus.probes",
        "func": "query_interval",
        "arguments": {
            "query": "process_cpu_seconds_total{job='websvc'}",
            "start": "2 minutes ago",
            "end": "now",
            "step": 5
        }
    }
}
```

In both cases, the probe returns the [JSON payload as-is][api] from Prometheus
or raises an exception when an error is met.

[api]: https://prometheus.io/docs/querying/api/

The result is not further processed and should be found in the generated report
of the experiment run.
