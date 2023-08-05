from airflow.utils.decorators import apply_defaults
from airflow.contrib.sensors.pubsub_sensor import PubSubPullSensor
from airflow.contrib.hooks.gcp_pubsub_hook import PubSubHook
from airflow.contrib.operators.pubsub_operator import (
    PubSubSubscriptionCreateOperator,
    PubSubTopicDeleteOperator,
    PubSubSubscriptionDeleteOperator
)
import base64


class SharedTopicPubSubPullSensor(PubSubPullSensor):
    """
        A pubsub pull sensor that can be set to listen for a specific trigger message
        from a central pubsub topic that's shared among many publishers and subscribers.
        Different instances of the sensor can be set to listen for different messages.
        :param project: the GCP project ID where the topic and subscriptions live (templated)
        :type project: str
        :param subscription: the Pub/Sub subscription name. Do not include the
            full subscription path.
        :type subscription: str
        :param trigger_msg: message the sensor is waiting for from the topic
        :type trigger_msg: str
        :param max_messages: The maximum number of messages to retrieve per
            PubSub pull request
        :type max_messages: int
        :param return_immediately: If True, instruct the PubSub API to return
            immediately if no messages are available for delivery.
        :type return_immediately: bool
        :param ack_messages: If True, each message will be acknowledged
            immediately rather than by any downstream tasks
        :type ack_messages: bool
        :param gcp_conn_id: The connection ID to use connecting to
            Google Cloud Platform.
        :type gcp_conn_id: str
        :param delegate_to: The account to impersonate, if any.
            For this to work, the service account making the request
            must have domain-wide delegation enabled.
        :type delegate_to: str
    """
    @apply_defaults
    def __init__(
            self,
            project,
            subscription,
            trigger_msg,
            max_messages=1000,
            return_immediately=True,
            ack_messages=True,
            gcp_conn_id='google_cloud_default',
            delegate_to=None,
            poke_interval=120,
            timeout=10800,
            *args,
            **kwargs):

        super(
            SharedTopicPubSubPullSensor,
            self).__init__(
            project=project,
            subscription=subscription,
            max_messages=max_messages,
            return_immediately=return_immediately,
            ack_messages=ack_messages,
            gcp_conn_id=gcp_conn_id,
            poke_interval=poke_interval,
            timeout=timeout,
            *args,
            **kwargs)

        self.gcp_conn_id = gcp_conn_id
        self.delegate_to = delegate_to
        self.project = project
        self.subscription = subscription
        self.max_messages = max_messages
        self.return_immediately = return_immediately
        self.ack_messages = ack_messages
        self._messages = None
        self.trigger_msg = trigger_msg

    def poke(self, context):
        self.log.info("poking...")
        hook = PubSubHook(gcp_conn_id=self.gcp_conn_id,
                          delegate_to=self.delegate_to)
        self.log.info("pulling messages...")
        self._messages = hook.pull(
            self.project, self.subscription, self.max_messages,
            self.return_immediately)
        if not self._messages:
            self.log.info("no messages found")
        elif self._messages and self.ack_messages:
            self.log.info("found " + str(len(self._messages)) + " message(s)")
            # This section is just to log info about the message.  It's been left
            # in to help with debugging production problems,
            for mes in self._messages:
                self.log.info(
                    "data: " +
                    base64.b64decode(
                        mes['message']['data']))
                for k, v in mes.iteritems():
                    self.log.info("key: " + str(k))
                    self.log.info("value: " + str(v))

            # Create an empty list to track ids of messages we want to acknowledge
            trigger_msg_found = False
            ack_ids = []
            # Check each pulled message and see if it contains the trigger
            # message the sensor is waiting for. 
            for m in self._messages:
                if m.get('ackId') and m.get('message') and base64.b64decode(m['message']['data']) == self.trigger_msg:
                    self.log.info("found trigger message:  " + self.trigger_msg)
                    trigger_msg_found = True
                # Add the ackId to a list so the list can be used after the looping is done.
                # The list will be passed via the hook to tell pubsub to acknowlege all the pulled messages.
                ack_ids.append(m.get('ackId'))
            # Acknowledge all messages that were pulled
            if self.ack_messages:
                self.log.info("acknowledging messages")
                hook.acknowledge(self.project, self.subscription, ack_ids)
            if trigger_msg_found:
                return self.trigger_msg



class SharedTopicSubscriptionTaskSet:

    """
        A convenience class for more easily creating the two operators and one sensor
        needed to subscribe to a pubsub topic, listen for a specific message and
        then delete the subscription once the message has been received.
        :param dag: the dag the airflow tasks will be added onto
        :type dag: dag
        :param gcp_conn_id: the connection to use to talk to the pubsub topic
        :type gcp_conn_id: str
        :param project: the GCP project ID where the topic and subscriptions live (templated)
        :type project: str
        :param topic: the pubsub topic that will be used to pass the trigger message
        :type topic : string
        :param subscription: the Pub/Sub subscription name. Do not include the
            full subscription path.
        :type subscription: str
        :param trigger_msg: the message being listened for from the pubsub topic
        :type trigger_msg: str
    """

    def __init__(
            self,
            dag,
            gcp_conn_id,
            project,
            topic,
            subscription,
            trigger_msg,
            timeout,
            max_messages=1000,
            return_immediately=True,
            ack_messages=True):
        self.dag = dag
        self.topic_project = project
        self.trigger_msg = trigger_msg
        self.gcp_conn_id = gcp_conn_id
        self.topic = topic
        self.subscription = subscription
        self.timeout = timeout
        self.max_messages = max_messages
        self.return_immediately = return_immediately
        self.ack_messages = ack_messages

    @property
    def create_subscription_task(self):
        return PubSubSubscriptionCreateOperator(
            task_id='create_subscription', topic_project=self.topic_project,
            topic=self.topic, subscription=self.subscription,
            dag=self.dag)

    @property
    def sensor_task(self):
        return SharedTopicPubSubPullSensor(
            task_id='trigger_msg_sensor',
            project=self.topic_project,
            subscription=self.subscription,
            trigger_msg=self.trigger_msg,
            max_messages=self.max_messages,
            return_immediately=self.return_immediately,
            ack_messages=self.ack_messages,
            gcp_conn_id=self.gcp_conn_id,
            topic=self.topic,
            timeout=self.timeout,
            dag=self.dag)

    # The delete subscription task is set to run no matter if the shared topic
    # pubsub sensor receives its trigger message, fails or times out.  That is because the
    # subscription needs to be cleaned up so that orphaned subscriptions don't
    # build up as alert DAGs fail or time out.
    @property
    def delete_subscription_task(self):
        return PubSubSubscriptionDeleteOperator(
            task_id='delete_subscription',
            project=self.topic_project,
            topic=self.topic, subscription=self.subscription,
            gcp_conn_id=self.gcp_conn_id,
            trigger_rule='all_done',
            dag=self.dag)
