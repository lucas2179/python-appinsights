from sanic import Sanic
import os
from opencensus.ext.azure.trace_exporter import AzureExporter
from sanic.response import json
from sanic.log import logger
from opencensus.ext.azure.log_exporter import AzureLogHandler
import asyncio
import psycopg2
from opencensus.trace.tracer import Tracer
from opencensus.trace.samplers import ProbabilitySampler

import sys



tracer = Tracer(
  exporter = AzureExporter(
    connection_string=os.getenv('APPINSIGHTS_KEY')
  ),
  sampler=ProbabilitySampler(1.0)
)
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,    
    "handlers": {
        "azure": {
            "class": "opencensus.ext.azure.log_exporter.AzureLogHandler",
            "connection_string": os.getenv('APPINSIGHTS_KEY'),
            "level": "DEBUG"
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": sys.stdout 
        }
    },
    "loggers": {
        "sanic.root": {
            "handlers": ["azure"],
            "level": "DEBUG",
            "propagate": True
        }
    }
}
app = Sanic(name='teste', log_config=logging_config)



async def connect_to_db():
    with tracer.span(name="teste") as span:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS')
        )
    return conn

@app.route("/")
async def test(request):
    with tracer.span(name="teste") as span:
        conn = await connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * from IMP_TEST.ISO_COUNTRY")
        rows = cursor.fetchall()
        logger.exception("here is your log")
    return json({"data": rows})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
