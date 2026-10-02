"""Project pipelines."""

import os

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline

KEDRO_ENV = os.getenv("KEDRO_ENV")


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns
    -------
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = find_pipelines()

    env_pipeline_names = ["data_processing", "data_science"]
    if KEDRO_ENV in ["local", "dev"]:
        env_pipeline_names.append("model_tuning")

    # Kedro >= 1.7 only discovers the pipelines requested by the run, so skip the absent ones
    pipelines = {name: pipelines[name] for name in env_pipeline_names if name in pipelines}

    # https://github.com/kedro-org/kedro/issues/2526
    pipelines["__default__"] = sum(pipelines.values(), start=Pipeline([]))
    return pipelines
