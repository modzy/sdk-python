# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from modzy.edge.proto.accounting.v1 import accounting_pb2 as protos_dot_modzy_dot_accounting_dot_v1_dot_accounting__pb2
from modzy.edge.proto.jobs.v1 import jobs_pb2 as protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2


class JobServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SubmitJob = channel.unary_unary(
                '/jobs.v1.JobService/SubmitJob',
                request_serializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobSubmission.SerializeToString,
                response_deserializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobSubmissionReceipt.FromString,
                )
        self.GetJobs = channel.unary_unary(
                '/jobs.v1.JobService/GetJobs',
                request_serializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobFilter.SerializeToString,
                response_deserializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobSummaryList.FromString,
                )
        self.GetJob = channel.unary_unary(
                '/jobs.v1.JobService/GetJob',
                request_serializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobIdentifier.SerializeToString,
                response_deserializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobDetails.FromString,
                )
        self.GetFeatures = channel.unary_unary(
                '/jobs.v1.JobService/GetFeatures',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobFeatures.FromString,
                )
        self.GetStatistics = channel.unary_unary(
                '/jobs.v1.JobService/GetStatistics',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobStatisticsList.FromString,
                )
        self.GetStatisticsForAccessKey = channel.unary_unary(
                '/jobs.v1.JobService/GetStatisticsForAccessKey',
                request_serializer=protos_dot_modzy_dot_accounting_dot_v1_dot_accounting__pb2.APIKeyIdentifier.SerializeToString,
                response_deserializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobStatistics.FromString,
                )
        self.CancelJob = channel.unary_unary(
                '/jobs.v1.JobService/CancelJob',
                request_serializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobIdentifier.SerializeToString,
                response_deserializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobDetails.FromString,
                )
        self.CancelAllJobs = channel.unary_unary(
                '/jobs.v1.JobService/CancelAllJobs',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobDetailsList.FromString,
                )
        self.GetJobHistory = channel.unary_unary(
                '/jobs.v1.JobService/GetJobHistory',
                request_serializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobHistoryFilter.SerializeToString,
                response_deserializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobDetailsList.FromString,
                )
        self.GetHistoryForJob = channel.unary_unary(
                '/jobs.v1.JobService/GetHistoryForJob',
                request_serializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobIdentifier.SerializeToString,
                response_deserializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobDetailsList.FromString,
                )
        self.CloseJob = channel.unary_unary(
                '/jobs.v1.JobService/CloseJob',
                request_serializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobIdentifier.SerializeToString,
                response_deserializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobSubmissionReceipt.FromString,
                )
        self.AddInputToJob = channel.unary_unary(
                '/jobs.v1.JobService/AddInputToJob',
                request_serializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.AppendableJobInput.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
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

    def GetFeatures(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetStatistics(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetStatisticsForAccessKey(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CancelJob(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CancelAllJobs(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetJobHistory(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetHistoryForJob(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CloseJob(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddInputToJob(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_JobServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SubmitJob': grpc.unary_unary_rpc_method_handler(
                    servicer.SubmitJob,
                    request_deserializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobSubmission.FromString,
                    response_serializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobSubmissionReceipt.SerializeToString,
            ),
            'GetJobs': grpc.unary_unary_rpc_method_handler(
                    servicer.GetJobs,
                    request_deserializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobFilter.FromString,
                    response_serializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobSummaryList.SerializeToString,
            ),
            'GetJob': grpc.unary_unary_rpc_method_handler(
                    servicer.GetJob,
                    request_deserializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobIdentifier.FromString,
                    response_serializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobDetails.SerializeToString,
            ),
            'GetFeatures': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFeatures,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobFeatures.SerializeToString,
            ),
            'GetStatistics': grpc.unary_unary_rpc_method_handler(
                    servicer.GetStatistics,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobStatisticsList.SerializeToString,
            ),
            'GetStatisticsForAccessKey': grpc.unary_unary_rpc_method_handler(
                    servicer.GetStatisticsForAccessKey,
                    request_deserializer=protos_dot_modzy_dot_accounting_dot_v1_dot_accounting__pb2.APIKeyIdentifier.FromString,
                    response_serializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobStatistics.SerializeToString,
            ),
            'CancelJob': grpc.unary_unary_rpc_method_handler(
                    servicer.CancelJob,
                    request_deserializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobIdentifier.FromString,
                    response_serializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobDetails.SerializeToString,
            ),
            'CancelAllJobs': grpc.unary_unary_rpc_method_handler(
                    servicer.CancelAllJobs,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobDetailsList.SerializeToString,
            ),
            'GetJobHistory': grpc.unary_unary_rpc_method_handler(
                    servicer.GetJobHistory,
                    request_deserializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobHistoryFilter.FromString,
                    response_serializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobDetailsList.SerializeToString,
            ),
            'GetHistoryForJob': grpc.unary_unary_rpc_method_handler(
                    servicer.GetHistoryForJob,
                    request_deserializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobIdentifier.FromString,
                    response_serializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobDetailsList.SerializeToString,
            ),
            'CloseJob': grpc.unary_unary_rpc_method_handler(
                    servicer.CloseJob,
                    request_deserializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobIdentifier.FromString,
                    response_serializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobSubmissionReceipt.SerializeToString,
            ),
            'AddInputToJob': grpc.unary_unary_rpc_method_handler(
                    servicer.AddInputToJob,
                    request_deserializer=protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.AppendableJobInput.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
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
            protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobSubmission.SerializeToString,
            protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobSubmissionReceipt.FromString,
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
            protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobFilter.SerializeToString,
            protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobSummaryList.FromString,
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
            protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobIdentifier.SerializeToString,
            protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobDetails.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFeatures(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jobs.v1.JobService/GetFeatures',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobFeatures.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetStatistics(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jobs.v1.JobService/GetStatistics',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobStatisticsList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetStatisticsForAccessKey(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jobs.v1.JobService/GetStatisticsForAccessKey',
            protos_dot_modzy_dot_accounting_dot_v1_dot_accounting__pb2.APIKeyIdentifier.SerializeToString,
            protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobStatistics.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CancelJob(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jobs.v1.JobService/CancelJob',
            protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobIdentifier.SerializeToString,
            protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobDetails.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CancelAllJobs(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jobs.v1.JobService/CancelAllJobs',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobDetailsList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetJobHistory(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jobs.v1.JobService/GetJobHistory',
            protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobHistoryFilter.SerializeToString,
            protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobDetailsList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetHistoryForJob(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jobs.v1.JobService/GetHistoryForJob',
            protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobIdentifier.SerializeToString,
            protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobDetailsList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CloseJob(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jobs.v1.JobService/CloseJob',
            protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobIdentifier.SerializeToString,
            protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.JobSubmissionReceipt.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddInputToJob(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jobs.v1.JobService/AddInputToJob',
            protos_dot_modzy_dot_jobs_dot_v1_dot_jobs__pb2.AppendableJobInput.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
