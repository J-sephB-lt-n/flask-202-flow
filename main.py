"""Defines Flask API endpoints"""

# standard lib imports #
import datetime
import logging
import time

# 3rd party imports #
import flask

# set up logging #
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = flask.Flask(__name__)


@app.route("/202_flow_example", methods=["POST"])
def index():
    """Example endpoint which returns a 202 response to the client
    then continues to run code after that"""

    wait_n_seconds_after_response: int = int(
        flask.request.args.get("wait_n_secs_after_response")
    )
    if wait_n_seconds_after_response > 10:
        response = flask.Response(
            f'FORBIDDEN (403) at {datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]}',
            status=403,
        )
    else:
        response = flask.Response(
            f'ACCEPTED (202) at {datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]}',
            status=202,
        )

    # save variable `wait_n_seconds_after_response` in response object #
    # (so it can be accessed within @response.call_on_close)
    setattr(
        response,
        "wait_n_secs_after_response",
        wait_n_seconds_after_response,
    )

    @response.call_on_close
    def on_close():
        """This code is run after returning the response to the client"""
        if response.status_code == 202:
            # only run this code if client response was [202] 'ACCEPTED' #
            logger.info("started after response code")
            wait_cntr = 0
            for _ in range(response.wait_n_secs_after_response):
                wait_cntr += 1
                time.sleep(1)
                logger.info(f"waited {wait_cntr} seconds")
            logger.info(
                "finished waiting %s seconds", response.wait_n_secs_after_response
            )

    return response
