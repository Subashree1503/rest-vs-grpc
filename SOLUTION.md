### Performance Comparison: REST vs gRPC

| Method          | Local                | Same-Zone | Different Region |
|-----------------|----------------------|-----------|------------------|
| REST add        |2.825 ms per operation |3.126 ms per operation|296.878 ms per operation|
| gRPC add        |0.780 ms per operation |0.919 ms per operation|145.984 ms per operation|
| REST rawimg     |6.649 ms per operation |8.931 ms per operation |1201.090 ms per operation|
| gRPC rawimg     |10.043 ms per operation|12.877 ms per operation|207.0195 ms per operation|
| REST dotproduct |3.504 ms per operation |4.081 ms per operation|298.196 ms per operation|
| gRPC dotproduct |0.657 ms per operation |0.956 ms per operation|146.247 ms per operation|
| REST jsonimg    |35.720 ms per operation|50.754 ms per operation|1346.073 ms per operation|
| gRPC jsonimg    |22.517 ms per operation|35.909 ms per operation|230.274 ms per operation|
| PING            |                       |0.333 ms               |142 ms                  |




From the preformance table, we can see that gRPC consistently outperforms REST across all methods, especially with tasks involving higher latency. In local and same-zone environments, the performance gap is noticeable but not drastic. We can also see that gRPC is 3 to 5 times faster for most methods. 

However, in different-region environments, where network latency is much higher (reflected in the PING of 142 ms), the difference becomes much more pronounced. This is largely due to REST opening a new TCP connection for each request, which incurs significant overhead, particularly in high-latency environments. In contrast, gRPC uses a single persistent TCP connection for all queries, reducing the impact of latency and resulting in faster execution times.

Also, gRPC's performance with heavy tasks like `rawimgage`, `jsonimage` is not as dramatically better in local and same-zone environments (10.043 ms for gRPC vs. 6.649 ms for REST). However, as network latency increases, gRPC still maintains better performance for large data (e.g., jsonimg in different-region: 230.274 ms for gRPC vs. 1346.073 ms for REST), demonstrating its resilience in transferring heavier data in challenging network conditions. For applications with a high number of requests and significant latency, such as those spanning across regions, gRPC offers better scalability due to its efficient connection reuse and binary protocol. REST’s overhead grows exponentially with network distance, making it less ideal for these types of distributed systems.
