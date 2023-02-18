# -*- coding: utf-8 -*-

import typing as T

from boto_session_manager import BotoSesManager

from ..tagging import to_tag_list
from ..helper import sha256_of_bytes, vprint
from ..waiter import Waiter

from .human_task_ui import (
    get_task_template_arn,
)


def get_flow_definition_arn(
    aws_account_id: str,
    aws_region: str,
    flow_definition_name: str,
) -> str:
    return (
        f"arn:aws:sagemaker:{aws_region}:{aws_account_id}:flow-definition"
        f"/{flow_definition_name}"
    )


def get_flow_definition_console_url(
    aws_region: str,
    flow_definition_name: str,
) -> str:
    return (
        f"https://console.aws.amazon.com/a2i/home?region={aws_region}#"
        f"/human-review-workflows/{flow_definition_name}"
    )


def parse_flow_definition_name_from_arn(arn: str) -> str:
    """
    Example:

        >>> parse_flow_definition_name_from_arn("arn:aws:sagemaker:us-east-1:111122223333:flow-definition/my-flow")
        'my-flow'
    """
    return arn.split("/")[-1]


def is_flow_definition_exists(
    bsm: BotoSesManager,
    flow_definition_name: str,
) -> T.Tuple[bool, dict]:
    """
    ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.describe_flow_definition

    :return: tuple of two item, first item is a boolean value, second value is
        the response of ``describe_flow_definition()``, you can call it flow details.
    """
    try:
        response = bsm.sagemaker_client.describe_flow_definition(
            FlowDefinitionName=flow_definition_name
        )
        return True, response
    except Exception as e:
        if "does not exist" in str(e):
            return False, {}
        else:
            raise e


def create_flow_definition(
    bsm: BotoSesManager,
    flow_definition_name: str,
    flow_execution_role_arn: str,
    labeling_team_arn: str,
    output_bucket: str,
    output_key: str,
    task_template_name: str,
    task_description: str,
    task_count: int,
    task_time_limit_in_seconds: T.Optional[int] = None,
    task_availability_life_time_in_seconds: T.Optional[int] = None,
    tags: T.Optional[T.Dict[str, str]] = None,
) -> dict:
    """
    ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.create_flow_definition
    """
    task_template_arn = get_task_template_arn(
        aws_account_id=bsm.aws_account_id,
        aws_region=bsm.aws_region,
        task_template_name=task_template_name,
    )
    if output_key.endswith("/"):
        output_key = output_key[:-1]
    human_loop_config = {
        "WorkteamArn": labeling_team_arn,
        "HumanTaskUiArn": task_template_arn,
        "TaskTitle": task_template_name,
        "TaskDescription": task_description,
        "TaskCount": task_count,
    }
    if task_availability_life_time_in_seconds is not None:
        human_loop_config[
            "TaskAvailabilityLifetimeInSeconds"
        ] = task_availability_life_time_in_seconds
    if task_time_limit_in_seconds is not None:
        human_loop_config["TaskTimeLimitInSeconds"] = task_time_limit_in_seconds
    kwargs = dict(
        FlowDefinitionName=flow_definition_name,
        HumanLoopConfig=human_loop_config,
        OutputConfig={
            "S3OutputPath": f"s3://{output_bucket}/{output_key}",
        },
        RoleArn=flow_execution_role_arn,
    )
    if tags:
        kwargs["Tags"] = to_tag_list(tags)
    response = bsm.sagemaker_client.create_flow_definition(**kwargs)
    return response


def delete_flow_definition(
    bsm: BotoSesManager,
    flow_definition_name: str,
):
    """
    ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.delete_flow_definition
    """
    return bsm.sagemaker_client.delete_flow_definition(
        FlowDefinitionName=flow_definition_name
    )


def remove_flow_definition(
    bsm: BotoSesManager,
    flow_definition_name: str,
    wait: bool = True,
    verbose: bool = True,
):
    vprint(
        "📋 Remove Human review workflow definition, it may takes 30 sec ~ 1 minute",
        verbose,
    )
    flow_definition_console_url = get_flow_definition_console_url(
        bsm.aws_region,
        flow_definition_name,
    )
    vprint(f"  Preview at {flow_definition_console_url}", verbose)

    is_flow_exists, flow_details = is_flow_definition_exists(
        bsm=bsm,
        flow_definition_name=flow_definition_name,
    )
    if is_flow_exists:
        delete_flow_definition(
            bsm=bsm,
            flow_definition_name=flow_definition_name,
        )
        if wait:
            for _ in Waiter(delays=1, timeout=30, indent=2, verbose=verbose):
                is_flow_exists, flow_details = is_flow_definition_exists(
                    bsm=bsm,
                    flow_definition_name=flow_definition_name,
                )
                if is_flow_exists is False:
                    break
                if flow_details["FlowDefinitionStatus"] == "Failed":
                    raise Exception("Failed!")
    else:
        vprint("  Flow definition doesn't exists, do nothing.", verbose)
    vprint(f"  ✅ Successfully delete flow definition {flow_definition_name!r}", verbose)


def deploy_flow_definition(
    bsm: BotoSesManager,
    flow_definition_name: str,
    flow_execution_role_arn: str,
    labeling_team_arn: str,
    output_bucket: str,
    output_key: str,
    task_template_name: str,
    task_description: str,
    task_count: int,
    task_time_limit_in_seconds: T.Optional[int] = None,
    task_availability_life_time_in_seconds: T.Optional[int] = None,
    tags: T.Optional[T.Dict[str, str]] = None,
    wait: bool = True,
    verbose: bool = True,
):
    """
    Deploy a Human in Loop workflow. in smart way.
    """
    vprint(
        "📋 Deploy Human review workflow definition, it may takes 30 sec ~ 1 minute",
        verbose,
    )
    flow_definition_console_url = get_flow_definition_console_url(
        aws_region=bsm.aws_region,
        flow_definition_name=flow_definition_name,
    )
    vprint(f"  preview at {flow_definition_console_url}", verbose)
    is_flow_exists, flow_response = is_flow_definition_exists(
        bsm=bsm,
        flow_definition_name=flow_definition_name,
    )
    if is_flow_exists:
        flag = (
            (flow_execution_role_arn == flow_response["RoleArn"])
            and (task_template_name == flow_response["HumanLoopConfig"]["TaskTitle"])
            and (task_count == flow_response["HumanLoopConfig"]["TaskCount"])
        )
        if task_availability_life_time_in_seconds is not None:
            flag = flag and (
                task_availability_life_time_in_seconds
                == flow_response["HumanLoopConfig"]["TaskAvailabilityLifetimeInSeconds"]
            )
        if task_time_limit_in_seconds is not None:
            flag = flag and (
                task_time_limit_in_seconds
                == flow_response["HumanLoopConfig"]["TaskTimeLimitInSeconds"]
            )
        # no need to deploy
        if flag:
            vprint("  No configuration changed, do nothing.", verbose)
            return
        # remove existing one first
        remove_flow_definition(
            bsm=bsm,
            flow_definition_name=flow_definition_name,
            wait=True,
            verbose=verbose,
        )
    vprint("📋 Create Human review workflow definition ...", verbose)
    create_flow_definition(
        bsm,
        flow_definition_name=flow_definition_name,
        flow_execution_role_arn=flow_execution_role_arn,
        labeling_team_arn=labeling_team_arn,
        output_bucket=output_bucket,
        output_key=output_key,
        task_template_name=task_template_name,
        task_description=task_description,
        task_count=task_count,
        task_time_limit_in_seconds=task_time_limit_in_seconds,
        task_availability_life_time_in_seconds=task_availability_life_time_in_seconds,
        tags=tags,
    )

    if wait:
        for _ in Waiter(delays=1, timeout=30, indent=2, verbose=verbose):
            is_flow_exists, flow_details = is_flow_definition_exists(
                bsm=bsm,
                flow_definition_name=flow_definition_name,
            )
            if is_flow_exists is False:
                break
            if flow_details["FlowDefinitionStatus"] == "Active":
                break
            if flow_details["FlowDefinitionStatus"] == "Failed":
                raise Exception("Failed")

    vprint(
        f"  ✅ Successfully deployed flow definition {flow_definition_name!r}", verbose
    )
