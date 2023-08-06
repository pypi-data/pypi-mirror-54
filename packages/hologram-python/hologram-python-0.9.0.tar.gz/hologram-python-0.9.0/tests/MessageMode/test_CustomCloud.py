# Author: Hologram <support@hologram.io>
#
# Copyright 2016 - Hologram (Konekt, Inc.)
#
# LICENSE: Distributed under the terms of the MIT License
#
# test_CustomCloud.py - This file implements unit tests for the CustomCloud class.

import pytest
import sys
sys.path.append(".")
sys.path.append("..")
sys.path.append("../..")
from Hologram.Authentication import *
from Hologram.CustomCloud import CustomCloud

class TestCustomCloud():

    def test_create_send(self):
        customCloud = CustomCloud(None, send_host='127.0.0.1',
                                  send_port=9999, enable_inbound=False)

        assert customCloud.send_host == '127.0.0.1'
        assert customCloud.send_port == 9999
        assert customCloud.receive_host == ''
        assert customCloud.receive_port == 0

    def test_create_receive(self):
        customCloud = CustomCloud(None, receive_host='127.0.0.1',
                                  receive_port=9999, enable_inbound=False)

        assert customCloud.send_host == ''
        assert customCloud.send_port == 0
        assert customCloud.receive_host == '127.0.0.1'
        assert customCloud.receive_port == 9999

    def test_enable_inbound(self):

        with pytest.raises(Exception, match='Must set receive host and port for inbound connection'):
            customCloud = CustomCloud(None, send_host='receive.com',
                                      send_port=9999, enable_inbound=True)

    def test_invalid_send_host_and_port(self):
        customCloud = CustomCloud(None, receive_host='receive.com', receive_port=9999)

        with pytest.raises(Exception, match = 'Send host and port must be set before making this operation'):
            customCloud.sendMessage("hello")

    def test_invalid_send_sms(self):
        customCloud = CustomCloud(None, 'test.com', 9999)

        temp = "hello"
        with pytest.raises(NotImplementedError, match='Cannot send SMS via custom cloud'):
            customCloud.sendSMS('+1234567890', temp)
