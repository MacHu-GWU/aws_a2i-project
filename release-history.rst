.. _release_history:

Release and Version History
==============================================================================


Backlog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.3.1 (2023-07-11)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- move all public api from ``aws_a2i`` to ``aws_a2i.api``, so the new way to import is ``from aws_api import api as aws_api``
- now the list of public APIs are:
    - ``aws_a2i.api.get_task_template_arn``
    - ``aws_a2i.api.get_task_template_console_url``
    - ``aws_a2i.api.parse_task_template_name_from_arn``
    - ``aws_a2i.api.is_hil_task_template_exists``
    - ``aws_a2i.api.create_human_task_ui``
    - ``aws_a2i.api.delete_human_task_ui``
    - ``aws_a2i.api.deploy_hil_task_template``
    - ``aws_a2i.api.remove_hil_task_template``
    - ``aws_a2i.api.FlowDefinitionStatusEnum``
    - ``aws_a2i.api.FlowDefinition``
    - ``aws_a2i.api.get_flow_definition_arn``
    - ``aws_a2i.api.get_flow_definition_console_url``
    - ``aws_a2i.api.parse_flow_definition_name_from_arn``
    - ``aws_a2i.api.is_flow_definition_exists``
    - ``aws_a2i.api.create_flow_definition``
    - ``aws_a2i.api.delete_flow_definition``
    - ``aws_a2i.api.remove_flow_definition``
    - ``aws_a2i.api.deploy_flow_definition``
    - ``aws_a2i.api.HumanAnswer``
    - ``aws_a2i.api.HumanLoopOutput``
    - ``aws_a2i.api.HumanLoopStatusEnum``
    - ``aws_a2i.api.HumanLoop``
    - ``aws_a2i.api.parse_team_name_from_private_team_arn``
    - ``aws_a2i.api.get_workspace_signin_url``
    - ``aws_a2i.api.get_hil_console_url``
    - ``aws_a2i.api.parse_hil_name_from_hil_arn``
    - ``aws_a2i.api.describe_human_loop``
    - ``aws_a2i.api.start_human_loop``
    - ``aws_a2i.api.get_human_loop_details``
    - ``aws_a2i.api.stop_human_loop``
    - ``aws_a2i.api.delete_human_loop``
    - ``aws_a2i.api.list_human_loops``
    - ``aws_a2i.api.render_task_template``
    - ``aws_a2i.api.to_tag_list``
    - ``aws_a2i.api.to_tag_dict``
    - ``aws_a2i.api.sha256_of_bytes``
    - ``aws_a2i.api.vprint``
    - ``aws_a2i.api.Play``
- Add a centralized human review workflow related resources manager ``Play``
- Add ``HumanLoopOutput`` and ``HumanAnswer`` to represent the output of human review workflow

**Miscellaneous**

- Bump ``boto_session_manager`` dependencies to 1.5.4+ to fit the new augmented ai client attribute name.


0.2.1 (2023-02-20)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add the following public APIs:
    - ``aws_a2i.FlowDefinitionStatusEnum``
    - ``aws_a2i.FlowDefinition``
    - ``aws_a2i.HumanLoopStatusEnum``
    - ``aws_a2i.HumanLoop``
    - ``aws_a2i.get_human_loop_details``
    - ``aws_a2i.stop_human_loop``
    - ``aws_a2i.delete_human_loop``
    - ``aws_a2i.list_human_loops``

**Bugfixes**

- Fix a bug that deploy human review workflow definition not happen when the s3 output is changed.


0.1.1 (2023-02-17)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release
- Add the following public APIs:
    - ``aws_a2i.get_task_template_arn``
    - ``aws_a2i.get_task_template_console_url``
    - ``aws_a2i.parse_task_template_name_from_arn``
    - ``aws_a2i.is_hil_task_template_exists``
    - ``aws_a2i.create_human_task_ui``
    - ``aws_a2i.delete_human_task_ui``
    - ``aws_a2i.deploy_hil_task_template``
    - ``aws_a2i.remove_hil_task_template``
    - ``aws_a2i.get_flow_definition_arn``
    - ``aws_a2i.get_flow_definition_console_url``
    - ``aws_a2i.parse_flow_definition_name_from_arn``
    - ``aws_a2i.is_flow_definition_exists``
    - ``aws_a2i.create_flow_definition``
    - ``aws_a2i.delete_flow_definition``
    - ``aws_a2i.remove_flow_definition``
    - ``aws_a2i.deploy_flow_definition``
    - ``aws_a2i.parse_team_name_from_private_team_arn``
    - ``aws_a2i.get_workspace_signin_url``
    - ``aws_a2i.get_hil_console_url``
    - ``aws_a2i.parse_hil_name_from_hil_arn``
    - ``aws_a2i.describe_human_loop``
    - ``aws_a2i.start_human_loop``
    - ``aws_a2i.render_task_template``
    - ``aws_a2i.to_tag_list``
    - ``aws_a2i.to_tag_dict``
    - ``aws_a2i.sha256_of_bytes``
    - ``aws_a2i.vprint``
