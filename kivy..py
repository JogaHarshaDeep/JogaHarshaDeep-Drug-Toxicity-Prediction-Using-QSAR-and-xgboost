import random
from kivy.app import App
from kivy.uix.button import Button
from kivy.animation import Animation

class HoliApp(App):
    def build(self):
        return Button(text="Happy Holi!", background_color=(1, 0, 0, 1), on_press=self.splash_colors)

    def splash_colors(self, instance):
        Animation(background_color=(random.random(), random.random(), random.random(), 1), duration=0.5).start(instance)

aj = HoliApp()
aj.run()
