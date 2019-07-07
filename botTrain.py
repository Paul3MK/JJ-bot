import logging
import asyncio
from rasa.train import train_core
from rasa.core.train import train
from rasa.core.policies.memoization import MemoizationPolicy
from rasa.core.policies.keras_policy import KerasPolicy
from rasa.core.policies.form_policy import FormPolicy
from rasa.cli.utils import create_output_path
from rasa.core.agent import Agent


def botTrain():
    logging.basicConfig(level=logging.DEBUG)
    # training the core model
    train_core("domain.yml", "config.yml", "data/stories.md", "models/dialogue", fixed_model_name="core")

botTrain()