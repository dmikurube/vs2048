import Queue
import threading


class NonBlockingStreamReader:

    def __init__(self, stream):
        '''
        stream: the stream to read from.
                Usually a process' stdout or stderr.
        '''

        self._finished = False
        self._s = stream
        self._q = Queue.Queue()

        def _populateQueue(stream, queue):
            '''
            Collect lines from 'stream' and put them in 'quque'.
            '''

            while True:
                line = stream.readline()
                if line:
                    queue.put(line)
                else:
                    self._finished = True
                    break

        self._t = threading.Thread(target = _populateQueue,
                                   args = (self._s, self._q))
        self._t.daemon = True
        self._t.start()  # start collecting lines from the stream

    def readline(self, timeout = None):
        try:
            return self._q.get(block = timeout is not None,
                               timeout = timeout)
        except Queue.Empty:
            return None

class UnexpectedEndOfStream(Exception): pass
