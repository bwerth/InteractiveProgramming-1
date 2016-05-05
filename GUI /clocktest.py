from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock

import time

class IncrediblyCrudeClock(Label):
    def update(self, *args):
        self.text = 'Hello World'

class TimeApp(App):
    def build(self):
        crudeclock = IncrediblyCrudeClock()
        Clock.schedule_once(crudeclock.update, 4)
        return crudeclock

if __name__ == "__main__":
    TimeApp().run()