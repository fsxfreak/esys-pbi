import zmq
from zmq.utils.monitor import recv_monitor_message

import msgpack as serializer

ipc_sub_url = 'tcp://127.0.0.1:40669'

def main():
  context = zmq.Context()
  socket = zmq.Socket(context, zmq.SUB)
  monitor = socket.get_monitor_socket()

  socket.connect(ipc_sub_url)
  while True:
    status = recv_monitor_message(monitor)
    if status['event'] == zmq.EVENT_CONNECTED:
      break
    elif status['event'] == zmq.EVENT_CONNECT_DELAYED:
      pass

  print('connected')
  socket.subscribe('pupil')
  while True:
    topic = socket.recv_string()
    payload = serializer.loads(socket.recv(), encoding='utf-8')
    print(topic, payload)

if __name__ == '__main__':
  main()
