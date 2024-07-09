#!/usr/bin/env python
"""The run script"""
import logging
import requests
import sys
from flywheel_gear_toolkit import GearToolkitContext
from app.parser import parse_config
from app.main import run

# Set up logging
log = logging.getLogger(__name__)

# Define main function
def main(context: GearToolkitContext) -> None:

    try:
        # Get the input files
        api_key = parse_config(context)
        
        # Run the tagger function
        e_code = run(context, api_key)

    except (TimeoutError, requests.exceptions.ConnectionError) as exc:
        log.error("Timeout error. Try increasing the read_timeout config parameter.")
        log.exception(exc)
        e_code = 1
    except Exception as exc:
        log.exception(exc)
        e_code = 1

    # Exit the python script with the exit code
    sys.exit(e_code)


# Only execute if file is run as main, not when imported by another module
if __name__ == "__main__":  # pragma: no cover
    # Get access to gear config, inputs, and sdk client if enabled.
    with GearToolkitContext() as gear_context:
        # Initialize logging, set logging level based on `debug` configuration
        # key in gear config.
        gear_context.init_logging()
        # Pass the gear context into main function defined above.
        main(gear_context)