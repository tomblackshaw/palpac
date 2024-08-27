"""
Created on Jun 2, 2024

@author: Tom Blackshaw
"""
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Ellipse, Color
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider

Window.size = (720, 400)


class CircleApp(App):

    def build(self):
        # main layout
        lo = BoxLayout(orientation='vertical', size=Window.size)

        # for width and height sliders
        sliders_wh = BoxLayout(size_hint_y=None, height=50)

        slb1 = BoxLayout(orientation='horizontal')
        self.sl1 = Slider(min=100, max=300, value=200)
        l1 = Label(text='Width: {}'.format(int(self.sl1.value)))
        slb1.add_widget(self.sl1)
        slb1.add_widget(l1)
        self.sl2 = Slider(min=100, max=300, value=200)
        l2 = Label(text='Height: {}'.format(int(self.sl2.value)))
        slb1.add_widget(self.sl2)
        slb1.add_widget(l2)
        sliders_wh.add_widget(slb1)

        # for cx and cy sliders
        sliders_xy = BoxLayout(size_hint_y=None, height=50)
        slb2 = BoxLayout(orientation='horizontal')
        self.sl3 = Slider(min=10, max=600, value=360)
        l3 = Label(text='cx: {}'.format(int(self.sl3.value)))
        slb2.add_widget(self.sl3)
        slb2.add_widget(l3)
        self.sl4 = Slider(min=10, max=300, value=50)
        l4 = Label(text='cy: {}'.format(int(self.sl4.value)))
        slb2.add_widget(self.sl4)
        slb2.add_widget(l4)
        sliders_xy.add_widget(slb2)

        lo.add_widget(sliders_wh)
        lo.add_widget(sliders_xy)

        self.flo = FloatLayout()  # circle canvas

        lo.add_widget(self.flo)

        # redraw cicle
        self.ev = Clock.schedule_interval(self.callback, .3)
        return lo

    def callback(self, dt):
        self.flo.canvas.clear()
        with self.flo.canvas:
            Color(1, 1, 1)
            Ellipse(
                pos=(self.sl3.value, self.sl4.value),
                size=(self.sl1.value, self.sl2.value),
                angle_start=0, angle_end=360
           )


CircleApp().run()
