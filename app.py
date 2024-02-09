from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.clock import Clock
import random

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        self.scrollable_label = Label(text="Press the button to simulate a football match", font_size='20sp', size_hint_y=None, height=400)
        self.scrollable_label.bind(size=self.scrollable_label.setter('text_size'))

        scrollview = ScrollView()
        scrollview.add_widget(self.scrollable_label)
        scrollview.scroll_y = 1

        self.button = Button(text="Simulate Match", size_hint=(None, None), size=(200, 50),
                        background_color=(0.1, 0.5, 0.9, 1),
                        color=(1, 1, 1, 1),
                        font_size='20sp')
        self.button.bind(on_press=self.on_button_press)

        self.slider = Slider(min=0.1, max=2.0, value=1.0, step=0.1, size_hint=(None, None), size=(200, 50))
        self.slider.bind(value=self.on_slider_change)

        layout.add_widget(scrollview)
        layout.add_widget(self.button)
        layout.add_widget(self.slider)

        self.simulation_speed = 1.0

        return layout

    def on_button_press(self, instance):
        if self.button.text == "Simulate Match":
            self.start_simulation()
        else:
            self.stop_simulation()

    def on_slider_change(self, instance, value):
        self.simulation_speed = value
        if hasattr(self, 'event'):
            Clock.unschedule(self.event)
            self.event = Clock.schedule_interval(self.display_event, 3.0 / self.simulation_speed)

    def start_simulation(self):
        self.scrollable_label.text = ""
        self.button.text = "Stop!"
        self.simulate_match()

    def stop_simulation(self):
        self.scrollable_label.text = "Press the button to simulate a football match"
        self.button.text = "Simulate Match"
        Clock.unschedule(self.event)

    def simulate_match(self):
        events = [
            ("Home Team makes move", 0.4),
            ("Away Team makes move", 0.4),
            ("Home Team attempts a shot", 0.15),
            ("Away Team attempts a shot", 0.15),
            ("Home Team scores a goal!", 0.05),
            ("Away Team scores a goal!", 0.05),
            ("Corner kick for Home Team", 0.05),
            ("Corner kick for Away Team", 0.05),
            ("Free kick for Home Team", 0.05),
            ("Free kick for Away Team", 0.05),
            ("Throw-in for Home Team", 0.05),
            ("Throw-in for Away Team", 0.05)
        ]

        match_duration = 90     
        match_time = 0
        match_events = []
        while match_time < match_duration:
            event, probability = random.choice(events)
            if random.random() < probability:
                if "makes move" in event or "attempts a shot" in event:
                    match_events.append((match_time, event))
                    move_success = self.attempt_move()
                    if move_success:
                        goal_scored = self.attempt_goal()
                        if goal_scored:
                            event = "Goal!"
                        else:
                            event = "Shot on target!"
                    else:
                        event = "Move failed!"
                match_events.append((match_time, event))
            match_time += 1

        self.event_index = 0
        self.match_events = match_events
        self.event = Clock.schedule_interval(self.display_event, 3.0 / self.simulation_speed)

    def attempt_move(self):
        return random.random() < 0.8

    def attempt_goal(self):
        return random.random() < 0.2

    def display_event(self, dt=None):
        if self.event_index < len(self.match_events):
            event_time, event_desc = self.match_events[self.event_index]
            self.scrollable_label.text += f"\n{event_time}' {event_desc}"
            self.event_index += 1

if __name__ == '__main__':
    MyApp().run()
