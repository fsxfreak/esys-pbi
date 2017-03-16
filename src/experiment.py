from multiprocessing import Process, Queue, Event
import signal, time, sys

from time import sleep

import capture_bci
import display_stimuli
import graph_realtime

event = Event()

def stop():
  print('Stopping all programs.')
  event.set()

def sigint_handler(signal, frame):
  stop()

def main():
  signal.signal(signal.SIGINT, sigint_handler)

  print('Terminate by CTRL-C not functional on windows. Do not attempt, or you will have to cleanup zombie programs on the taskmanager.')

  stim_queue = Queue()
  bci_queue = Queue()

  stimuli = Process(target=display_stimuli.begin, args=((stim_queue), ))
  bci = Process(target=capture_bci.begin, args=((bci_queue), (event)))
  graph = Process(target=graph_realtime.begin, args=((None), (event)))

  stimuli.start()
  print('Waiting a bit for the stimuli to load...')
  time.sleep(1)
  print('Initializing sensors...')
  bci.start()
  print('Starting realtime graph...')

  bci_ready = False

  # Wait for the sensors to initialize before starting the experiment
  while True:
    bci_msg = bci_queue.get()
    print('bci_msg', bci_msg)

    if bci_msg == 'CONNECTED':
      bci_ready = True
      graph.start()
    elif bci_msg == 'FAIL':
      event.set()
      stimuli.terminate()
      bci.terminate()
      graph.terminate()
      sys.exit(-1)

    if bci_ready:
      stim_queue.put('BEGIN')
      break

  # Wait for the stimuli to finish displaying before stopping sensor capture
  while True:
    try:
      stim_msg = stim_queue.get()
      print('stim', stim_msg)
    except InterruptedError:
      stop()
      break

    if (stim_msg == 'FINISHED'):
      stop()
      break

  print('Terminating from the main thread...')
  stimuli.terminate()
  #bci.terminate() Do not send terminate signal on Windows.
  graph.terminate()

  stimuli.join()
  bci.join()
  graph.join()

if __name__ == '__main__':
  main()
