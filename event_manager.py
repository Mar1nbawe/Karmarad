class EventManager:
    def __init__(self):
        self.ai_list = []

    def register_ai(self, ai):
        """Registers an AI to the event manager."""
        self.ai_list.append(ai)

    def broadcast_event(self, origin_ai, event):
        """
        Broadcast an event to all AIs except the origin.
        :param origin_ai: The AI that triggered the event.
        :param event: A dictionary describing the event (e.g., karma increase).
        """
        for ai in self.ai_list:
            if ai != origin_ai:  # Exclude the event's origin AI
                ai.receive_event(origin_ai, event)
