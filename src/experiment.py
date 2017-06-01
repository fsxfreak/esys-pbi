from multiprocessing import Process, Queue
import subprocess # to call python3 code
import signal, time, sys

from time import sleep

import capture_bci
# import capture_pupil
import display_stimuli
import graph_matplotlib

def stop(stimuli, bci, graph, pupil=None):
  print('Terminating from the main thread...')
  stimuli.terminate()
  bci.terminate()
  graph.terminate()

  if pupil:
    pupil.terminate()

def sigint_handler(signal, frame):
  # TODO bad fix
  stop(None, None, None)

def main():
  signal.signal(signal.SIGINT, sigint_handler)

  stim_queue = Queue()
  bci_queue = Queue()
  # pupil_queue = Queue()

  stimuli = Process(target=display_stimuli.begin, args=((stim_queue), ))
  bci = Process(target=capture_bci.begin, args=((bci_queue), ))
  graph = Process(target=graph_matplotlib.begin, args=((None), ))

  stimuli.start()
  print('Waiting a bit for the stimuli to load...')
  time.sleep(1)
  print('Initializing sensors...')
  bci.start()

  bci_ready = False

  # Wait for the BCI to initialize before starting the experiment
  while True:
    bci_msg = bci_queue.get()
    # TODO pupil_msg
    pupil_msg = None
    if bci_msg:
      print('bci_msg', bci_msg)

    if bci_msg == 'CONNECTED':
      bci_ready = True
      print('BCI connected, starting realtime graph...')
      graph.start()
    elif bci_msg == 'FAIL':
      stop(stimuli, bci, graph, None)
      sys.exit(-1)

    # TODO wait for pupil_ready?
    if bci_ready:
      break

  # open pupil process
  pupil = None
  '''
  pupil = subprocess.Popen(['sudo', 'python3', 'capture_pupil.py'],
                           stdout=subprocess.PIPE)
  while True:
    pass
    # TODO wait or the magic 'CONNECTED' from capture_pupil.main
  '''

  stim_queue.put('BEGIN')

  # Wait for the stimuli to finish displaying before stopping sensor capture
  while True:
    try:
      stim_msg = stim_queue.get()
      print('stim', stim_msg)
    except InterruptedError:
      stop(stimuli, bci, graph, pupil)
      break

    if (stim_msg == 'FINISHED'):
      stop(stimuli, bci, graph, pupil)
      break

  stimuli.join()
  bci.join()
  graph.join()

if __name__ == '__main__':
  main()
