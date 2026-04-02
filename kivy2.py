import webbrowser
from kivy.app import App
from kivy.uix.button import Button
from kivy.animation import Animation

class ap(App):
    def build(self):
        btn = Button(text="Click Me", background_color=(1, 1, 0, 1))  # Yellow
        btn.bind(on_press=lambda x: Animation(background_color=(0, 1, 1, 1), duration=1).start(btn)) 
        btn1 = Button(text="Open Google", on_press=lambda x: webbrowser.open("https://www.google.com"))

        return btn1

j = ap()
j.run()