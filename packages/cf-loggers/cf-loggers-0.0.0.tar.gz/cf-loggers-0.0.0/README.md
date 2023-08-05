# Elasticsearch

Light weight NoSQL logger handles that we internally use at Invana. 

## Installation
`pip install cf-loggers`

## TODO

- write in bulk
- authentications - basic, aws signed auth.

## Simple Usage 
```python

from cf_loggers.setup import init_logger
import logging

logger_settings = {
    "HOSTS": ["localhost:9200"],
    "INDEX": "custom_index",
    "DOC_TYPE": "something",
    "EXTRA_DATA": {"machine_type": "task-engine"},
    "LEVEL": "INFO"
}

init_logger(logger_settings)
logging.info("Hello Earthians, We are coming from back from Mars soon")

```

## Advanced Usage 

```python

import logging
from cf_loggers.elasticsearch.handler import ESLoggingHandler

logger_settings = {
    "HOSTS": ["localhost:9200"],
    "INDEX": "custom_index",
    "DOC_TYPE": "something",
    "EXTRA_DATA": {"machine_type": "task-engine"},
    "LEVEL": "INFO"
}

logging.getLogger("elasticsearch").setLevel(logging.WARNING)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] [%(name)s]   %(message)s",
    handlers=[
        logging.StreamHandler(),
        ESLoggingHandler(
            hosts=logger_settings['HOSTS'],
            index=logger_settings['INDEX'],
            doc_type=logger_settings.get('DOC_TYPE'),
            extra_data=logger_settings.get("EXTRA_DATA", {})
        )
    ])
logging.info("Hello Earthians, We are coming from back from Mars soon")

```