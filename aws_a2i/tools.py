# -*- coding: utf-8 -*-

import typing as T
import sys
import subprocess
from pathlib import Path

try:
    from box import Box
    from liquid import Template

    HAS_DEPENDENCIES = True
except ImportError as e:
    HAS_DEPENDENCIES = False


def _warn_if_no_dependencies():
    if HAS_DEPENDENCIES is False:
        raise ImportError(f"cannot import 'box' or 'liquid' package")


def render_task_template(
    task_template_content: str,
    input_data: dict,
    path_task_ui_html: T.Union[str, Path, T.Any],
    preview: bool = True,
):
    _warn_if_no_dependencies()

    # read liquid template
    template = Template(task_template_content)

    # convert task data to box, so it support dot notation
    task = Box({"input": input_data})

    # render template
    content = template.render(task=task)

    # write template to html file
    path_task_ui_html = Path(path_task_ui_html)
    path_task_ui_html.write_text(content)

    # open html in browser
    if preview:
        if sys.platform in ["win32", "cygwin"]:
            open_command = "start"
        else:
            open_command = "open"
        subprocess.run([open_command, str(path_task_ui_html)])
