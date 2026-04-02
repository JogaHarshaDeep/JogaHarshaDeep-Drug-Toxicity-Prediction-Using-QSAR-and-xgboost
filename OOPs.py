from kivy.app import App
from kivy.uix.button import Button
from kivy.animation import Animation

class a(App):
    def build (self):
        btn = Button(text = "me", background_color = (1,1,0,1))
        btn.bind(on_press = lambda x: Animation(background_color = (0,1,0,1),duration = 1).start(btn))
        return btn


dj = a()
dj.run()

