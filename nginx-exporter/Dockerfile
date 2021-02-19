FROM quay.io/martinhelmich/prometheus-nginxlog-exporter:v1

COPY config.hcl /etc/prometheus-nginxlog-exporter.hcl
CMD ["-config-file", "/etc/prometheus-nginxlog-exporter.hcl"]
