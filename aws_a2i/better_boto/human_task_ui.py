# -*- coding: utf-8 -*-

import typing as T

from light_emoji import common as emojis
from boto_session_manager import BotoSesManager

from ..helper import sha256_of_bytes, vprint
from ..tagging import to_tag_list


# --- Low level API
def get_task_template_arn(
    aws_account_id: str,
    aws_region: str,
    task_template_name: str,
) -> str:
    return (
        f"arn:aws:sagemaker:{aws_region}:{aws_account_id}:human-task-ui"
        f"/{task_template_name}"
    )


def get_task_template_console_url(
    aws_region: str,
    task_template_name: str,
) -> str:
    return (
        f"https://{aws_region}.console.aws.amazon.com/sagemaker"
        f"/groundtruth?region={aws_region}#/a2i/worker-task-templates"
        f"/{task_template_name}"
    )


def parse_task_template_name_from_arn(arn: str) -> str:
    """
    Example:

        >>> parse_task_template_name_from_arn("arn:aws:sagemaker:us-east-1:111122223333:human-task-ui/my-task-template")
        'my-task-template'
    """
    return arn.split("/")[-1]


def is_hil_task_template_exists(
    bsm: BotoSesManager,
    task_template_name: str,
) -> T.Tuple[bool, dict]:
    """
    Reference:

    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.describe_human_task_ui

    :return: tuple of two item, first item is a boolean value, second value is
        the response of ``describe_human_task_ui()``, you can call it task ui details.
    """
    try:
        response = bsm.sagemaker_client.describe_human_task_ui(
            HumanTaskUiName=task_template_name,
        )
        return True, response
    except Exception as e:
        if "does not exist" in str(e):
            return False, {}
        else:
            raise e


def create_human_task_ui(
    bsm: BotoSesManager,
    task_template_name: str,
    task_template_content: str,
    tags: T.Optional[T.Dict[str, str]] = None,
) -> dict:
    """
    ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.create_human_task_ui
    """
    kwargs = dict(
        HumanTaskUiName=task_template_name,
        UiTemplate={"Content": task_template_content},
    )
    if tags:
        kwargs["Tags"] = to_tag_list(tags)
    return bsm.sagemaker_client.create_human_task_ui(**kwargs)


def delete_human_task_ui(
    bsm: BotoSesManager,
    task_template_name: str,
):
    """
    Reference:

    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html#SageMaker.Client.delete_human_task_ui
    """
    return bsm.sagemaker_client.delete_human_task_ui(HumanTaskUiName=task_template_name)


# --- High level API
def deploy_hil_task_template(
    bsm: BotoSesManager,
    task_template_name: str,
    task_template_content: str,
    tags: T.Optional[T.Dict[str, str]] = None,
    verbose: bool = True,
) -> T.Optional[dict]:
    """
    Deploy HIL task template, smartly.

    :return: if deployment happens, then return the response of ``create_human_task_ui()``,
        otherwise return ``None``.
    """
    vprint(f"{emojis.deploy} Deploy Human in Loop task template", verbose)
    task_template_console_url = get_task_template_console_url(
        aws_region=bsm.aws_region,
        task_template_name=task_template_name,
    )
    vprint(f"  preview at {task_template_console_url}", verbose)
    flag, response = is_hil_task_template_exists(
        bsm=bsm,
        task_template_name=task_template_name,
    )
    if flag:
        content_sha256 = response["UiTemplate"]["ContentSha256"]
        if content_sha256 == sha256_of_bytes(task_template_content.encode("utf-8")):
            vprint(
                "  a HIL task template with the same content already exists, do nothing.",
                verbose,
            )
            return None
        else:
            delete_human_task_ui(
                bsm=bsm,
                task_template_name=task_template_name,
            )
            response = create_human_task_ui(
                bsm=bsm,
                task_template_name=task_template_name,
                task_template_content=task_template_content,
                tags=tags,
            )
    else:
        response = create_human_task_ui(
            bsm, task_template_name, task_template_content, tags
        )
    vprint(
        f"  {emojis.succeeded} Successfully deployed task ui template {task_template_name!r}",
        verbose,
    )
    return response


def remove_hil_task_template(
    bsm: BotoSesManager,
    task_template_name: str,
    verbose: bool = True,
) -> bool:
    """
    Remove HIL task template, smartly.

    :return: a boolean flag indicating whether the delete operation happens.
    """
    vprint(f"{emojis.delete} Remove Human in Loop task template", verbose)
    task_template_console_url = get_task_template_console_url(
        aws_region=bsm.aws_region,
        task_template_name=task_template_name,
    )
    vprint(f"  verify at {task_template_console_url}", verbose)
    flag, response = is_hil_task_template_exists(
        bsm=bsm,
        task_template_name=task_template_name,
    )
    if flag:
        delete_human_task_ui(
            bsm=bsm,
            task_template_name=task_template_name,
        )
    else:
        vprint("  HIL task template doesn't exists, do nothing.", verbose)

    vprint(
        f"  {emojis.succeeded} Successfully removed task ui template {task_template_name!r}",
        verbose,
    )
    return not flag
