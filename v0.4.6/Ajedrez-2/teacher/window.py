#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

try:
    import gtk
except ImportError:
    import pygtk
    pygtk.require(2.0)
    import gtk
finally:
    import cv2

import lists
import pieces
import audio
from func import give_values, inv_change_position

pos0, pos1, who_promote = give_values(None, 3)


class Window:
    global pos0, pos1, who_promote

    @staticmethod
    def destroy(widget, data=None):
        gtk.main_quit()

    @staticmethod
    def translate(string, to):
        if to == 'english':
            string = re.sub(audio.language.pawn, "Pawn", string)
            string = re.sub(audio.language.rook, "Rook", string)
            string = re.sub(audio.language.knight, "Knight", string)
            string = re.sub(audio.language.bishop, "Bishop", string)
            string = re.sub(audio.language.queen, "Queen", string)
            string = re.sub(audio.language.king, "King", string)

        else:
            string = re.sub("Pawn", audio.language.pawn, string)
            string = re.sub("Rook", audio.language.rook, string)
            string = re.sub("Knight", audio.language.knight, string)
            string = re.sub("Bishop", audio.language.bishop, string)
            string = re.sub("Queen", audio.language.queen, string)
            string = re.sub("King", audio.language.king, string)

        return string

    @staticmethod
    def make_button(text, func, box):
        new_button = gtk.Button(text)
        new_button.connect('clicked', func)
        box.pack_start(new_button)
        return new_button

    def playing(self, player, lis):
        string = "%s\n\n" % player
        for i in lis:
            string = string + "%s\n" % i

        return self.translate(string, audio.language.babel)

    def change_idiom(self):
        idiom_index = audio.languages.index(audio.language)
        new_idiom = audio.languages[idiom_index - 1]

        audio.language = new_idiom
        self.idiom_button.set_label(new_idiom.name_of_the_button)

        audio.refresh_sts()
        self.refresh_gui()

    def __init__(self):
        self.window = gtk.Window()
        self.window.maximize()
        self.window.set_title("PyCT")

        self.main_box = gtk.HBox()

        self.box1 = gtk.VBox()
        self.box2 = gtk.VBox()
        self.box3 = gtk.VBox()
        self.box4 = gtk.HBox()
        self.box5 = gtk.VBox()
        self.box6 = gtk.HBox()
        self.box7 = gtk.HBox()
        self.box8 = gtk.HBox()

        self.main_box.pack_start(self.box1)
        self.main_box.pack_start(self.box2)
        self.main_box.pack_start(self.box3)
        self.box2.pack_start(self.box4)
        self.box2.pack_start(self.box5)
        self.box3.pack_start(self.box6)
        self.box3.pack_start(self.box7)
        self.box5.pack_start(self.box8)

        self.main_box.set_homogeneous(10)
        self.box3.set_homogeneous(10)
        self.box2.set_homogeneous(10)

        self.playing_w = gtk.Label(self.playing(audio.language.player_1, lists.WhitePieces))

        self.playing_b = gtk.Label(self.playing(audio.language.player_2, lists.BlackPieces))
        self.label = gtk.Label()

        self.image = gtk.Image()

        self.box4.pack_start(self.playing_w)
        self.box4.pack_start(self.playing_b)

        self.turn = gtk.Label("")
        self.player = gtk.Label("")
        self.move = gtk.Label("")

        self.box7.pack_start(self.turn)
        self.box7.pack_start(self.player)
        self.box7.pack_start(self.move)

        self.box7.set_homogeneous(10)

        self.start = self.make_button('Empezar', lambda (widget): gtk.main_quit(), self.box5)

        self.idiom_button = self.make_button(audio.language.name_of_the_button,
                                             lambda (widget): self.change_idiom(),
                                             self.box8)

        self.record = self.make_button('Grabar partida', lambda (widget): None, self.box5)

        self.exit = self.make_button('Salir', lambda (widget): exit(11), self.box5)

        self.window.add(self.main_box)

        self.window.show_all()
        self.window.connect('delete-event', self.destroy)

    @staticmethod
    def main():
        gtk.main()

    def refresh_playing(self, K, player):
        text_w = self.translate(self.playing_w.get_text(), 'english')
        text_b = self.translate(self.playing_b.get_text(), 'english')

        for i in text_w[7:].split("\n"):
            if i != "":
                if i not in lists.WhitePieces:
                    if type(K) == str and player == 1:
                        text_w = re.sub(i, self.translate(K, audio.language.babel), text_w)
                        K = None
                    else:
                        text_w = re.sub(i, "", text_w)

                elif len(re.findall(i, text_w)) > len(re.findall(i, str(lists.WhitePieces))):
                    text_w = re.sub(i, "", text_w, 1)

                else:
                    continue

        for j in text_b[6:].split("\n"):
            if j != "":
                if j not in lists.BlackPieces:
                    if type(K) == str and player == 2:
                        text_b = re.sub(j, self.translate(K, audio.language.babel), text_b)
                        K = None
                    else:
                        text_b = re.sub(j, "", text_b)

                elif len(re.findall(i, text_b)) > len(re.findall(i, str(lists.BlackPieces))):
                    text_b = re.sub(i, "", text_b, 1)

                else:
                    continue

        self.playing_w.set_text(self.translate(text_w, audio.language.babel))
        self.playing_b.set_text(self.translate(text_b, audio.language.babel))

    def refresh_gui(self):
        self.playing_w.set_text(self.playing(audio.language.player_1, lists.WhitePieces))
        self.playing_b.set_text(self.playing(audio.language.player_2, lists.BlackPieces))

        self.refresh_playing(None, None)

        self.start.set_label(audio.language.start)
        self.record.set_label(audio.language.record)
        self.exit.set_label(audio.language.out)

    def video(self, img):
        pix = gtk.gdk.pixbuf_new_from_file(img)
        pix = pix.scale_simple(430, 370, gtk.gdk.INTERP_BILINEAR)
        self.image.set_from_pixbuf(pix)

        self.box6.pack_start(self.image)

        self.window.show_all()

    def calibration_instructions(self):
        self.label.set_text(audio.language.calibration)
        self.label.set_justify(0)
        self.box1.pack_start(self.label)
        self.label.set_alignment(0.5, 0.04)
        self.window.show_all()

    def print_move(self, turn, player, mov):
        self.turn.set_alignment(0.1, 0.004)
        self.player.set_alignment(0.1, 0.004)
        self.move.set_alignment(0.1, 0.004)

        text_1 = self.turn.get_text()
        text_2 = self.player.get_text()
        text_3 = self.move.get_text()

        if len(text_1.split("\n")) >= 21:
            text_1 = ""
            text_2 = ""
            text_3 = ""

        turn_number = int(turn[-1])

        if turn_number == 1 and len(text_1) == 0 or text_1[-2] == "\n":
            pass
        elif turn_number == int(text_1[-2]):
            turn = ""

        player = audio.language.player_1 if int(player[-1]) == 1 else audio.language.player_2

        text_1 = text_1 + "%s\n" % turn
        text_2 = text_2 + "%s\n" % player
        text_3 = text_3 + "%s\n" % mov

        self.turn.set_text(text_1)
        self.player.set_text(text_2)
        self.move.set_text(text_3)

        self.window.show_all()

    def print_incorrect_move(self):
        self.label.set_text(self.label.get_text() + pieces.answer)
        self.label.set_justify(0)
        self.label.set_alignment(0.01, 0.04)
        self.window.show_all()

    def promote(self):
        global who_promote

        def end(widget):
            global who_promote
            who_promote = text.get_text()
            win.hide()
            gtk.main_quit()

        win = gtk.Window()
        win.set_size_request(500, 40)
        win.set_position(gtk.WIN_POS_CENTER)
        win.set_title(audio.language.promote_1)

        box = gtk.HBox()
        label = gtk.Label(audio.language.promote_2)
        text = gtk.Entry()

        button = gtk.Button('OK')
        button.connect('clicked', end)
        box.pack_start(label)
        box.pack_start(text)
        box.pack_start(button)

        win.add(box)
        win.show_all()
        gtk.main()

        return self.translate(who_promote, audio.language.babel)

    @staticmethod
    def movement(widget):
        def end(w):
            global pos0, pos1
            pos0 = text1.get_text()
            pos1 = text2.get_text()
            win.hide()
            gtk.main_quit()

        win = gtk.Window()
        win.set_size_request(500, 40)
        win.set_position(gtk.WIN_POS_CENTER)
        win.set_title(audio.language.move_1)

        box = gtk.HBox()
        label1 = gtk.Label(audio.language.move_2)
        label2 = gtk.Label(audio.language.move_3)
        text1 = gtk.Entry()
        text2 = gtk.Entry()

        button = gtk.Button('OK')
        button.connect('clicked', end)
        box.pack_start(label1)
        box.pack_start(text1)
        box.pack_start(label2)
        box.pack_start(text2)
        box.pack_start(button)

        win.add(box)
        win.show_all()
        gtk.main()

        global pos0, pos1
        return inv_change_position(pos0), inv_change_position(pos1)

    def sort_of_detection(self):
        def type_1(w):
            global sort
            sort = 'manual'
            win.hide()
            gtk.main_quit()

        def type_2(w):
            global sort
            sort = 'semi-automatic'
            win.hide()
            gtk.main_quit()

        def type_3(w):
            global sort
            sort = 'automatic'
            win.hide()
            gtk.main_quit()

        win = gtk.Window()
        win.set_size_request(500, 40)
        win.set_position(gtk.WIN_POS_CENTER)
        win.set_title(audio.language.sort_of_detection)

        box = gtk.HBox()

        manual = self.make_button(audio.language.sort_of_detection_1, type_1, box)
        semi_automatic = self.make_button(audio.language.sort_of_detection_2, type_2, box)
        automatic = self.make_button(audio.language.sort_of_detection_3, type_3, box)

        manual.set_tooltip_text(audio.language.detection_description_1)
        semi_automatic.set_tooltip_text(audio.language.detection_description_2)
        automatic.set_tooltip_text(audio.language.detection_description_3)

        win.add(box)
        win.show_all()
        gtk.main()

        global sort
        return sort


def OpenCV(winName, x, y, width, height):
        cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
        cv2.moveWindow(winName, x, y)
        cv2.resizeWindow(winName, width, height)
