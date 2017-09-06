# -*- coding: utf-8 -*-

from scripts import synth
from func import prevent_auido_error, give_values

from languages import Spanish, English, Italian, Personalizado

languages = [Spanish, Italian, Personalizado, English]
language = Spanish

sts = synth.Sts(language.babel)


class Language:
    def __init__(self):
        global language
        self.say = sts.say

    def intro(self):
        self.say(language.aud_001)
        # self.say(language.aud_002)

    def calibration(self, moment):
        if moment == 1:
            self.say(language.aud_003)
            self.say(language.aud_004)
            self.say(language.aud_005)
            self.say(language.aud_006)
        elif moment == 2:
            self.say(language.aud_007)
            self.say(language.aud_008)

    def arduino(self, signal):
        if signal:
            self.say(language.aud_009)
        else:
            self.say(language.aud_010)

    def match(self):
        prevent_auido_error(self.say, language.aud_011)
        prevent_auido_error(self.say, language.aud_012)
        prevent_auido_error(self.say, language.aud_013)

    def play(self, piece, position, eaten):
        if eaten:
            prevent_auido_error(self.say, language.aud_014 % (piece, position))
        else:
            prevent_auido_error(self.say, language.aud_015 % (piece, position))

    def error_1(self):
        self.say(language.aud_019)
        self.say(language.aud_020)

    def error_2(self):
        self.say(language.aud_021)

    def check_mate(self, player, turn):
        prevent_auido_error(self.say, language.aud_022 % (player, turn - 1))

    def promotion(self, piece):
        self.say(language.aud_023 % piece)

    def castling(self, side):
        if side.lower() == 'kingside':
            self.say(language.aud_024)

        elif side.lower() == 'queenside':
            self.say(language.aud_025)

    def repeat_move(self, first_time):
        self.say(language.aud_026)

        if first_time:
            self.say(language.aud_027)


class Advice(Language):
    pawn_1, pawn_2, knight = give_values(None, 3)

    def main(self):
        self.pawn_1 = language.aud_016
        self.pawn_2 = language.aud_017
        self.knight = language.aud_018


def _refresh_sts():
    global language, sts
    try:
        sts = synth.Sts(language.sound)

    except AttributeError:
        sts = synth.Sts(language.babel)


def english():
    global language
    language = English
    _refresh_sts()


def spanish():
    global language
    language = Spanish
    _refresh_sts()


def italian():
    global language
    language = Italian
    _refresh_sts()


def personalizado():
    global language
    language = Personalizado
    _refresh_sts()
