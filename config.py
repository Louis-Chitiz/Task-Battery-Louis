import yaml
from os import path
default_config = {
    "randomize_task":False,
    "num_task_in_subset":5,

}

with open('config.yaml','w') as f:
    yaml.dump(default_config,f)