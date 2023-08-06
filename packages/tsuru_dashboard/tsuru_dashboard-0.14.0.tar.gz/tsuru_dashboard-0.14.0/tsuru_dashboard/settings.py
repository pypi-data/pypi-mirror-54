import os


TSURU_HOST = os.environ.get("TSURU_HOST", "http://localhost:8080")
ELASTICSEARCH_HOST = os.environ.get("ELASTICSEARCH_HOST")
PROMETHEUS_HOST = os.environ.get("PROMETHEUS_HOST")
ELASTICSEARCH_INDEX = os.environ.get("ELASTICSEARCH_INDEX", ".measures-tsuru")
METRICS_COMPONENTS = os.environ.get("METRICS_COMPONENTS", "registry, big-sibling")
RESOLVE_CONNECTION_HOSTS = os.environ.get("RESOLVE_CONNECTION_HOSTS", "") in ['true', 'True', '1']
