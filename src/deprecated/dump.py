class BaseThread(QThread):

    def __init__(self, window : BaseWindow=None):
        self.window = window
        self.docker_client = docker.from_env()
        super().__init__()

    def WaitingText(self, str_signal : pyqtSignal(str)):

        dots_number = 3
        text = self.window.GetText()

        while text[-1] == '.':
            text = text[:-1]
        for i in range(dots_number):
            text += '.'
            str_signal.emit(text)
            time.sleep(0.5)
            if i == dots_number - 1:
                text = text[:-dots_number]
                str_signal.emit(text)
                time.sleep(0.5)


class WaitingHandler(QThread):

    update_text = pyqtSignal(str)
    dots_number = 3
    stop = False

    def __init__(self, window : BaseWindow=None):

        self.window = window
        super().__init__()

    def run(self):
        if isinstance(self.window, BaseWindow):
            self.WaitingText()

    def WaitingText(self):
        text = self.window.GetText()
        # Removing all the dots at the end of our text
        while text[-1] == '.':
            text = text[:-1]
        for i in range(self.dots_number):
            text += '.'
            self.update_text.emit(text)
            time.sleep(0.5)
            if i == self.dots_number - 1:
                text = text[:-self.dots_number]
                self.update_text.emit(text)
                time.sleep(0.5)
        if self.stop is True:
            self.finished.emit()
        else:
            # Once done, we call the function again
            self.WaitingText()

def LaunchWaitingHandler(self):
    waiting_handler = WaitingHandler(window=self)
    waiting_handler.update_text.connect(self.setText)
    waiting_handler.finished.connect(self.RemoveWaitingHandlerThread)
    self.threads.append(waiting_handler)
    self.threads[-1].start()

def RemoveWaitingHandler(self):
    for thread in self.threads:
        if isinstance(thread, WaitingHandler):
            thread.stop = True

def RemoveWaitingHandlerThread(self):
    for thread in self.threads:
        if isinstance(thread, WaitingHandler):
            self.threads.remove(thread)