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
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Scoreboard layout
        scoreboard_layout = BoxLayout(size_hint=(1, None), height=50, padding=10, spacing=10)
        self.score_label = Label(text="Score: 0 - 0", font_size='16sp')
        scoreboard_layout.add_widget(self.score_label)
        layout.add_widget(scoreboard_layout)

        # Scrollable label for event chat
        self.scrollable_label = Label(text="Press the button to simulate a football match", font_size='16sp')
        self.scrollable_label.bind(size=self.scrollable_label.setter('text_size'))
        scrollview = ScrollView()
        scrollview.add_widget(self.scrollable_label)
        layout.add_widget(scrollview)

        # Button to start/stop simulation
        self.button = Button(text="Simulate Match", size_hint=(None, None), size=(200, 50),
                        background_color=(0.1, 0.5, 0.9, 1),
                        color=(1, 1, 1, 1),
                        font_size='16sp')
        self.button.bind(on_press=self.on_button_press)
        layout.add_widget(self.button)

        # Slider to adjust simulation speed
        self.slider = Slider(min=0.1, max=7.0, value=1.0, step=0.1, size_hint=(None, None), size=(200, 50))
        self.slider.bind(value=self.on_slider_change)
        layout.add_widget(self.slider)

        # Initialize simulation speed attribute
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
        self.home_score = 0  # Reset home score
        self.away_score = 0  # Reset away score
        self.simulate_match()

    def stop_simulation(self):
        self.scrollable_label.text = "Press the button to simulate a football match"
        self.button.text = "Simulate Match"
        Clock.unschedule(self.event)

    def simulate_match(self):
        events = [
            ("Home Team makes move", 0.3),
            ("Away Team makes move", 0.3),
            ("Home Team attempts a shot", 0.4),
            ("Away Team attempts a shot", 0.4),
            ("Home Team scores a goal!", 0.1),  # Adjusted probability for goal events
            ("Away Team scores a goal!", 0.1),  # Adjusted probability for goal events
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
        self.home_score = 0  # Reset home score
        self.away_score = 0  # Reset away score
        while match_time < match_duration:
            event, probability = random.choice(events)
            if random.random() < probability:
                if "makes move" in event or "attempts a shot" in event:
                    match_events.append((match_time, event))
                    if "on target" in event:
                        goal_scored = self.attempt_goal()
                        if goal_scored:
                            event = "Goal!"
                            if "Home" in event:
                                self.home_score += 1
                            else:
                                self.away_score += 1
                match_events.append((match_time, event))
            match_time += 1

        match_events.append((90, "Match Ended", f"Barcelona {self.home_score} - {self.away_score} Real Madrid"))

        self.score_label.text = f"Score: {self.home_score} - {self.away_score}"

        self.event_index = 0
        self.match_events = match_events
        self.event = Clock.schedule_interval(self.display_event, 3.0 / self.simulation_speed)

    def attempt_goal(self):
        return random.random() < 0.2

    def display_event(self, dt=None):
        if self.event_index < len(self.match_events):
            event_info = self.match_events[self.event_index]
            if len(event_info) == 2:
                event_time, event_desc = event_info
                self.scrollable_label.text += f"\n{event_time}' {event_desc}"
            elif len(event_info) == 3:
                event_time, event_type, event_desc = event_info
                self.scrollable_label.text += f"\n{event_time}' {event_type}: {event_desc}"
            
            self.event_index += 1

            # Check if it's a goal event and update scoreboard accordingly
            if "scores a goal!" in event_desc:
                team_name = "Home" if "Home" in event_desc else "Away"
                if team_name == "Home":
                    self.home_score += 1
                else:
                    self.away_score += 1
                self.score_label.text = f"Barcelona {self.home_score} - {self.away_score} Real Madrid"

    def update_scoreboard(self):
        self.score_label.text = f"Barcelona {self.home_score} - {self.away_score} Real Madrid"


if __name__ == '__main__':
    MyApp().run()
