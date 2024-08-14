from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.clock import Clock
import random

class FootballApp(App):
    def match(self):
        pitch = BoxLayout(
            orientation='vertical', padding=20, spacing=10
            )

        # Scoreboard
        scoreboard = BoxLayout(
            size_hint=(1, None), height=50
            )
        self.skor_tablosu = Label(
            text="Score: 0 - 0", font_size='16sp'
            )
        scoreboard.add_widget(self.skor_tablosu)
        pitch.add_widget(scoreboard)

        # Event
        self.write_event = Label(
            text="Press the button to start match", font_size='16sp'
            )
        self.write_event.bind(size=self.write_event.setter('text_size'))
        scrollview = ScrollView()
        scrollview.add_widget(self.write_event)
        pitch.add_widget(scrollview)

        # Start/Stop
        self.startstop_button = Button(
            text="Start Match", size_hint=(None, None), size=(200, 50),
            background_color=(0.1, 0.5, 0.9, 1), color=(1, 1, 1, 1),
            font_size='16sp'
        )
        self.startstop_button.bind(on_press=self.startstop_sim)
        pitch.add_widget(self.startstop_button)

        # Speed adjuster
        self.speed_slider = Slider(
            min=0.1, max=7.0, value=1.0, step=0.1, size_hint=(None, None), size=(200, 50)
            )
        self.speed_slider.bind(value=self.adjust_speed)
        pitch.add_widget(self.speed_slider)

        self.speed = 1.0
        return pitch

    def startstop_sim(self, instance):
        if self.startstop_button.text == "Start":
            self.start_sim()
        else:
            self.stop_sim()

    def adjust_speed(self, instance, value):
        self.speed = value
        if hasattr(self, 'event'):
            Clock.unschedule(self.event)
            self.event = Clock.schedule_interval(
                self.display_next_event, 3.0 / self.speed
                )

    def start_sim(self):
        self.write_event.text = ""
        self.startstop_button.text = "Stop"
        self.home_score = 0
        self.away_score = 0
        self.match_events()

    def stop_sim(self):
        self.write_event.text = "Press the button to start match"
        self.startstop_button.text = "Start"
        Clock.unschedule(self.event)

    def match_events(self):
        events = [
            ("Home Team makes a move", 0.3),
            ("Away Team makes a move", 0.3),
            ("Home Team attempts a shot", 0.4),
            ("Away Team shoots", 0.4),
            ("Home Team scores!", 0.1),
            ("Away Team scores!", 0.1),
            ("Corner kick for Home Team", 0.05),
            ("Corner kick for Away Team", 0.05),
            ("Freekick for Home Team", 0.05),
            ("Freekick for Away Team", 0.05),
            ("Throw-in for Home Team", 0.05),
            ("Throw-in for Away Team", 0.05)
        ]

        match_time = 90
        start_time = 0
        match_events = []
        self.home_score = 0
        self.away_score = 0

        while start_time < match_time:
            event, probability = random.choice(events)
            if random.random() < probability:
                match_events.append((start_time, event))
                if "scores!" in event:
                    if "Home" in event:
                        self.home_score += 1
                    else:
                        self.away_score += 1
            start_time += 1

        match_events.append(
            (90, f"Match Ended: Barcelona {self.home_score} - {self.away_score} Real Madrid")
            )
        self.skor_tablosu.text = f"Score: {self.home_score} - {self.away_score}"
        self.event_index = 0
        self.match_events = match_events
        self.event = Clock.schedule_interval(self.display_next_event, 3.0 / self.speed)

    def display_next_event(self, dt=None):
        if self.event_index < len(self.match_events):
            event_time, event_text = self.match_events[self.event_index]
            self.write_event.text += f"\n{event_time}' {event_text}"
            self.event_index += 1
            self.skor_tablosu.text = f"Barcelona {self.home_score} - {self.away_score} Real Madrid"

if __name__ == '__main__':
    FootballApp().run()
