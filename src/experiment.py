from multiprocessing import Process, Queue
import signal

from time import sleep

import capture_stream
import display_stimuli

def main():
  jobs = []

  original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)

  # display_stimuli should be run first
  # TODO pass queue to children so they can communicate with parent
  jobs.append(Process(target=display_stimuli.main, args=()))
  jobs.append(Process(target=capture_stream.main, args=()))

  signal.signal(signal.SIGINT, original_sigint_handler)  

  print('starting jobs')
  for job in jobs:
    job.start()

  test = input("enter to continue")
 
  print('time to terminate jobs')
  for job in jobs:
    job.terminate()

  print('jobs have been sent terminate signal, join now')
  for job in jobs:
    job.join()

  print('jobs have been joined')

if __name__ == '__main__':
  main()
