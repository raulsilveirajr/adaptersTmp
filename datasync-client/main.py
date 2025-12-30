import argparse
import time

from engine.main_engine import exec_guider
from engine.tools.logger import log

start_time = time.time()

parser = argparse.ArgumentParser(description="Generic script to sync data.")
parser.add_argument("guider_name", type=str, help="Guider to use.")

args = parser.parse_args()

log(f"Received parameter: {args.guider_name}")

exec_guider(args.guider_name)

end_time = time.time()
elapsed_time = end_time - start_time

log(f"Time taken: {elapsed_time:.2f} seconds")
