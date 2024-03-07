from datetime import datetime

class Plant:
    def __init__(self, name: str = "", heyday: str = "", location: str = ""):
        self.further_info = ""
        self.name: str = name
        self.heyday: str = heyday
        self.location: str = location
        self.etymologie: str = ""
        self.eatable: str = ""


        self.image_paths: list[str | None] = [None, None, None, None]
        self.last_modified: datetime = datetime.now()
        self.created: datetime = datetime.now()

