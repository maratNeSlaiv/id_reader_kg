from typing import Any
import torch
from PIL import Image
from reader.parseq.parseq_main_file_1 import SceneTextDataModule
import easyocr
import re
import os
import cv2
from tools.multi_reading_via_parseq import mnogorazovyi_chitatel
from detector.id_detection_script import detect_id_cards

def parsing_results_and_confidences(easyocr_results, parseq_results):
    easyocr = []
    easyocr_confs = []
    parseq = []
    parseq_confs = []

    for i in easyocr_results:
        easyocr.append(i[1])
        easyocr_confs.append(i[2])

    for i in parseq_results:
        parseq.append(i[0])
        parseq_confs.append(i[1])

    return easyocr, easyocr_confs, parseq, parseq_confs

def find_necessary(easyocr_results, parseq_results):
    from tools.dictionaries import pattern_list, words_to_skip
    
    easyocr, easyocr_confs, parseq, parseq_confs = parsing_results_and_confidences(easyocr_results, parseq_results)
    # easyocr и parseq это лист с словами
    # easyocr_confs это лист с вероятностями к всему выражению (каждый лист соответсвует слову в easyocr)
    # parseq_confs это лист с листами с вероятностями к каждой букве (каждый больший лист соотвествует слову в parseq)
    
    necessary = []
    for i,j in zip(easyocr, parseq):
        if not (j.lower() in words_to_skip or i.lower() in words_to_skip):
            if re.fullmatch(pattern_list['ИНН'], j):
                # print('INN is necessary', j)
                necessary.append(j)
                continue

            if re.fullmatch(pattern_list['otchestvo'], i):
                # print('Otchestvo is necessary', i)
                necessary.append(i)
                continue

            if re.fullmatch(r'^[A-Z]+$', i) and re.fullmatch(r'^[A-Z]+$', j):
                # print('english letters are necessary', j)
                necessary.append(j)
                continue

            if re.fullmatch(pattern_list['authority'], i) or re.fullmatch(pattern_list['authority'], j):
                # print('authority is necessary', j)
                necessary.append(j)
                continue
            
            if re.fullmatch(pattern_list['date_pointed'], i) or re.fullmatch(pattern_list['date_pointed'], j) or re.fullmatch(pattern_list['date_unpointed'], i) or re.fullmatch(pattern_list['date_unpointed'], j):
                # print('date is necessary', j)
                necessary.append(j)
                continue
            
            if re.fullmatch(pattern_list['gender'], i) or re.fullmatch(pattern_list['gender'], j):
                # print('gender is necessary', j)
                necessary.append(j)
                continue

            if re.fullmatch(pattern_list['passport_no'], i) or re.fullmatch(pattern_list['passport_no'], j):
                # print('passport number is necessary', j)
                necessary.append(j)
                continue
     
    return necessary

def odna_kartinka(img, parseq, img_transform, reader):
    # предсказание моделей
    easyocr_result = reader.readtext(img)
    pil_img = Image.fromarray(img).convert('RGB')
    coords = []
    for i in range(len(easyocr_result)):
        coords.append(easyocr_result[i][0])
    parseq_results = mnogorazovyi_chitatel(pil_img, coords, parseq, img_transform)

    necessary = find_necessary(easyocr_result, parseq_results)
    return necessary


def mnogo_kartinok(img_folder, parseq, img_transform, reader, detector):
    paths = os.listdir(img_folder)

    # Прогрузка моделей
    necessaries = []
    for i in paths:
        if not i == '.DS_Store':
            # Загрузка изображения
            path = img_folder + i
            print('Current image is:', i)
            img = cv2.imread(path)

            # Нахождение айди карт
            id_cards, num_found = detect_id_cards(img, detector)

            # Чтение
            for id_card in id_cards:
                necessary = odna_kartinka(id_card, parseq, img_transform, reader)
                necessaries.append(necessary)
    return necessaries