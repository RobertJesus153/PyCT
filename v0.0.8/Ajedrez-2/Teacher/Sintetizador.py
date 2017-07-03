# -*- coding: utf-8 -*-

import pyttsx


class Sts:
    def __init__(self, inicio):
        self.engine = pyttsx.init()
        self.engine.setProperty('rate', 140)
        self.engine.setProperty('voice', 'spanish')

        if inicio:
            self.say('Hola, soy Pict')
            self.say(u'Mi objetivo es enseñarte a jugar al ajedrez')

    def say(self, texto):
        self.engine.say(unicode(texto))
        self.engine.say(' ')
        self.engine.runAndWait()
        self.engine.runAndWait()
