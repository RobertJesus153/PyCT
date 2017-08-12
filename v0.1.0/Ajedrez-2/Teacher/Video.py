# -*- coding: utf-8 -*-

import cv2
import numpy as np
from Functions import *
from Window import OpenCV

puntos = []
rectify_points = []
esquinas = list

calibrated = False
sts = Sts('spanish')


class ChessBoard:

    def __init__(self, img, calibrate=True, esq=list, size=8):
        global calibrated
        self.patternSize = size + 1

        self.points_chessboard = np.ones((self.patternSize * self.patternSize, 3))
        self.points_chessboard[:, :2] = np.mgrid[0:self.patternSize, 0:self.patternSize].T.reshape(-1, 2)*100

        self.image = cv2.imread(img)

        self.points_image = np.zeros((2, self.patternSize * self.patternSize))

        if not calibrate:
            self.points_roi = esq

            self.transform = self.compute_warp(self.points_roi)

        else:

            cv2.namedWindow('Calibrate', cv2.WINDOW_NORMAL)
            cv2.moveWindow('Calibrate', 1100, -100)
            cv2.resizeWindow('Calibrate', 600, 500)
            self.points_roi = []
            cv2.setMouseCallback('Calibrate', self.mouse_click, self)
            cv2.imshow('Calibrate', self.image)

            cv2.waitKey(0)

            self.transform = self.compute_warp(self.points_roi)

            points_image = np.matmul(self.transform, self.points_chessboard.transpose())

            self.points_image[0, :] = points_image[0, :] / points_image[2, :]
            self.points_image[1, :] = points_image[1, :] / points_image[2, :]
            self.points_image = self.points_image.transpose()

            #
            # n = 0
            for point in self.points_image:
                cv2.circle(self.image, tuple(point.astype(int)), 5, (0, 255, 0), -1)
                puntos.append(point)
                # cv2.putText(self.image, str(n), tuple(point.astype(int)),
                #             fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=(0, 0, 255), fontScale=1)
                # n += 1

            #

            cv2.imshow('Calibrate', self.image)
            thread_starter(sts.say, [u'Si estás de acuerdo con los puntos, pulsa énter. Si no, escape'])
            k = cv2.waitKey(0) & 0xFF
            if k == 10:
                calibrated = True

            elif k == 27:
                calibrated = False

            if not calibrated:
                return

            n = 0
            for y in range(1, 9):
                for x in range(1, 9):
                    Lists.casillas[(x, y)] = [list(puntos[n].astype(int)),
                                              list(puntos[n + 1].astype(int)),
                                              list(puntos[n + 9].astype(int)),
                                              list(puntos[n + 10].astype(int))]
                    n += 1
                n += 1

    def mouse_click(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:

            self.points_roi.append((float(x), float(y)))
            Lists.esquinas.append((float(x), float(y)))

            cv2.circle(self.image, (x, y), 5, (255, 0, 0), -1)
            cv2.imshow('Calibrate', self.image)

    def compute_warp(self, points_roi):

        index_bl = 0
        index_br = self.patternSize - 1
        index_tr = (self.patternSize * self.patternSize) - 1
        index_tl = index_tr - self.patternSize + 1

        points_corners = self.points_chessboard[[index_bl, index_br, index_tr, index_tl], 0:2]

        points_roi = np.float32(points_roi)
        points_corners = np.float32(points_corners)

        H, status = cv2.findHomography(points_corners, points_roi)

        return H

    def rectify_crop(self, img_src, corners):
        #
        status, trf = cv2.invert(self.transform)
        #
        img_dst = cv2.warpPerspective(img_src, trf, (800, 800))
        #
        corners_hom = np.ones((4, 3))
        corners_hom[:, 0:2] = corners
        #
        corners_transformed = np.matmul(trf, corners_hom.transpose())
        #
        corners_result = np.zeros((2, 4))
        #
        corners_result[0, :] = corners_transformed[0, :] / corners_transformed[2, :]
        corners_result[1, :] = corners_transformed[1, :] / corners_transformed[2, :]
        #
        corners_result[corners_result < 0] = 0
        #
        corners_result = np.rint(corners_result)
        #
        r0 = (corners_result[0, 0] + corners_result[0, 2])/2
        r1 = (corners_result[0, 1] + corners_result[0, 3])/2
        c0 = (corners_result[1, 0] + corners_result[1, 1])/2
        c1 = (corners_result[1, 2] + corners_result[1, 3])/2
        #
        patchSize = (int(r1-r0), int(c1-c0))
        center = (int((r1+r0)/2), int((c1+c0)/2))
        #
        return cv2.getRectSubPix(img_dst, patchSize, center)

    #
    #
    #

    def rectify_chessboard(self, img):          # Image is not a file

        image = img

        points_image = np.zeros((2, self.patternSize * self.patternSize))

        points_roi = [(0, 800), (800, 800), (800, 0), (0, 0)]

        transform = self.compute_warp(points_roi)

        sub_points_image = np.matmul(transform, self.points_chessboard.transpose())

        points_image[0, :] = sub_points_image[0, :] / sub_points_image[2, :]
        points_image[1, :] = sub_points_image[1, :] / sub_points_image[2, :]
        points_image = points_image.transpose()

        #

        # n = 0
        for point in points_image:
            cv2.circle(image, tuple(point.astype(int)), 5, (0, 255, 0), -1)
            rectify_points.append(point)
            # cv2.putText(image, str(n), tuple(point.astype(int)),
            #            fontFace=cv2.FONT_HERSHEY_SIMPLEX, color=(0, 0, 255), fontScale=0.5)
            # n += 1
        #

        n = 0
        for y in range(1, 9):
            for x in range(1, 9):
                Lists.rectify_squares[(x, y)] = [list(rectify_points[n].astype(int)),
                                                 list(rectify_points[n + 1].astype(int)),
                                                 list(rectify_points[n + 9].astype(int)),
                                                 list(rectify_points[n + 10].astype(int))]
                n += 1
            n += 1

        # self.seleccionar(image)

    def rectify_image(self, img_src):
        status, trf = cv2.invert(self.transform)
        img_dst = cv2.warpPerspective(img_src, trf, (800, 800))

        M = cv2.getRotationMatrix2D((400, 400), 180, 1)

        img_dst = cv2.warpAffine(img_dst, M, (800, 800))
        img_dst = cv2.flip(img_dst, 1)

        return img_dst

    def seleccionar(self, image):
        sub_img = image
        while True:

            k = cv2.waitKey(1) & 0xFF

            if k == 27:
                cv2.destroyAllWindows()
                break

            if k == ord('c'):

                casilla = inv_cambio_posicion(raw_input("Casilla: "))

                for j in Lists.rectify_squares[casilla]:
                    cv2.circle(sub_img, tuple(j), 5, (0, 0, 255), -1)

            cv2.namedWindow('main',  cv2.WINDOW_NORMAL)
            cv2.imshow('main', sub_img)


class Calibration:
    def __init__(self, img):        # Image is a file
        self.tablero = ChessBoard(img)
        self.rectified_image = self.tablero.rectify_image(cv2.imread(img))
        self.tablero.rectify_chessboard(self.rectified_image)

    def rectify_image(self, img):       # Image is not a file
        self.rectified_image = self.tablero.rectify_image(img)
        return self.rectified_image

    def value(self):
        return calibrated


class Detection:
    def __init__(self, patch1, patch2, jugador):        # Images are files
        self.tablero = ChessBoard(patch1, False, Lists.esquinas)

        self.patch1 = patch1
        self.patch2 = patch2

        self.lista = []
        if jugador == 1:
            self.lista = Lists.casillasOcupadas['Blancas']
        elif jugador == 2:
            self.lista = Lists.casillasOcupadas['Negras']

    def Tablero(self):
        img_1 = self.tablero.rectify_image(cv2.imread(self.patch1))
        img_2 = self.tablero.rectify_image(cv2.imread(self.patch2))

        contornos, umbral, resta = self.Resta(img_1, img_2)
        """
        cv2.imshow('umbral', umbral)
        cv2.imshow('resta', resta)

        k = cv2.waitKey(0)

        if k == 27:
            cv2.destroyAllWindows()
            exit(11)

        cv2.destroyWindow('umbral')
        cv2.destroyWindow('resta')
        """

        areas = []
        for c in contornos:
            if cv2.contourArea(c) > 1000:
                areas.append(cv2.contourArea(c))

        if len(areas) == 2:
            max_areas = areas

        elif len(areas) < 2:
            return self.Casillas()

        else:
            areas.sort()
            max_areas = [areas[len(areas) - 1], areas[len(areas) - 2]]

        max_contornos = []
        for c in contornos:
            for a in max_areas:
                if cv2.contourArea(c) == a:
                    max_contornos.append(c)

        casillas = []
        pts = []

        for c in max_contornos:
            x, y, w, h = cv2.boundingRect(c)

            cv2.rectangle(img_2, (x, y), (x + w, y + h), (0, 255, 0), 2)

            centro = ((2 * x + w) / 2, (2 * y + h) / 2)
            pts.append(centro)

            cv2.circle(img_2, centro, 3, (255, 0, 0))

            k = cv2.waitKey(1)
            if k == 27:
                cv2.destroyAllWindows()
                exit(11)

            for punto in pts:
                for i in Lists.rectify_squares:
                    j = Lists.rectify_squares[i]

                    inf_izq = tuple(j[2])
                    sup_der = tuple(j[1])

                    if inf_izq[0] < punto[0] and inf_izq[1] < punto[1] and \
                       sup_der[0] > punto[0] and sup_der[1] > punto[1]:

                        if i not in casillas:
                            casillas.append(i)
        """
        cv2.imshow('%s' % img_2, img_2)
        cv2.imshow('umbral', umbral)
        cv2.imshow('resta', resta)

        k = cv2.waitKey(0)

        if k == 27:
            cv2.destroyAllWindows()
            exit(11)

        cv2.destroyWindow('%s' % img_2)
        cv2.destroyWindow('umbral')
        cv2.destroyWindow('resta')
        """
        if len(casillas) == 2:
            pos0, pos1 = give_values(tuple, 2)

            for casilla in casillas:
                if casilla in self.lista:
                    pos0 = casilla
                else:
                    pos1 = casilla

            try:
                print pos0[0], pos0[1], pos1[0], pos1[1]
                return pos0, pos1

            except TypeError:
                return self.Casillas()

        else:
            return self.Casillas()

    def Casillas(self):
        print "casillas"
        casillas = {}
        for y in range(1, 9):
            for x in range(1, 9):
                thread = thread_starter(self.Sub_Casillas, [x, y, casillas])

                if (x, y) == (8, 8):
                    thread.join()
        areas = []
        for casilla in casillas:
            areas.append(casillas[casilla])
        areas.sort()
        max_areas = [areas[len(areas) - 1], areas[len(areas) - 2]]

        pos0 = tuple
        pos1 = tuple

        for casilla in casillas:
            if casillas[casilla] in max_areas:
                if casilla in self.lista:
                    pos0 = casilla
                else:
                    pos1 = casilla

        try:
            print pos0[0], pos0[1], pos1[0], pos1[1]
            return pos0, pos1

        except TypeError:
            print casillas
            print pos0, pos1
            return None, None

    def Sub_Casillas(self, x, y, dic):
        corners = np.array(Lists.casillas[(x, y)], np.float32)

        casilla_1 = self.tablero.rectify_crop(cv2.imread(self.patch1), corners)
        casilla_2 = self.tablero.rectify_crop(cv2.imread(self.patch2), corners)

        contornos, umbral, resta = self.Resta(casilla_1, casilla_2)

        for c in contornos:
            if cv2.contourArea(c) > 400:
                if (x, y) not in dic:
                    dic[(x, y)] = cv2.contourArea(c)

                elif cv2.contourArea(c) > dic[(x, y)]:
                    dic[(x, y)] = cv2.contourArea(c)

    @staticmethod
    def Resta(img_1, img_2):
        kernel = np.ones((5, 5), np.uint8)

        gris_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2GRAY)
        gris_2 = cv2.cvtColor(img_2, cv2.COLOR_BGR2GRAY)

        resta = cv2.absdiff(gris_1, gris_2)

        umbral = cv2.threshold(resta, 20, 255, cv2.THRESH_BINARY)[1]
        umbral = cv2.morphologyEx(umbral, cv2.MORPH_OPEN, kernel)
        umbral = cv2.dilate(umbral, kernel, iterations=2)
        umbral = cv2.morphologyEx(umbral, cv2.MORPH_CLOSE, kernel)

        contornos_img = umbral.copy()
        im, contornos, hierarchy = cv2.findContours(contornos_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        return contornos, umbral, resta


class Camera:
    def __init__(self):
        self.choosing = True
        self.election = 0

        self.cam_1 = cv2.VideoCapture(0)

        self.second_camera = False
        if cv2.VideoCapture(1).isOpened():

            from Synthesizer import Sts
            sts = Sts('spanish')

            thread_starter(prevent_auido_error, (u'Selecciona la cámara que vayas a usar.',))

            OpenCV('camera 1', 200, 100, 500, 500)
            OpenCV('camera 2', 700, 100, 500, 500)
            self.cam_2 = cv2.VideoCapture(1)
            self.second_camera = True

    def choose(self):
        while True:
            if self.choosing:
                if self.second_camera:
                    ret_1, frame_1 = self.cam_1.read()
                    ret_2, frame_2 = self.cam_2.read()

                    cv2.imshow('camera 1', frame_1)
                    cv2.imshow('camera 2', frame_2)

                    cv2.setMouseCallback('camera 1', self.election_1)
                    cv2.setMouseCallback('camera 2', self.election_2)

                    k = cv2.waitKey(1) & 0xFF
                    video_exit(k)

                    if k == 27:
                        cam = cv2.VideoCapture(1)
                        cv2.destroyAllWindows()
                        break

                else:
                    self.choosing = False
            else:
                cv2.destroyAllWindows()
                self.cam_1.release()
                return self.election

    def election_1(self, event, x, y, flags, param):
        self.sub_election(event, 0)

    def election_2(self, event, x, y, flags, param):
        self.sub_election(event, 1)

    def sub_election(self, event, num):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.choosing = False
            self.election = num
            self.cam_1.release()
            self.cam_2.release()


if __name__ == '__main__':
    global calibrated
    calibration = Calibration('DSCN9031.JPG')
    print calibrated
