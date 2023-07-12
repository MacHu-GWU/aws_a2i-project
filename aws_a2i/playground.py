# -*- coding: utf-8 -*-

import typing as T
import uuid
import dataclasses
from datetime import datetime

from boto_session_manager import BotoSesManager

from .better_boto.human_task_ui import deploy_hil_task_template
from .better_boto.human_task_ui import remove_hil_task_template
from .better_boto.flow_definition import FlowDefinition
from .better_boto.flow_definition import is_flow_definition_exists
from .better_boto.flow_definition import deploy_flow_definition
from .better_boto.flow_definition import get_flow_definition_arn
from .better_boto.flow_definition import remove_flow_definition
from .better_boto.human_loop import parse_team_name_from_private_team_arn
from .better_boto.human_loop import get_workspace_signin_url
from .better_boto.human_loop import start_human_loop
from .better_boto.human_loop import list_human_loops


@dataclasses.dataclass
class Play:
    aws_account_id: T.Optional[str] = dataclasses.field(default=None)
    aws_region: T.Optional[str] = dataclasses.field(default=None)
    task_template_name: T.Optional[str] = dataclasses.field(default=None)
    task_template_content: T.Optional[str] = dataclasses.field(default=None)
    flow_definition_name: T.Optional[str] = dataclasses.field(default=None)
    flow_execution_role_arn: T.Optional[str] = dataclasses.field(default=None)
    output_bucket: T.Optional[str] = dataclasses.field(default=None)
    output_key: T.Optional[str] = dataclasses.field(default=None)
    private_team_arn: T.Optional[str] = dataclasses.field(default=None)

    @property
    def flow_definition_arn(self) -> str:
        return get_flow_definition_arn(
            aws_account_id=self.aws_account_id,
            aws_region=self.aws_region,
            flow_definition_name=self.flow_definition_name,
        )

    def get_flow_definition(
        self,
        bsm: BotoSesManager,
    ) -> T.Optional[FlowDefinition]:
        _, flow_def = is_flow_definition_exists(
            bsm=bsm,
            flow_definition_name=self.flow_definition_name,
        )
        return flow_def

    def deploy_hil_task_template(
        self,
        bsm: BotoSesManager,
        tags: T.Optional[T.Dict[str, str]] = None,
        verbose: bool = True,
    ):
        return deploy_hil_task_template(
            bsm=bsm,
            task_template_name=self.task_template_name,
            task_template_content=self.task_template_content,
            tags=tags,
            verbose=verbose,
        )

    def deploy_flow_definition(
        self,
        bsm: BotoSesManager,
        task_description: str,
        task_count: int,
        task_availability_life_time_in_seconds: T.Optional[int] = None,
        task_time_limit_in_seconds: T.Optional[int] = None,
        tags: T.Optional[T.Dict[str, str]] = None,
        wait: bool = True,
        wait_delay: int = 3,
        wait_timeout: int = 30,
        verbose: bool = True,
    ):
        return deploy_flow_definition(
            bsm=bsm,
            flow_definition_name=self.flow_definition_name,
            flow_execution_role_arn=self.flow_execution_role_arn,
            labeling_team_arn=self.private_team_arn,
            output_bucket=self.output_bucket,
            output_key=self.output_key,
            task_template_name=self.task_template_name,
            task_description=task_description,
            task_count=task_count,
            task_availability_life_time_in_seconds=task_availability_life_time_in_seconds,
            task_time_limit_in_seconds=task_time_limit_in_seconds,
            tags=tags,
            wait=wait,
            wait_delay=wait_delay,
            wait_timeout=wait_timeout,
            verbose=verbose,
        )

    def get_workspace_signin_url(
        self,
        bsm: BotoSesManager,
    ):
        return get_workspace_signin_url(
            bsm=bsm,
            work_team_name=parse_team_name_from_private_team_arn(
                arn=self.private_team_arn
            ),
        )

    def start_human_loop(
        self,
        bsm: BotoSesManager,
        input_data: dict,
        human_loop_name: T.Optional[str] = None,
        data_attributes: T.Optional[dict] = None,
        verbose: bool = True,
    ):
        if human_loop_name is None:
            human_loop_name = str(uuid.uuid4())
        return start_human_loop(
            bsm=bsm,
            human_loop_name=human_loop_name,
            flow_definition_arn=self.flow_definition_arn,
            input_data=input_data,
            data_attributes=data_attributes,
            verbose=verbose,
        )

    def remove_flow_definition(
        self,
        bsm: BotoSesManager,
        wait: bool = True,
        wait_timeout: int = 30,
        verbose: bool = True,
    ):
        return remove_flow_definition(
            bsm=bsm,
            flow_definition_name=self.flow_definition_name,
            wait=wait,
            wait_timeout=wait_timeout,
            verbose=verbose,
        )

    def remove_hil_task_template(
        self,
        bsm: BotoSesManager,
        verbose: bool = True,
    ):
        return remove_hil_task_template(
            bsm=bsm,
            task_template_name=self.task_template_name,
            verbose=verbose,
        )

    def list_human_loops(
        self,
        bsm: BotoSesManager,
        creation_time_after: T.Optional[datetime] = None,
        creation_time_before: T.Optional[datetime] = None,
        ascending: bool = False,
        max_items: T.Optional[int] = 1000,
        page_size: T.Optional[int] = 100,
    ):
        return list_human_loops(
            bsm=bsm,
            flow_definition_arn=self.flow_definition_arn,
            creation_time_after=creation_time_after,
            creation_time_before=creation_time_before,
            ascending=ascending,
            max_items=max_items,
            page_size=page_size,
        )
