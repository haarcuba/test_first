import pytest
import socket
from testix.frequentlyused import *
from testix import patch_module
from chatbot import chatbot

class TestChatbot:
    @pytest.fixture(autouse=True)
    def globals_patch(self, patch_module):
        patch_module( chatbot, 'responder' )

    def construct(self):
        with Scenario() as s:
            s.responder.Responder() >> FakeObject( 'responder_' )
            self.tested = chatbot.Chatbot( FakeObject( 'sock' ) )

    def test_construction(self):
        self.construct()

    def test_request_response_loop(self):
        self.construct()
        class EndTestException(Exception): pass
        with Scenario() as s:
            for i in range(10):
                s.sock.recv(4096)                     >> f'request {i}'
                s.responder_.process(f'request {i}')    >> f'response {i}'
                s.sock.send(f'response {i}')

            s.sock.recv(4096).throwing(EndTestException)
            with pytest.raises(EndTestException):
                self.tested.go()

    def test_request_response_loop_survives_a_recv_exception(self):
        self.construct()
        class EndTestException(Exception): pass
        with Scenario() as s:
            for i in range(10):
                s.sock.recv(4096)                     >> f'request {i}'
                s.responder_.process(f'request {i}')    >> f'response {i}'
                s.sock.send(f'response {i}')

            s.sock.recv(4096).throwing(socket.error)

            for i in range(10):
                s.sock.recv(4096)                     >> f'request {i}'
                s.responder_.process(f'request {i}')    >> f'response {i}'
                s.sock.send(f'response {i}')

            s.sock.recv(4096).throwing(EndTestException)
            with pytest.raises(EndTestException):
                self.tested.go()