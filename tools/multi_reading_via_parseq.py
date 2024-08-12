from PIL import Image

def mnogorazovyi_chitatel(img : Image, coords, parseq, img_transform):
    parseq_results = []
    for i in coords:
        # print('coords of image:', int(i[0][0]), int(i[0][1]), int(i[2][0]), int(i[2][1]))
        current_img = img.crop((int(i[0][0]), int(i[0][1]), int(i[2][0]), int(i[2][1])))
        label, confidence = chitatel(current_img, parseq, img_transform)
        parseq_results.append([label, confidence])

    return parseq_results 

def chitatel(img, parseq, img_transform):
    
    img = img_transform(img).unsqueeze(0)
    logits = parseq(img)
    pred = logits.softmax(-1)

    label, confidence = parseq.tokenizer.decode(pred)
    # print('Decoded label = {}'.format(label[0]))
    # print('Found confidences = {}'.format(confidence))
    return label[0], confidence
