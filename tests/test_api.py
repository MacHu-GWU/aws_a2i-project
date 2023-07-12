# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx


def test():
    from aws_a2i import api

    _ = api.get_task_template_arn
    _ = api.get_task_template_console_url
    _ = api.parse_task_template_name_from_arn
    _ = api.is_hil_task_template_exists
    _ = api.create_human_task_ui
    _ = api.delete_human_task_ui
    _ = api.deploy_hil_task_template
    _ = api.remove_hil_task_template
    _ = api.FlowDefinitionStatusEnum
    _ = api.FlowDefinition
    _ = api.get_flow_definition_arn
    _ = api.get_flow_definition_console_url
    _ = api.parse_flow_definition_name_from_arn
    _ = api.is_flow_definition_exists
    _ = api.create_flow_definition
    _ = api.delete_flow_definition
    _ = api.remove_flow_definition
    _ = api.deploy_flow_definition
    _ = api.HumanAnswer
    _ = api.HumanLoopOutput
    _ = api.HumanLoopStatusEnum
    _ = api.HumanLoop
    _ = api.parse_team_name_from_private_team_arn
    _ = api.get_workspace_signin_url
    _ = api.get_hil_console_url
    _ = api.parse_hil_name_from_hil_arn
    _ = api.describe_human_loop
    _ = api.start_human_loop
    _ = api.get_human_loop_details
    _ = api.stop_human_loop
    _ = api.delete_human_loop
    _ = api.list_human_loops
    _ = api.render_task_template
    _ = api.to_tag_list
    _ = api.to_tag_dict
    _ = api.sha256_of_bytes
    _ = api.vprint
    _ = api.Play


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
