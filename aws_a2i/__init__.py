# -*- coding: utf-8 -*-

"""
Amazon Augmented AI for Human.
"""


from ._version import __version__

__short_description__ = "Amazon Augmented AI for Human."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"


try:
    from .better_boto.human_task_ui import (
        get_task_template_arn,
        get_task_template_console_url,
        parse_task_template_name_from_arn,
        is_hil_task_template_exists,
        create_human_task_ui,
        delete_human_task_ui,
        deploy_hil_task_template,
        remove_hil_task_template,
    )
    from .better_boto.flow_definition import (
        get_flow_definition_arn,
        get_flow_definition_console_url,
        parse_flow_definition_name_from_arn,
        is_flow_definition_exists,
        create_flow_definition,
        delete_flow_definition,
        remove_flow_definition,
        deploy_flow_definition,
    )
    from .better_boto.human_loop import (
        parse_team_name_from_private_team_arn,
        get_workspace_signin_url,
        get_hil_console_url,
        parse_hil_name_from_hil_arn,
        describe_human_loop,
        start_human_loop,
    )
    from .tools import (
        render_task_template,
    )
    from .tagging import (
        to_tag_list,
        to_tag_dict,
    )
    from .helper import (
        sha256_of_bytes,
        vprint,
    )
except ImportError:  # pragma: no cover
    pass
