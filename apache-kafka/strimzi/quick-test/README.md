# Test Apache Kafka Cluster Deployment

1. **Make Shell Scripts Executable**

    Use the following command to ensure all shell scripts are executable:
    ```bash
    chmod +x *.sh
    ```

2. **Send Messages to a Kafka Topic**

    With the cluster running, execute the producer script to send messages to a Kafka topic (the topic will be created automatically):
    ```bash
    ./send.sh
    ```
    You’ll see a prompt where you can type your messages. For example:
    ```sh
    If you don't see a command prompt, press Enter.
    >Hello sciDX
    ```

3. **Receive Messages from the Kafka Topic**

    In a separate terminal, run the consumer script to receive messages:
    ```bash
    ./receive.sh
    ```
    If everything is configured correctly, you’ll see the message you sent earlier:
    ```bash
    If you don't see a command prompt, press Enter.
    >Hello sciDX!
    ```
