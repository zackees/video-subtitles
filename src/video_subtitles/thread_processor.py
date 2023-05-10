"""
Processes threads one at a time.
"""

import queue
import threading


# Can't use futures because it doesn't have a daemon option so we have to
# impliment our own thread processor.
class ThreadProcessor(threading.Thread):
    """Thread processor."""

    def __init__(self) -> None:
        super().__init__(daemon=True)
        self.pending_tasks: queue.Queue = queue.Queue()
        self.processing_task: threading.Thread | None = None
        self.event = threading.Event()
        self.update_status_cb = lambda _: None

    def set_status_callback(self, callback) -> None:
        """Sets the status callback."""
        self.update_status_cb = callback

    def run(self) -> None:
        """Process each thread in the queue."""
        while not self.event.wait(0.1):
            if self.processing_task is not None:
                self.update_status_cb(True)
                if not self.processing_task.is_alive():
                    self.processing_task.join()
                    self.processing_task = None
            else:
                self.update_status_cb(False)
            if self.processing_task is not None:
                continue
            if self.pending_tasks.empty():
                continue
            self.processing_task = self.pending_tasks.get()
            self.processing_task.start()

    def add(self, thread: threading.Thread) -> None:
        """Queues a thread to be executed."""
        assert thread.daemon is True
        self.pending_tasks.put(thread)

    def stop(self) -> None:
        """Stops the thread executor."""
        self.event.set()
        self.join()
