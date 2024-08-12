import numpy as np
import sys
import re
from tools.programm_test import odna_kartinka, mnogo_kartinok
from detector.id_detection_script import detect_id_cards
from ultralytics import YOLO
import torch
import easyocr
import cv2
from reader.parseq.parseq_main_file_1 import SceneTextDataModule
from tools.formatting import post_formatting

if __name__ == '__main__':
    parseq = torch.hub.load('baudm/parseq', 'parseq', pretrained=True).eval()
    img_transform = SceneTextDataModule.get_transform(parseq.hparams.img_size)
    reader = easyocr.Reader(['ru','en'])
    detector_path = '/Users/maratorozaliev/Desktop/id_reader/detector/ID_detection.pt'
    detector = YOLO(detector_path)
    
    # много картинок в папке (для тестов только)
    # folder = '/Users/maratorozaliev/Desktop/back_views/'
    # pustota = mnogo_kartinok(folder, parseq, img_transform, reader, detector)

    # одну картинку чекнуть
    image_path = '/Users/maratorozaliev/Desktop/front_views/ID2323288.png'
    image = cv2.imread(image_path)
    id_cards, num_found = detect_id_cards(image, detector)

    print('Current image is:', image_path)
    necessaries = set()
    for id_card in id_cards:
        necessary = odna_kartinka(id_card, parseq, img_transform, reader)
        for necessity in necessary:
            necessaries.add(necessity)

    necessaries = post_formatting(necessaries)
    print(necessaries)
    sys.exit('Концовка')

