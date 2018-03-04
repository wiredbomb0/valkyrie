import os
import sys
import time
import logging
import json

from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

class RebuildFilterEvent(LoggingEventHandler):
  def dispatch(self, event):
    if ".filterplus" in event.src_path:
      RebuildFilter(event.src_path)

def RebuildFilter(file):
  # Calculate start time
  start_time = int(round(time.time() * 1000))

  # Load color changes
  color_swap = None
  with open("colors.json", "r") as _f:
    color_swap = json.load(_f)

  item_filter = None
  # Open file
  with open(file, "r") as _f:
    item_filter = _f.read()

  # Replace all the colors
  for key, value in color_swap.iteritems():
    item_filter = item_filter.replace(key, value)

  # Write file
  with open(file.replace(".filterplus", ".filter"), "w+") as _f:
    _f.write(item_filter)

  # Calculate end time
  end_time = int(round(time.time() * 1000))
  total_time = end_time - start_time

  # Output helpful information
  print "{} took {}ms".format(os.path.basename(file), total_time)

if __name__ == "__main__":
  event_handler = RebuildFilterEvent()
  observer = Observer()
  observer.schedule(event_handler, ".", recursive=True)
  observer.start()
  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    observer.stop()
  observer.join()