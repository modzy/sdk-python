# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from modzy.edge.proto.jobs.v1 import job_pb2 as jobs_dot_v1_dot_job__pb2


class JobServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SubmitJob = channel.unary_unary(
                '/jobs.v1.JobService/SubmitJob',
                request_serializer=jobs_dot_v1_dot_job__pb2.JobSubmission.SerializeToString,
                response_deserializer=jobs_dot_v1_dot_job__pb2.JobSubmissionReceipt.FromString,
                )
        self.GetJobs = channel.unary_unary(
                '/jobs.v1.JobService/GetJobs',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=jobs_dot_v1_dot_job__pb2.GetJobsListResponse.FromString,
                )
        self.GetJob = channel.unary_unary(
                '/jobs.v1.JobService/GetJob',
                request_serializer=jobs_dot_v1_dot_job__pb2.JobIdentifier.SerializeToString,
                response_deserializer=jobs_dot_v1_dot_job__pb2.JobDetailsResponse.FromString,
                )


class JobServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SubmitJob(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetJobs(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetJob(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_JobServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SubmitJob': grpc.unary_unary_rpc_method_handler(
                    servicer.SubmitJob,
                    request_deserializer=jobs_dot_v1_dot_job__pb2.JobSubmission.FromString,
                    response_serializer=jobs_dot_v1_dot_job__pb2.JobSubmissionReceipt.SerializeToString,
            ),
            'GetJobs': grpc.unary_unary_rpc_method_handler(
                    servicer.GetJobs,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=jobs_dot_v1_dot_job__pb2.GetJobsListResponse.SerializeToString,
            ),
            'GetJob': grpc.unary_unary_rpc_method_handler(
                    servicer.GetJob,
                    request_deserializer=jobs_dot_v1_dot_job__pb2.JobIdentifier.FromString,
                    response_serializer=jobs_dot_v1_dot_job__pb2.JobDetailsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'jobs.v1.JobService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class JobService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SubmitJob(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jobs.v1.JobService/SubmitJob',
            jobs_dot_v1_dot_job__pb2.JobSubmission.SerializeToString,
            jobs_dot_v1_dot_job__pb2.JobSubmissionReceipt.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetJobs(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jobs.v1.JobService/GetJobs',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            jobs_dot_v1_dot_job__pb2.GetJobsListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetJob(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jobs.v1.JobService/GetJob',
            jobs_dot_v1_dot_job__pb2.JobIdentifier.SerializeToString,
            jobs_dot_v1_dot_job__pb2.JobDetailsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)