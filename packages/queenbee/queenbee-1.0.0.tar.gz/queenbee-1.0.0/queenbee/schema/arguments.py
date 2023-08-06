"""Queenbee Arguments class.

Arguments includes the input arguments to a task or a workflow.

Queenbee accepts two types of arguments:

    1. Parameters: A ``parameter`` is a variable that can be passed to a task or a
        workflow.
    2. Artifact: An ``artifact`` is a file or folder that can be identified by a url or
        a path.
"""
from queenbee.schema.qutil import BaseModel
from pydantic import Schema
from typing import List, Any


class Parameter(BaseModel):
    """Parameter.

    Parameter indicate a passed string parameter to a service template with an optional
    default value.
    """
    name: str = Schema(
        ...,
        description='Name is the parameter name. must be unique within a task\'s '
        'inputs / outputs.'
    )

    value: Any = Schema(
        None,
        description='Default value to use for an input parameter if a value was not'
        ' supplied.'
    )

    description: str = Schema(
        None,
        description='Optional description for input parameter.'
    )

    path: str = Schema(
        None,
        description='load parameters from a file. File can be a JSON / YAML or a text file.'
    )


class Artifact(BaseModel):
    """Artifact indicates an artifact to place at a specified path"""

    name: str = Schema(
        ...,
        description='name of the artifact. must be unique within a task\'s '
        'inputs / outputs.'
    )

    path: str = Schema(
        None,
        description='Path is the path to the artifact which can be a local path or a url.'
    )

    is_url: bool = Schema(
        False,
        description='Switch to indicate if path is a url.'
    )

    description: str = Schema(
        None,
        description='Optional description for input parameter.'
    )


class Arguments(BaseModel):
    """Arguments to a task or a workflow.
    
    Queenbee accepts two types of arguments: parameters and artifacts. A ``parameter``
    is a variable that can be passed to a task or a workflow. An ``artifact`` is a file
    or folder that can be identified by a url or a path.
    """

    parameters: List[Parameter] = Schema(
        None,
        description='Parameters is the list of input parameters to pass to the task '
        'or workflow. A parameter can have a default value which will be overwritten if '
        'an input value is provided.'
    )

    artifacts: List[Artifact] = Schema(
        None,
        description='Artifacts is the list of file and folder arguments to pass to the '
        'task or workflow.'
    )
