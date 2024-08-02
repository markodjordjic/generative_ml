class GenericProfileFinder:

    def __init__(self, name_to_look: str = None) -> None:
        self.name_to_look = name_to_look


class LinkedInProfileFinder(GenericProfileFinder) -> tuple[]:

    def __init__(self, name_to_look: str = None) -> None:
        super().__init__(name_to_look)
        self.name_to_look = name_to_look

    def _find_user(self):
        pass

    def _scrape_profile_data(self):
        pass



