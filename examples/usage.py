# -*- coding: utf-8 -*-

import os
import uuid
from pathlib import Path

from rich import print as rprint
from boto_session_manager import BotoSesManager

import aws_a2i

# ------------------------------------------------------------------------------
bsm = BotoSesManager(profile_name="aws_data_lab_sanhe_us_east_2")

# dir_here = Path(os.getcwd()).absolute() # for jupyter notebook
dir_here = Path(__file__).absolute().parent  # for python script

path_task_template = dir_here.parent.joinpath("task-ui.liquid")

private_team_arn = (
    "arn:aws:sagemaker:us-east-2:669508176277:workteam/private-crowd/my-labeling-team"
)
task_template_name = "aws-a2i-example"
flow_definition_name = "aws-a2i-example"
flow_execution_role_arn = "arn:aws:iam::669508176277:role/a2i_poc-a2i_execution_role"
output_bucket = "669508176277-us-east-2-a2i-poc"
output_key = "poc/aws_a2i/hil-output/"

flow_definition_arn = aws_a2i.get_flow_definition_arn(
    aws_account_id=bsm.aws_account_id,
    aws_region=bsm.aws_region,
    flow_definition_name=flow_definition_name,
)

# ------------------------------------------------------------------------------
# aws_a2i.remove_hil_task_template(bsm=bsm, task_template_name=task_template_name)
# aws_a2i.remove_flow_definition(bsm=bsm, flow_definition_name=flow_definition_name)


# ------------------------------------------------------------------------------
# aws_a2i.deploy_hil_task_template(
#     bsm=bsm,
#     task_template_name=task_template_name,
#     task_template_content=path_task_template.read_text(),
# )

# ------------------------------------------------------------------------------
# aws_a2i.deploy_flow_definition(
#     bsm=bsm,
#     flow_definition_name=flow_definition_name,
#     flow_execution_role_arn=flow_execution_role_arn,
#     labeling_team_arn=private_team_arn,
#     output_bucket=output_bucket,
#     output_key=output_key,
#     task_template_name=task_template_name,
#     task_description="Review reimbursement request",
#     task_count=1,
# )

# ------------------------------------------------------------------------------
# _, flow_details = aws_a2i.is_flow_definition_exists(
#     bsm=bsm, flow_definition_name=flow_definition_name
# )
# rprint(flow_details)

# workspace_signin_url = aws_a2i.get_workspace_signin_url(
#     bsm=bsm,
#     work_team_name=aws_a2i.parse_team_name_from_private_team_arn(arn=private_team_arn),
# )
# print(workspace_signin_url)
#
# aws_a2i.start_human_loop(
#     bsm=bsm,
#     human_loop_name=str(uuid.uuid4()),
#     flow_definition_arn=aws_a2i.get_flow_definition_arn(
#         aws_account_id=bsm.aws_account_id,
#         aws_region=bsm.aws_region,
#         flow_definition_name=flow_definition_name,
#     ),
#     input_data={
#         "date_of_expense": "2020-01-01",
#         "payment_method": "Credit Card",
#         "purpose_of_expenditure": "Business Meal",
#         "amount": "36.99",
#     },
# )

# # ------------------------------------------------------------------------------
# path_task_ui_html = dir_here.parent.joinpath("task-ui.html")
# input_data = {
#     "date_of_expense": "2020-01-01",
#     "payment_method": "Credit Card",
#     "purpose_of_expenditure": "Business Meal",
#     "amount": "36.99",
# }
# aws_a2i.render_task_template(
#     task_template_content=path_task_template.read_text(),
#     input_data=input_data,
#     path_task_ui_html=path_task_ui_html,
#     preview=True,
# )


result = aws_a2i.list_human_loops(
    bsm=bsm,
    flow_definition_arn=flow_definition_arn,
)
for i in result:
    print(i)