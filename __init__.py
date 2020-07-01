from mycroft import intent_file_handler, intent_handler, MycroftSkill
from mycroft.skills.core import resting_screen_handler
from os.path import join, dirname


class SpaceStuffSkill(MycroftSkill):


    @resting_screen_handler("SpaceStuff")
    def idle(self, message):
        self.gui.clear()
        url = join(dirname(__file__), "ui", "index.php") # TODO
        #url = "http://stuffin.space/"
        self.gui.show_url(url,  override_idle=200)

    @intent_file_handler("spacestuff.intent")
    def handle_debris_intent(self, message):
        self.speak_dialog("spacestuff")
        self.idle(message)


def create_skill():
    return SpaceStuffSkill()
