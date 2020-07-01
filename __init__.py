from mycroft import intent_file_handler, intent_handler, MycroftSkill
from mycroft.skills.core import resting_screen_handler
from os.path import join, dirname
import pexpect
from mycroft.util import create_daemon


class SpaceStuffSkill(MycroftSkill):

    def initialize(self):
        self.running = False
        create_daemon(self.serve_page)

    def serve_page(self):
        prev = ""
        self.running = True
        self.server = pexpect.spawn('php -S 0.0.0.0:8087 -t ' +
                                    join(dirname(__file__), "ui"))
        while self.running:
            try:
                out = self.server.readline().decode("utf-8")
                if out != prev:
                    out = out.strip()
                    self.log.debug(out)
            except pexpect.exceptions.EOF:
                self.server.close(True)
                break
            except pexpect.exceptions.TIMEOUT:
                # nothing happened for a while
                pass

    @resting_screen_handler("SpaceStuff")
    def idle(self, message):
        self.gui.clear()
        url = "http://0.0.0.0:8087/"
        self.gui.show_url(url,  override_idle=True)

    @intent_file_handler("spacestuff.intent")
    def handle_debris_intent(self, message):
        self.speak_dialog("spacestuff")
        self.idle(message)

    def shutdown(self):
        super().shutdown()
        self.server.close(True)
        self.running = False


def create_skill():
    return SpaceStuffSkill()
