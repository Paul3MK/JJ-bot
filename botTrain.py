import logging
import asyncio
from rasa.train import train_core
from rasa.core.train import train
from rasa.core.policies.memoization import MemoizationPolicy
from rasa.core.policies.keras_policy import KerasPolicy
from rasa.core.policies.form_policy import FormPolicy
from rasa.cli.utils import create_output_path
from rasa.core.agent import Agent
import os
import psycopg2


def botTrain():
    logging.basicConfig(level=logging.DEBUG)
    # training the core model
    train_core("domain.yml", "config.yml", "data/stories.md", "models/dialogue", fixed_model_name="core")

botTrain()

DATABASE_URL = os.environ['DATABASE_URL']
# con = psycopg2.connect(database="jjtestdb", user="postgres", password="hieg") #for local work
con =  psycopg2.connect(DATABASE_URL, sslmode='require')
with con:
    
    cur = con.cursor()
    cur.execute("INSERT INTO trained_counter VALUES(1)")    
