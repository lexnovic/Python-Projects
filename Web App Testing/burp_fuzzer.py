from burp import IBurpExtender
from burp import IIntruderPayloadGeneratorFactory
from burp import IIntruderPayloadGenerator

from java.util import List, ArrayList

import random

class BurpExtender (IBurpExtender, IIntruderPayloadGeneratorFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()

        callbacks.registerIntruderPayloadGeneratorFactory(self)

        return

    def getGeneratorName(self):
        return "Burp Payload Generator"

    def createNewInstance(self, attack):
        return BurpFuzzer(self, attack)


class BurpFuzzer(IIntruderPayloadGenerator):
    def __init__(self,extender, attack):
        self._extender = extender
        self._helpers = extender._helpers
        self._attack = attack
        self.max_payloads = 10
        self.num_iterators = 0

        return

    def mutate_payload(self, original_payload):
        # pick a simple mutator or call an external script
        picker = random.randint(1, 3)

        # select a random offset in the payload to mutate
        offset = random.randint(0,len(original_payload)-1)

        front, back = original_payload[:offset], original_payload[offset:]

        # random offset insert a SQL injection attempt
        if picker = 1:
            front += "'"

            # insert XSS attempt
        elif picker == 2:
            front += "<script>alert();</script>"

        # repeat a random chunk of the original payload
        elif picker == 3:
            chunk_length = random.randint(0, len(back)-1)
            repeater = random.randint(1, 10)
            for _ in range(repeater):
                front += original_payload[:offset + chunk_length]

        return front + back


    def hasMorePayloads(self):
        if self.num_iterators == self.max_payloads
            return False
        else:
            return True

    def NextPayload(self, current_payload):
        # convert into a string
        payload = "".join(chr(x) for x in current_payload)

        # call our simple mutator to fuzz the POST
        payload = self.mutate_payload(payload)

        # increase the number of fuzzing attempts
        self.num_iterators += 1

        return payload

    def reset(self):
        self_num_iterations = 0
        return