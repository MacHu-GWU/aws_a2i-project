# -*- coding: utf-8 -*-

import typing as T
import json

from boto_session_manager import BotoSesManager

from ..helper import vprint

from .flow_definition import (
    parse_flow_definition_name_from_arn,
)


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
    vprint(f"▶️ Start a Human Loop Task {human_loop_name!r}", verbose)
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
