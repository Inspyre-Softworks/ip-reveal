class InvalidProjInfoRequestError(Exception):
    def __init__(self, choices, made_choice):
        self.message = f"INVALID CHOICE {made_choice}. Please choose from {', '.join(choices)}"


