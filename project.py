import cv2
import os
import sys
import json
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import imutils


class Paper:
    def __init__(self, name, width, height, paper_id, paper_id_pos_width, paper_id_pos_height):
        self.name = name
        self.width = width
        self.height = height
        self.paper_id = paper_id
        self.paper_id_pos_width = paper_id_pos_width
        self.paper_id_pos_height = paper_id_pos_height
        self.sections = []

    def add_section(self, s):
        self.sections.append(s)

    # def print(self):
    #     print(self.name, self.width, self.height, self.paper_id, self.paper_id_pos_width, self.paper_id_pos_height,
    #           " # of sections ", len(self.sections))
    #     for s in self.sections:
    #         s.print()

    # def mark_on_paper(self, img, shiftx, shifty):
    #     for s in self.sections:
    #         s.mark_on_image(img, shiftx, shifty, self.width, self.height)


class Section:
    def __init__(self, name, x, y, width, height, orientation, part_width, part_height):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.orientation = orientation
        self.part_width = part_width
        self.part_height = part_height
        self.parts = []

    def add_part(self, part):
        self.parts.append(part)

    # def print(self):
    #     print(self.name, self.x, self.y, self.orientation, self.part_width, self.part_height,
    #           " # of parts ", len(self.parts))
    #     for p in self.parts:
    #         p.print()
    #
    # def mark_on_image(self, img, shiftx, shifty, paper_w, paper_h):
    #     for p in self.parts:
    #         p.mark_on_image(img, shiftx, shifty, paper_w, paper_h)


class Part:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.bubbles_list = []

    def add_bubble(self, b, partname):
        self.bubbles_list.append([b, partname])

    # def print(self):
    #     print("part ", self.name, self.x, self.y,
    #           " # of bubbles ", len(self.bubbles_list))
    #     for b in self.bubbles_list:
    #         b.print()
    #
    # def mark_on_image(self, img, shiftx, shifty, paper_w, paper_h):
    #     for b, p in self.bubbles_list:
    #         b.mark_on_image(img, shiftx, shifty, paper_w, paper_h)


class Bubble:
    def __init__(self, name, x, y, width, height, partname):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.partname = partname

    def isBubbleSelected(self, img, x, y, shiftx, shifty, width, height):
        x = x + shiftx
        y = y + shifty
        selected = img[y:y + height, x:x + width]
        minimum = 300
        total = cv2.countNonZero(selected)
        if total >= minimum:
            return False
        return True

    def print(self):
        return self.partname, self.name

    # def mark_on_image(self, img, shiftx, shifty, paper_w, paper_h):
    #     x_1 = self.x + shiftx
    #     y_1 = self.y + shifty
    #     x_2 = x_1 + self.width * (img.shape[1] / paper_w)
    #     y_2 = y_1 + self.height * (img.shape[0] / paper_h)
    #     cv2.rectangle(img, (int(x_1), int(y_1)), (int(x_2), int(y_2)), (0, 255, 0), 1)

        # def count_on_pixels(self, img,  paper_w, paper_h):
        #
        #     x_1 = self.x * (img.shape[1] / paper_w)
        #     y_1 = self.y * (img.shape[0] / paper_h)
        #     x_2 = x_1 + self.width * (img.shape[1] / paper_w)
        #     y_2 = y_1 + self.height * (img.shape[0] / paper_h)
        #     selected = img[y_1:y_1 + y_2, x_1:x_1 + x_2]
        #     minimum = 1500
        #     total = cv2.countNonZero(selected)


class Adjust:
    def detect_corners(self, imgGray):
        imgThresh = cv2.threshold(imgGray, 150, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        img_cnts = cv2.findContours(imgThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        img_cnts = img_cnts[0] if imutils.is_cv2() else img_cnts[1]
        corner = []
        coorcorner = []
        for c in img_cnts:
            x, y, w, h = cv2.boundingRect(c)
            ar = h / float(w)
            if w >= 9 and w <= 12 and h >= 9 and h <= 12 and ar >= 0.9 and ar <= 1.1:
                if y <= 150:
                    corner.append(c)
                    coorcorner.append([x, y + h])
        coorcorner.sort(reverse=0)
        print(coorcorner)
        shiftx = coorcorner[0][0]
        shifty = coorcorner[0][1]
        return shiftx, shifty


class Answer:
    def __init__(self, img, description):
        self.img = img
        self.description = description

    def get_answers(self):
        seatNumber = []
        modelNumber = 0
        answers = []

        img = cv2.imread(self.img, cv2.IMREAD_GRAYSCALE)
        ret, bin_img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
        adjust = Adjust()
        shiftx, shifty = adjust.detect_corners(img)
        with open(self.description) as json_file:
            data = json.load(json_file)
            paper = Paper(data['name'],
                          data['width'],
                          data['height'],
                          data['paperId'],
                          data['paperIdPosition']['width'],
                          data['paperIdPosition']['height'])
        for section in data['sections']:
            sec_obj = Section(section['name'],
                              section['x'],
                              section['y'],
                              section['width'],
                              section['height'],
                              section['orientation'],
                              section['partWidth'],
                              section['partHeight'])
            for part in section['parts']:
                part_obj = Part(part['name'],
                                part['x'],
                                part['y'])
                test_answers = []
                for bubble in part['bubbles']:
                    bubble_obj = Bubble(bubble['name'],
                                        bubble['x'],
                                        bubble['y'],
                                        section['bubbleWidth'],
                                        section['bubbleWidth'], part['name'])
                    partname, bubblename = bubble_obj.print()
                    isSelected = bubble_obj.isBubbleSelected(bin_img, bubble['x'],
                                                             bubble['y'],
                                                             shiftx, shifty,
                                                             section['bubbleWidth'],
                                                             section['bubbleWidth'])
                    if section['name'] == 'modelNumber':
                        if isSelected == True:
                            modelNumber = bubblename
                    elif section['name'] == 'seatNumber':

                        if isSelected == True:
                            seatNumber.append(bubblename)
                    elif section['name'] == 'questionBlock':

                        if isSelected == True:
                            test_answers.append(bubblename)

                    part_obj.add_bubble(bubble_obj, part['name'])
                    del bubble_obj
                answers.append([partname, test_answers])
                sec_obj.add_part(part_obj)
                del part_obj
            paper.add_section(sec_obj)
            del sec_obj
            seatNumberString = "".join(str(x) for x in seatNumber)
        return seatNumberString, modelNumber, answers

    def evaluate(self, answer, model):
        mark = int()
        for i in range(len(answer)):
            for x in answer[i][1]:
                for y in model[i][1]:
                    if len(model[i][1]) > 0:
                        if x == y:
                            submark = 1 / len(answer[i][1])
                            mark = mark + submark
        return mark


# import time
#
# start = time.clock()
# img = '1.jpg'
# file = 'fi.json'
# answer_obj = Answer(img, file)
# seatNumber, modelNumber, Sanswers = answer_obj.get_answers()
# answer_obj1 = Answer(img, file)
# seatNumber1, modelNumber1, Manswers = answer_obj.get_answers()
# mark = answer_obj.evaluate(Sanswers, Manswers)
# print(seatNumber, mark)
# print(Sanswers)
