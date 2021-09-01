# Performance verification using iperf

This is intended to connect to a remote iperf server to test latency/jitter/drop
2 measurements will be sent, upstream and downstream

### Variables used

- iperf_host: Target iperf server (default to 127.0.0.1)
- iperf_port: Target iperf port   (default 5201)
- params: Set the parameter for iperf (Default, --bandwidth 1m) NOTE: --udp flag required!
- location: (optional) Location where the test originate from
- elastic_url: Elasticsearch URL to post data (default to http://elasticsearch:9200)
- HOSTNAME: Can be used to override the docker generate hostname

- Example:

docker run -it --rm -e host=127.0.0.1 -e params="--bandwidth 100k --udp --length 60" -e elastic_url=http://127.0.0.1:9200 iperf:latest 

