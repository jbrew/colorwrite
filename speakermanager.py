
import pyttsx
import sys


class SpeakerManager(object):
    """Provide a context to for using Speaker in with statements."""
    def __enter__(self):    
        class Speaker(object):
            """Performs Text-To-Speech"""
            def __init__(self):
                self._engine = pyttsx.init()
                self._engine.startLoop(False)
                self._engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Alex')
                rate = self._engine.getProperty('rate')
                self._engine.setProperty('rate', rate)

            def say(self, message):
                print '\n'
                sys.stdout.write("say: " + message)
                self._engine.say(message)
                self._engine.iterate()

            def cleanup(self):
                self._engine.endLoop()


        self.speaker = Speaker()
        return self.speaker

    def __exit__(self, type, value, traceback):
        self.speaker.cleanup()

