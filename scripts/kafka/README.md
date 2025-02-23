## Deployment notes

Kafka can be accessed by consumers via port 9092 on the following DNS name from within your cluster:

    kafka-operator.data-platform.svc.cluster.local

Each Kafka broker can be accessed by producers via port 9092 on the following DNS name(s) from within your cluster:

    kafka-operator-controller-0.kafka-operator-controller-headless.data-platform.svc.cluster.local:9092
    kafka-operator-controller-1.kafka-operator-controller-headless.data-platform.svc.cluster.local:9092
    kafka-operator-controller-2.kafka-operator-controller-headless.data-platform.svc.cluster.local:9092

The CLIENT listener for Kafka client connections from within your cluster have been configured with the following security settings:
    - SASL authentication
    - TLS encryption
    - mTLS authentication

To connect a client to your Kafka, you need to create the 'client.properties' configuration files with the content below:

security.protocol=SASL_SSL
sasl.mechanism=SCRAM-SHA-256
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
    username="brokerUser" \
    password="$(kubectl get secret kafka-operator-user-passwords --namespace data-platform -o jsonpath='{.data.client-passwords}' | base64 -d | cut -d , -f 1)";
ssl.truststore.type=JKS
ssl.truststore.location=/tmp/kafka.truststore.jks
#ssl.truststore.password=
ssl.keystore.type=JKS
ssl.keystore.location=/tmp/client.keystore.jks
#ssl.keystore.password=

To create a pod that you can use as a Kafka client run the following commands:

    kubectl run kafka-operator-client --restart='Never' --image docker.io/bitnami/kafka:3.9.0-debian-12-r6 --namespace data-platform --command -- sleep infinity
    kubectl cp --namespace data-platform /path/to/client.properties kafka-operator-client:/tmp/client.properties
    kubectl cp --namespace data-platform ./kafka.truststore.jks kafka-operator-client:/tmp/kafka.truststore.jks
    kubectl cp --namespace data-platform ./client.keystore.jks kafka-operator-client:/tmp/client.keystore.jks
    kubectl exec --tty -i kafka-operator-client --namespace data-platform -- bash

    PRODUCER:
        kafka-console-producer.sh \
            --producer.config /tmp/client.properties \
            --bootstrap-server kafka-operator.data-platform.svc.cluster.local:9092 \
            --topic test

    CONSUMER:
        kafka-console-consumer.sh \
            --consumer.config /tmp/client.properties \
            --bootstrap-server kafka-operator.data-platform.svc.cluster.local:9092 \
            --topic test \
            --from-beginning
To connect to your Kafka controller+broker nodes from outside the cluster, follow these instructions:
    Kafka brokers domain: You can get the external node IP from the Kafka configuration file with the following commands (Check the EXTERNAL listener)

        1. Obtain the pod name:

        kubectl get pods --namespace data-platform -l "app.kubernetes.io/name=kafka,app.kubernetes.io/instance=kafka-operator,app.kubernetes.io/component=kafka"

        2. Obtain pod configuration:

        kubectl exec -it KAFKA_POD -- cat /opt/bitnami/kafka/config/server.properties | grep advertised.listeners
    Kafka brokers port: You will have a different node port for each Kafka broker. You can get the list of configured node ports using the command below:

        echo "$(kubectl get svc --namespace data-platform -l "app.kubernetes.io/name=kafka,app.kubernetes.io/instance=kafka-operator,app.kubernetes.io/component=kafka,pod" -o jsonpath='{.items[*].spec.ports[0].nodePort}' | tr ' ' '\n')"

The EXTERNAL listener for Kafka client connections from within your cluster have been configured with the following settings:
    - SASL authentication
    - TLS encryption
    - mTLS authentication

To connect a client to your Kafka, you need to create the 'client.properties' configuration files with the content below:

security.protocol=SASL_SSL
sasl.mechanism=SCRAM-SHA-256
sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule required \
    username="brokerUser" \
    password="$(kubectl get secret kafka-operator-user-passwords --namespace data-platform -o jsonpath='{.data.client-passwords}' | base64 -d | cut -d , -f 1)";
ssl.truststore.type=JKS
ssl.truststore.location=/tmp/kafka.truststore.jks
#ssl.truststore.password=
ssl.keystore.type=JKS
ssl.keystore.location=/tmp/client.keystore.jks
#ssl.keystore.password=

WARNING: There are "resources" sections in the chart not set. Using "resourcesPreset" is not recommended for production. For production installations, please set the following values according to your workload needs:
  - controller.resources
  - externalAccess.autoDiscovery.resources
+info https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/