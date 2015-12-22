import logging

import controller
import steps


class PreProcessor(controller.AbstractController):

    """
    Preprocesses incoming messages. This class is responsible for message
    transfer to processor
    """

    def __init__(self, processor):
        super(PreProcessor, self).__init__()
        self.log = logging.getLogger(__name__)
        self._processor = processor
        self._steps = [
            steps.ValidateMessageMiddleware(),
            steps.CreateMessageMiddleware()
        ]

    @property
    def processor(self):
        return self._processor

    def process(self, amqp_message):
        """
        PreProcesses incoming message

        :param amqp_message: AMPQ message
        :type amqp_message: messages.AMQPMEssage
        :return: response object ot None
        :rtype: Response, Error or None
        """
        msg = amqp_message
        all_controllers = self._steps
        for step in all_controllers:
            msg = step.process(msg)
        self._processor.process(msg)
