import logging
import queue
import threading


class MessageQueue:
    def __init__(self):
        self.queues = {}
        self.running = False
        self.thread = None

    def create_queue(self, name):
        self.queues[name] = queue.Queue()

    def put(self, name, message):
        if name in self.queues:
            self.queues[name].put(message)

    def get(self, name):
        if name in self.queues:
            return self.queues[name].get()

    def _loop(self):
        logging.info("MessageQueue loop iniciado")
        while self.running:
            # aqui você pode implementar lógica de monitoramento,
            # como consumir mensagens de status e atualizar algo
            pass
        logging.info("MessageQueue loop encerrado")

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._loop, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
