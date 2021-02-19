listen {
  port = 4040
  metrics_endpoint = "/metrics"
}

namespace "nginx" {
  format = "$remote_addr - $remote_user [$time_local] \"$request\" $status $body_bytes_sent \"$http_referer\" \"$http_user_agent\" rt=$request_time uct=\"$upstream_connect_time\" uht=\"$upstream_header_time\" urt=\"$upstream_response_time\""
  histogram_buckets = [.005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10]
  source {
    files = ["/var/log/nginx/app.log"]
  }
  print_log = true
}

