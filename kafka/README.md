# Apache Kafka

## Architecture

- Kafka servers are referred to as brokers
- All of the brokers that work together are referred to as a cluster
- Clusters may consist of just one broker, or thousands of brokers
- Apache Zookeeper is used by Kafka brokers to determine which broker is the leader of a given partition and topic
- Zookeeper keeps track of which brokers are part of the Kafka cluster
- Zookeeper stores configuration for topics and permissions (Access Control Lists - ACLs)
    - ACLs are Permissions associated with an object. In Kafka, this typically refers to a user’s permissions with respect to production and consumption, and/or the topics themselves.
- Kafka nodes may gracefully join and leave the cluster
- Kafka runs on the Java Virtual Machine (JVM)

## How Kafka Stores Data

The way that Kafka stores data is pretty simple. It has a data directory on a disk where it stores logs of data and text files. `/var/lib/kafka/data` is a directory where Kafta sorts data in your workspace and in many Kafka productions systems.

- Each topic receives its own sub-directory with the associated name of the topic.
- Kafka may store more than one log file for a given topic
- Kafka stores data on disk in folders for each of its topics

## Data Partitioning

### Message Ordering

Message ordering is only guaranteed within a partition in Kafka. If your topic has more than one partition, Kafka provides no guarantees that the messages will be consumed in the order they were produced. For many applications, this is an acceptable tradeoff for increasing the parallelism and speed of consumption. Your producer applications may still add metadata to the event header or message body itself to indicate ordering. However, this logic would belong to your application, and not Kafka itself. For example, you may place an increasing ID sequence in every message (eg 1, 2, 3, and so on) or a granular timestamp to indicate the order of a message.

- A single topic may have more than one partition. Each partition, such as “a” and “b” above, may live on different brokers, or on all of the brokers.

### Partitioning Topics

- The “right” number of partitions is highly dependent on the scenario.
- The most important number to understand is desired throughput. How many MB/s do you need to achieve to hit your goal?
- You can easily add partitions at a later date by modifying a topic.
- Partitions have performance consequences. They require additional networking latency and potential rebalances, leading to unavailability.
- To determine the number of partitions you need by dividing the overall throughput you want by the throughput per single consumer partition or the throughput per single producer partition. Pick the larger of these two numbers to determine the needed number of partitions.
    - `# Partitions = Max(Overall Throughput/Producer Throughput, Overall Throughput/Consumer Throughput)`
    - Example:
        - With 3 producers and 5 consumers, each operating at 10MB/s per single producer/consumer partition:
        - `Max(100MBs/(3 *10MB/s), 100MBs/(5* 10MB/s)) = Max(2) ~= *4 partitions needed*`

- Ordering is guaranteed only within a topic’s partitions

## Data Replication

### Preventing Data Loss

Based on an understanding that machines can fail, one of the core features of Kafka is the concept of replication.

- Replication – when the data is written to many brokers
- Leader Broker – the broker responsible for sending and receiving data to clients for a given topic partition
- Replicas – any brokers that are storing replicated data

If the leader broker were to fail, one of the replicas would be elected the new topic partition leader by a zookeeper election.

The exact number of replicas used can be configured globally as a Kafta server configuration item or set individually on every topic you create. But keep a few things in mind:

1. You can not have more replicas than brokers
2. Data replication has overhead
3. Always enable replication in a production cluster to prevent data loss

Kafka uses data replication to duplicate data across multiple machines to prevent data loss in case a broker fails

Commonlym the desired replication factor is set at the topic level and the value should always be specificed when creating a topic

## Security

Kafka is secured via mutual TLS (mTLS) or Simple Authentication and Security Layer (SASL). Configuring these security mechanisms is outside of the scope of this class. For hobbyist usage, Kafka is typically run unencrypted. However, if you are using Kafka at your job, or to transport sensitive information, you should either invest the time to secure Kafka or work with your company's security team to help you accomplish this.

## Topic 

### Configuration

- Data replication can be set on **per-topic basis**
- A broker must be an ***"In Sync Replica" (ISR)*** to become leader
- **Desired number of ISRs** can be set on topic
- **Number of ISRs must succeed** when data is sent

### Naming

- The only enforced rules for topic names are that they must be less than 256 characters, consist only of alphanumeric characters (a-z, A-Z, 0-9), “.”, “_”, or “-”.
- There is no idiomatic or universally correct naming convention.
- Naming conventions can help reduce confusion, save time, and even increase reusability.

Example:
    - Considering starting with a namespace, like `com.natanascimento`
    - Considering segmenting on model type like `com.natanascimento.lesson`, where `lesson` is the model 
    - Considering segmenting on event type like `com.natanascimento.lesson.quiz_complete`, where `quiz_complete` is the event

### Data Management

- **Data retention** determines how long Kafka stores data in a topic
    - The `retention.bytes`, `retention.ms` settings control retention policy
- When data expires it's deleted from the topic
    - This is true if `cleanup.policy` is set to delete
- Retention policies may be time based. Once data reaches a certain age it is deleted.
    - The `retention.ms` setting controls retention policy on time
- Retention policies may be size based. Once a topic reaches a certain age the oldest data is deleted.
    - The `retention.bytes` setting controls retention policy on time
- Retention policies may be both time- and size-based. Once either condition is reached, the oldest data is deleted.
- Alternatively, topics can be compacted in which there is no size or time limit for data in the topic.
    - This is true if `cleanup.policy` is set to compact
- Compacted topics use the message key to identify messages uniquely. If a duplicate key is found, the latest value for that key is kept, and the old message is deleted.
- Kafka topics can use compression algorithms to store data. This can reduce network overhead and save space on brokers. Supported compression algorithms include: lz4, ztsd, snappy, and gzip.
    - `compression.type` controls the type of message compression for a topic
- Kafka topics should store data for one type of event, not multiple types of events. Keeping multiple event types in one topic will cause your topic to be hard to use for downstream consumers.

### Creation

- Create topics manually, you can create topics automatically, but this is an anti-pattern and bad practice.
- Write code or use a provisioning tool to **manually create your topics** as needed.



## Glossary

- Broker (Kafka) - A single member server of the Kafka cluster
- Cluster (Kafka) - A group of one or more Kafka Brokers working together to satisfy Kafka production and consumption
- Node - A single computing instance. May be physical, as in a server in a datacenter, or virtual, as an instance might be in AWS, GCP, or Azure.
- Zookeeper - Used by Kafka Brokers to determine which broker is the leader of a given partition and topic, as well as track cluster membership and configuration for Kafka
- Access Control List (ACL) - Permissions associated with an object. In Kafka, this typically refers to a user’s permissions with respect to production and consumption, and/or the topics themselves.
- JVM - The Java Virtual Machine - Responsible for allowing host computers to execute the byte-code compiled against the JVM.
- Data Partition (Kafka) - Kafka topics consist of one or more partitions. A partition is a log which provides ordering guarantees for all of the data contained within it. Partitions are chosen by hashing key values.
- Data Replication (Kafka) - A mechanism by which data is written to more than one broker to ensure that if a single broker is lost, a replicated copy of the data is available.
- In-Sync Replica (ISR) - A broker which is up to date with the leader for a particular broker for all of the messages in the current topic. This number may be less than the replication factor for a topic.
- Rebalance - A process in which the current set of consumers changes (addition or removal of consumer). When this occurs, assignment of partitions to the various consumers in a consumer group must be changed.
- Data Expiration - A process in which data is removed from a Topic log, determined by data retention policies.
- Data Retention - Policies that determine how long data should be kept. Configured by time or size.
- Batch Size - The number of messages that are sent or received from Kafka
- acks - The number of broker acknowledgements that must be received from Kafka before a producer continues processing
- Synchronous Production - Producers which send a message and wait for a response before performing additional processing
- Asynchronous Production - Producers which send a message and do not wait for a response before performing additional processing
- Avro - A binary message serialization format
- Message Serialization - The process of transforming an applications internal data representation to a format suitable for interprocess communication over a protocol like TCP or HTTP.
- Message Deserialization - The process of transforming an incoming set of data from a form suitable for interprocess communication, into a data representation more suitable for the application receiving the data.
- Retries (Kafka Producer) - The number of times the underlying library will attempt to deliver data before moving on
- Consumer Offset - A value indicating the last seen and processed message of a given consumer, by ID.
- Consumer Group - A collection of one or more consumers, identified by group.id which collaborate to consume data from Kafka and share a consumer offset.
- Consumer Group Coordinator - The broker in charge of working with the Consumer Group Leader to initiate a rebalance
- Consumer Group Leader - The consumer in charge of working with the Group Coordinator to manage the consumer group
- Topic Subscription - Kafka consumers indicate to the Kafka Cluster that they would like to consume from one or more topics by specifying one or more topics that they wish to subscribe to.
- Consumer Lag - The difference between the offset of a consumer group and the latest message offset in Kafka itself

## Data

### Glossary

- CCPA - California Consumer Privacy Act
- GDPR - General Data Protection Regulation


## References

- [Why does Kafka need Zookeeper?](https://www.cloudkarafka.com/blog/2018-07-04-cloudkarafka_what_is_zookeeper.html)
- [KIP-500](https://cwiki.apache.org/confluence/display/KAFKA/KIP-500%3A+Replace+ZooKeeper+with+a+Self-Managed+Metadata+Quorum)
- [Architecture](https://kafka.apache.org/documentation/#design)
- [Data Partitioning](https://kafka.apache.org/documentation/#intro_topics)
- [Considerations in choosing the number of partitions](https://www.confluent.io/blog/how-choose-number-topics-partitions-kafka-cluster)
- [Data Replication](https://kafka.apache.org/documentation/#replication)
- [Topic configs](https://kafka.apache.org/documentation.html#topicconfigs)
