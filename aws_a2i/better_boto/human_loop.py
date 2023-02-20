# -*- coding: utf-8 -*-

import typing as T
import json
import enum
import dataclasses
from datetime import datetime

from light_emoji import common as emojis
from iterproxy import IterProxy
from boto_session_manager import BotoSesManager

from ..helper import vprint

from .flow_definition import (
    parse_flow_definition_name_from_arn,
)

# --- Data Model
class HumanLoopStatusEnum(str, enum.Enum):
    InProgress = "InProgress"
    Failed = "Failed"
    Completed = "Completed"
    Stopped = "Stopped"
    Stopping = "Stopping"


@dataclasses.dataclass
class HumanLoop:
    creation_time: T.Optional[datetime] = dataclasses.field(default=None)
    failure_reason: T.Optional[str] = dataclasses.field(default=None)
    failure_code: T.Optional[str] = dataclasses.field(default=None)
    human_loop_status: T.Optional[str] = dataclasses.field(default=None)
    human_loop_name: T.Optional[str] = dataclasses.field(default=None)
    human_loop_arn: T.Optional[str] = dataclasses.field(default=None)
    flow_definition_arn: T.Optional[str] = dataclasses.field(default=None)
    human_loop_output_s3uri: T.Optional[str] = dataclasses.field(default=None)

    def get_details(self, bsm: BotoSesManager) -> "HumanLoop":
        """
        Call ``describe_human_loop`` API to fetch additional details.
        """
        if self.human_loop_name is not None:
            human_loop = get_human_loop_details(
                bsm=bsm,
                human_loop_name_or_arn=self.human_loop_name,
            )
        elif self.human_loop_arn is not None:
            human_loop = get_human_loop_details(
                bsm=bsm,
                human_loop_name_or_arn=self.human_loop_arn,
            )
        else:
            raise NotImplementedError
        self.creation_time = human_loop.creation_time
        self.failure_reason = human_loop.failure_reason
        self.failure_code = human_loop.failure_code
        self.human_loop_status = human_loop.human_loop_status
        self.human_loop_name = human_loop.human_loop_name
        self.human_loop_arn = human_loop.human_loop_arn
        self.flow_definition_arn = human_loop.flow_definition_arn
        self.human_loop_output_s3uri = human_loop.human_loop_output_s3uri
        return self


# --- Low level API
def parse_team_name_from_private_team_arn(arn: str) -> str:
    """
    Example:

         >>> parse_team_name_from_private_team_arn(
            "arn:aws:sagemaker:us-east-1:111122223333:workteam/private-crowd/my-workforce"
         )
         'my-workforce'
    """
    return arn.split("/")[-1]


def get_workspace_signin_url(
    bsm: BotoSesManager,
    work_team_name: str,
) -> str:
    """
    Example:

        >>> get_workspace_signin_url(bsm, "my-workforce")
        'https://1a2b3c4d5e.labeling.us-east-1.sagemaker.aws'
    """
    response = bsm.sagemaker_client.describe_workteam(WorkteamName=work_team_name)
    sub_domain = response["Workteam"]["SubDomain"]
    return "https://" + sub_domain


def get_hil_console_url(
    aws_region: str,
    flow_definition_name: str,
    hil_name: str,
) -> str:
    return (
        f"https://{aws_region}.console.aws.amazon.com/a2i/home?"
        f"region={aws_region}#/human-review-workflows/"
        f"{flow_definition_name}/human-loops/{hil_name}"
    )


def parse_hil_name_from_hil_arn(arn: str) -> str:
    """
    Example:

        >>> parse_hil_name_from_hil_arn("arn:aws:sagemaker:us-east-1:111122223333:human-loop/4d7b0711-0e9e-48c5-9df9-a03692cdcd8b")
        '4d7b0711-0e9e-48c5-9df9-a03692cdcd8b'
    """
    return arn.split("/")[-1]


def describe_human_loop(
    bsm: BotoSesManager,
    human_loop_name: str,
) -> dict:
    """
    ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client.describe_human_loop
    """
    return bsm.sagemaker_a2i_runtime_client.describe_human_loop(
        HumanLoopName=human_loop_name,
    )


def stop_human_loop(
    bsm: BotoSesManager,
    human_loop_name: str,
):
    """
    ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client.stop_human_loop
    """
    return bsm.sagemaker_a2i_runtime_client.stop_human_loop(
        HumanLoopName=human_loop_name,
    )


def delete_human_loop(
    bsm: BotoSesManager,
    human_loop_name: str,
):
    """
    ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client.delete_human_loop
    """
    return bsm.sagemaker_a2i_runtime_client.delete_human_loop(
        HumanLoopName=human_loop_name,
    )


# --- High level API
def start_human_loop(
    bsm: BotoSesManager,
    human_loop_name: str,
    flow_definition_arn: str,
    input_data: dict,
    data_attributes: T.Optional[dict] = None,
    verbose: bool = True,
) -> str:
    """
    ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client.start_human_loop

    :return: the human in loop task ARN.
    """
    vprint(
        f"{emojis.play_or_pause} Start a Human Loop Task {human_loop_name!r}", verbose
    )
    flow_definition_name = parse_flow_definition_name_from_arn(flow_definition_arn)
    hil_console_url = get_hil_console_url(
        bsm.aws_region, flow_definition_name, human_loop_name
    )
    vprint(f"  You can preview HIL status at {hil_console_url}", verbose)
    input_data["hil_name"] = human_loop_name
    input_data["hil_console_url"] = hil_console_url
    kwargs = dict(
        HumanLoopName=human_loop_name,
        FlowDefinitionArn=flow_definition_arn,
        HumanLoopInput={
            "InputContent": json.dumps(input_data),
        },
    )
    if data_attributes is not None:
        kwargs["DataAttributes"] = data_attributes
    response = bsm.sagemaker_a2i_runtime_client.start_human_loop(**kwargs)
    hil_arn = response["HumanLoopArn"]
    return hil_arn


def get_human_loop_details(
    bsm: BotoSesManager,
    human_loop_name_or_arn: str,
) -> HumanLoop:
    """
    Get human loop details.
    """
    if human_loop_name_or_arn.startswith("arn:"):
        human_loop_name_or_arn = parse_hil_name_from_hil_arn(human_loop_name_or_arn)
    response = describe_human_loop(
        bsm=bsm,
        human_loop_name=human_loop_name_or_arn,
    )
    return HumanLoop(
        creation_time=response["CreationTime"],
        failure_reason=response.get("FailureReason"),
        failure_code=response.get("FailureCode"),
        human_loop_status=response["HumanLoopStatus"],
        human_loop_name=response["HumanLoopName"],
        human_loop_arn=response["HumanLoopArn"],
        flow_definition_arn=response["FlowDefinitionArn"],
        human_loop_output_s3uri=response["HumanLoopOutput"]["OutputS3Uri"],
    )


class HumanLoopIterProxy(IterProxy[HumanLoop]):
    pass


def _list_human_loops(
    bsm: BotoSesManager,
    flow_definition_arn: str,
    creation_time_after: T.Optional[datetime] = None,
    creation_time_before: T.Optional[datetime] = None,
    ascending: bool = False,
    max_items: T.Optional[int] = 1000,
    page_size: T.Optional[int] = 100,
) -> T.Iterator[HumanLoop]:
    paginator = bsm.sagemaker_a2i_runtime_client.get_paginator("list_human_loops")
    kwargs = dict(
        FlowDefinitionArn=flow_definition_arn,
    )
    if creation_time_after is not None:
        kwargs["CreationTimeAfter"] = creation_time_after
    if creation_time_before is not None:
        kwargs["CreationTimeBefore"] = creation_time_before
    if ascending:
        kwargs["SortOrder"] = "Ascending"
    else:
        kwargs["SortOrder"] = "Descending"
    kwargs["PaginationConfig"] = dict(
        MaxItems=max_items,
        PageSize=page_size,
    )
    response_iterator = paginator.paginate(**kwargs)
    for response in response_iterator:
        for data in response["HumanLoopSummaries"]:
            yield HumanLoop(
                creation_time=data["CreationTime"],
                failure_reason=data.get("FailureReason"),
                failure_code=None,
                human_loop_status=data["HumanLoopStatus"],
                human_loop_name=data["HumanLoopName"],
                human_loop_arn=None,
                flow_definition_arn=data["FlowDefinitionArn"],
                human_loop_output_s3uri=None,
            )


def list_human_loops(
    bsm: BotoSesManager,
    flow_definition_arn: str,
    creation_time_after: T.Optional[datetime] = None,
    creation_time_before: T.Optional[datetime] = None,
    ascending: bool = False,
    max_items: T.Optional[int] = 1000,
    page_size: T.Optional[int] = 100,
) -> HumanLoopIterProxy:
    """
    List human loops. You can then call :meth:`HumanLoop.get_details()` method
    to fetch more details.

    ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-a2i-runtime.html#AugmentedAIRuntime.Client.list_human_loops
    """
    return HumanLoopIterProxy(
        iterable=_list_human_loops(
            bsm=bsm,
            flow_definition_arn=flow_definition_arn,
            creation_time_after=creation_time_after,
            creation_time_before=creation_time_before,
            ascending=ascending,
            max_items=max_items,
            page_size=page_size,
        )
    )
