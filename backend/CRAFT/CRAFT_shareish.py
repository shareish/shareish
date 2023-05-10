
import os
import argparse
from .BBoxes import copyStateDict
import string
import torch
import torch.backends.cudnn as cudnn
from PIL import Image

import cv2
import numpy as np
from .BBoxes import test_net
from .imgproc import loadImage
from .file_utils import get_files

from .utils import CTCLabelConverter, AttnLabelConverter
from .model import Model
from .craft import CRAFT
from .dataset import AlignCollate, ShareishDataset
import torch.nn.functional as F
import cv2
def str2bool(v):
    return v.lower() in ("yes", "y", "true", "t", "1")




def Boxes(filename):
    #CRAFT
    base = os.path.dirname(os.path.abspath(__file__))

    model_pretrained = "weights/craft_mlt_25k.pth"
    model_pretrained = os.path.join(base, model_pretrained)
    text_threshold = 0.7
    low_text = 0.4
    link_threshold = 0.4
    cuda = False
    canvas_size = 1280
    mag_ratio = 1.5
    #Image_folder = "D:/Shareish/CRAFT/Git_shareish-main/Git_shareish-main/Image_shareish/"
    image = Image.open(filename).convert('RGB')


    #image_path, _, _ = get_files(Image_folder)


    #image_name = os.path.basename(image_path[0])

    model = CRAFT()    

    if cuda:
        model = model.cuda()
        model.load_state_dict(copyStateDict(torch.load(model_pretrained)))
        model = torch.nn.DataParallel(model)
        cudnn.benchmark = False
    else:
        model.load_state_dict(copyStateDict(torch.load(model_pretrained, map_location='cpu')))

    model.eval()

    image = np.array(image)

    image = np.ascontiguousarray(image)
    def str2bool(v):
        return v.lower() in ("yes", "y", "true", "t", "1")

    #CRAFT


    bboxes, polys, score_text, det_scores = test_net(model, image, text_threshold, link_threshold, low_text, cuda, False)

    bbox_score = []

    for box_num in range(len(bboxes)):
          key = det_scores[box_num]
          bbox = bboxes[box_num]
          item = [key, bbox]

          bbox_score.append(item)

    #image = cv2.imread(image_path[0])
    image_name = ""

    return image_name , image, bbox_score, polys, score_text, det_scores

def crop(pts, image):
  """
  Takes inputs as 8 points
  and Returns cropped, masked image with a white background
  """
  rect = cv2.boundingRect(pts)
  x,y,w,h = rect
  cropped = image[y:y+h, x:x+w].copy()
  # show cropped image


  pts = pts - pts.min(axis=0)
  mask = np.zeros(cropped.shape[:2], np.uint8)
  cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)
  dst = cv2.bitwise_and(cropped, cropped, mask=mask)
  bg = np.ones_like(cropped, np.uint8)*255
  cv2.bitwise_not(bg,bg, mask=mask)
  dst2 = bg + dst

  return dst2

def generate_words(image_name, score_bbox, image):
  words = []                  
  for bbox_coords in score_bbox:

    if bbox_coords[0] != 0:
      l_t = bbox_coords[1][0][0]
      t_l = bbox_coords[1][0][1]
      r_t = bbox_coords[1][1][0]
      t_r = bbox_coords[1][1][1]
      r_b = bbox_coords[1][2][0]
      b_r = bbox_coords[1][2][1]
      l_b = bbox_coords[1][3][0]
      b_l = bbox_coords[1][3][1]

      pts = np.array([[int(l_t), int(t_l)], [int(r_t) ,int(t_r)], [int(r_b) , int(b_r)], [int(l_b), int(b_l)]])
      
      if np.all(pts) > 0:
        
        word = crop(pts, image)
      words.append(word)
  return words

def get_words(filename):

    image_name, image, bbox_score, polys, score_text, det_scores = Boxes(filename)

    # disct to dataframe

    image_name = image_name.strip('.jpg')

    words = generate_words(image_name, bbox_score, image)
    return words, image

def generate_text(image, words):



    cudnn.benchmark = True
    cudnn.deterministic = True


    converter = CTCLabelConverter("0123456789abcdefghijklmnopqrstuvwxyz")

    num_class = len(converter.character)


    model = Model(num_class)
    device = torch.device('cpu')
    model = torch.nn.DataParallel(model).to(device)

    base = os.path.dirname(os.path.abspath(__file__))
    saved_model = os.path.join(base, "None-VGG-BiLSTM-CTC.pth")

    model.load_state_dict(torch.load(saved_model, map_location='cpu'))
    
    AlignCollate_demo = AlignCollate(imgH=32, imgW=100)# PAD MISSING ?
    demo_data = ShareishDataset(words, image)  
    demo_loader = torch.utils.data.DataLoader(
        demo_data, batch_size=192,
        shuffle=False,
        collate_fn=AlignCollate_demo, pin_memory=True)

    model.eval()
    with torch.no_grad():
        for image_tensors, _ in demo_loader:

            batch_size = image_tensors.size(0)

            image = image_tensors.to(device)

            # For max length prediction
            length_for_pred = torch.IntTensor([25] * batch_size).to(device)
            text_for_pred = torch.LongTensor(batch_size, 25 + 1).fill_(0).to(device)


            preds = model(image, text_for_pred)
            preds_size = torch.IntTensor([preds.size(1)] * batch_size)
            # Select max probabilty (greedy decoding) then decode index to character
            _, preds_index = preds.max(2)
            #preds_index = preds_index.view(-1)
            preds_str = converter.decode(preds_index, preds_size)



            preds_prob = F.softmax(preds, dim=2)
            preds_max_prob, _ = preds_prob.max(dim=2)
            predictions = []
            confidence_scores = []
            for  pred, pred_max_prob in zip(preds_str, preds_max_prob):

                # calculate confidence score (= multiply of pred_max_prob)
                confidence_score = pred_max_prob.cumprod(dim=0)[-1]


                predictions.append(pred)
                confidence_scores.append(confidence_score)

    # ATTENTION : prediction only for 1 image
    return predictions, confidence_scores
        

def CRAFT_txt(filename):
    words, image = get_words(filename)
    res, conf = generate_text(image, words)
    return res, conf

if __name__ == '__main__':

    CRAFT('test.jpg')
