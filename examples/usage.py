# -*- coding: utf-8 -*-

from pathlib import Path

from rich import print as rprint
from boto_session_manager import BotoSesManager

import aws_a2i.api as aws_a2i

bsm = BotoSesManager(profile_name="awshsh_app_dev_us_east_1")

# dir_here = Path(os.getcwd()).absolute() # for jupyter notebook
dir_here = Path(__file__).absolute().parent  # for python script

path_task_template = dir_here.parent.joinpath("task-ui.liquid")

play = aws_a2i.Play(
    aws_account_id=bsm.aws_account_id,
    aws_region=bsm.aws_region,
    # task UI template name
    task_template_name="aws-a2i-example",
    task_template_content=path_task_template.read_text(),
    # Human Review Workflow name
    flow_definition_name="aws-a2i-example",
    # The IAM role for Human Review Workflow, you have to create it yourself
    flow_execution_role_arn=f"arn:aws:iam::{bsm.aws_account_id}:role/all-services-admin-role",
    # Where you store HIL output data
    output_bucket=f"{bsm.aws_account_id}-{bsm.aws_region}-data",
    output_key="projects/aws_a2i-project/hil-output/",
    # the Ground Truth private team ARN
    private_team_arn=f"arn:aws:sagemaker:{bsm.aws_region}:{bsm.aws_account_id}:workteam/private-crowd/my-private-team",
)

def remove_flow_definition():
    play.remove_flow_definition(bsm=bsm)

    
def remove_hil_task_template():
    play.remove_hil_task_template(bsm=bsm)


def deploy_hil_task_template():
    play.deploy_hil_task_template(bsm=bsm, verbose=True)


def deploy_flow_definition():
    play.deploy_flow_definition(
        bsm=bsm,
        task_description="Review reimbursement request",
        task_count=1,
    )
    flow_def = play.get_flow_definition(bsm=bsm)
    rprint(flow_def)


def print_flow_definition_details():
    _, flow_details = aws_a2i.is_flow_definition_exists(
        bsm=bsm, flow_definition_name=play.flow_definition_name
    )
    rprint(flow_details)


def print_workspace_signin_url():
    workspace_signin_url = play.get_workspace_signin_url(bsm=bsm)
    print(f"Login to the workspace: {workspace_signin_url}")


def start_human_loop():
    input_data = {
        "date_of_expense": "2020-01-01",
        "payment_method": "Credit Card",
        "purpose_of_expenditure": "Business Meal",
        "amount": "36.99",
    }
    play.start_human_loop(bsm=bsm, input_data=input_data)


def render_task_template():
    path_task_ui_html = dir_here.parent.joinpath("task-ui.html")
    input_data = {
        "date_of_expense": "2020-01-01",
        "payment_method": "Credit Card",
        "purpose_of_expenditure": "Business Meal",
        "amount": "36.99",
    }
    aws_a2i.render_task_template(
        task_template_content=path_task_template.read_text(),
        input_data=input_data,
        path_task_ui_html=path_task_ui_html,
        preview=True,
    )


def inspect_human_loops_details():
    result = play.list_human_loops(bsm=bsm)
    for human_loop in result:
        if human_loop.is_completed():
            human_loop.get_details(bsm=bsm)
            rprint(human_loop)
            human_loop_output = human_loop.get_output(bsm=bsm)
            rprint(human_loop_output)
        else:
            rprint(human_loop)
        break


# remove_flow_definition()
# remove_hil_task_template()
# deploy_hil_task_template()
# deploy_flow_definition()
# print_flow_definition_details()
# print_workspace_signin_url()
# start_human_loop()
# render_task_template()
# inspect_human_loops_details()
