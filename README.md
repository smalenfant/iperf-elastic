# Performance verification using iperf

This is intended to connect to a remote iperf server to test latency/jitter/drop

### Variables used

- iperf_host: Target iperf server (default to 127.0.0.1)
- iperf_port: Target iperf port   (default 5201)
- location: (optional) Location where the test originate from
- elastic_url: Elasticsearch URL to post data (default to http://elasticsearch:9200)
- HOSTNAME: Can be used to override the docker generate hostname

- Example:

docker run -it --rm -e host=127.0.0.1 -e port=5201 -e HOSTNAME=me -e location="here" -e elastic_url=http://127.0.0.1:9200 iperf:latest 

