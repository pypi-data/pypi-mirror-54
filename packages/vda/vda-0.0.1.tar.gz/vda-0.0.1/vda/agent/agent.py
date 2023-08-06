from concurrent import futures
import logging

import grpc

from vda.grpc import agent_pb2, agent_pb2_grpc

logger = logging.getLogger(__name__)


class AgentClient:

    def __init__(self, address, port, timeout):
        self.addr_port = "{address}:{port}".format(
            address=address, port=port)
        self.channel = grpc.insecure_channel(self.addr_port)
        self.stub = agent_pb2_grpc.AgentStub(self.channel)
        self.timeout = timeout

    def sync_call(self, seq, body):
        request = agent_pb2.ConfRequest(seq=seq, body=body)
        logger.info("agent sync request: %s %s", self.addr_port, request)
        reply = self.stub.Configure(request, self.timeout)
        logger.info("agent sync reply: %s", reply)
        return reply

    def async_call(self, seq, body, callback):
        request = agent_pb2.ConfRequest(seq=seq, body=body)
        logger.info("agent async request: %s %s", self.addr_port, request)

        def _callback(call_future):
            logger.info("agent async reply: %s", call_future.result())
            callback(call_future)

        call_future = self.stub.Configure.future(request)
        call_future.add_done_callback(_callback)

    def close(self):
        self.channel.close()


class AgentServicer(agent_pb2_grpc.AgentServicer):

    def __init__(self, configure_handler):
        self.configure_handler = configure_handler

    def Configure(self, request, context):
        logger.info("request: %s\ncontext: %s", request, context)
        event = self.configure_handler(request.seq, request.body)
        reply = agent_pb2.ConfReply(event=event)
        logger.info("reply: %s", reply)
        return reply


def launch_server(address, port, max_workers, configure_handler):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    agent_pb2_grpc.add_AgentServicer_to_server(
        AgentServicer(configure_handler), server)
    addr_port = "{address}:{port}".format(address=address, port=port)
    server.add_insecure_port(addr_port)
    server.start()
    server.wait_for_termination()
