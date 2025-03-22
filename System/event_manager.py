class EventManager:
    def __init__(self):
        self.ai_list = []

    def register_ai(self, ai):

        self.ai_list.append(ai)

    def broadcast_event(self, origin_ai, event):

        for ai in self.ai_list:
            if ai != origin_ai:  # Exclude the event's origin AI
                ai.receive_event(origin_ai, event)
