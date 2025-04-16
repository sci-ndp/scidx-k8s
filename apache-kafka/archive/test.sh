# produce a message to a topic
echo "key1:value1" | kcat -b kcat -b a49496f7fa9a34ba4a1b8b193ed3ff95-872419998.us-west-2.elb.amazonaws.com:31093 -t test-topic -C -t test-topic -P -K:

# consume a message from a topic
kcat -b a49496f7fa9a34ba4a1b8b193ed3ff95-872419998.us-west-2.elb.amazonaws.com:31093 -t test-topic -C