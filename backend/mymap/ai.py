import os
import re

import pytesseract
import torch
import json
from PIL import Image
from matplotlib import pyplot as plt
from torchvision import models, transforms
from pyzbar.pyzbar import decode
import requests
from CRAFT.CRAFT_shareish import CRAFT_txt

model = torch.hub.load(
    'pytorch/vision:v0.10.0', 'mobilenet_v3_large',
    weights=models.MobileNet_V3_Large_Weights.IMAGENET1K_V1
    )
model.eval()


print("Loading imageNet classes and mapped categories")
with open("./mymap/imagenet_class_index.json", "r") as jsonfile:
    categories = json.load(jsonfile)



def getImage(filename):
    print(filename)
    resize = transforms.Resize((256, 256))
    normalize = transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
    img = Image.open(filename).convert('RGB')
    image = transforms.functional.pil_to_tensor(img)
    print(img.size)
    image = resize.forward(image)
    image = image.unsqueeze(0)  # create a mini-batch as expected by the model
    image = image.to(dtype=torch.float32)
    image = image / 256
    image = normalize.forward(image)
    return image


def showImage(image):
    f = plt.figure()
    inv_trans = transforms.Compose(
        [transforms.Normalize(
            mean=[0., 0., 0.],
            std=[1 / 0.229, 1 / 0.224, 1 / 0.225]
            ),
         transforms.Normalize(
             mean=[-0.485, -0.456, -0.406],
             std=[1., 1., 1.]
             ),
         ]
        )

    image = inv_trans(image)
    image = image.squeeze(0)
    plt.imshow(image.transpose(0, 2).transpose(0, 1))
    plt.savefig("testdimage.png", format='png', bbox_inches='tight', dpi=80)
    plt.close(f)


def findOCR(filename):
    # predicted_result = pytesseract.image_to_string(Image.open(filename), lang='eng')
    predicted_result = pytesseract.image_to_string(Image.open(filename))
    clean_predicted_result = re.sub(r'\n+', '\n', predicted_result).strip()
    return clean_predicted_result


def findClass(filename):
    image = getImage(filename)

    if torch.cuda.is_available():
        image = image.to('cuda')
        model.to('cuda')

    with torch.no_grad():
        output = model(image)

    probabilities = torch.nn.functional.softmax(output[0], dim=0)

    top5_prob, top5_catid = torch.topk(probabilities, 5)

    # call pytesseract for OCR
    detected_text = findOCR(filename)

    response = {
        'probabilities': [],
        'detected_text': detected_text
    }

    for i in range(top5_prob.size(0)):
        current_item = categories[str(top5_catid[i].item())]
        response['probabilities'].append({
            'class': current_item[1],
            'category': current_item[2],
            'probability': top5_prob[i].item()
        })

    return response

def BarcodePicture(image):

    image = Image.open(image)
    decodedObjects = decode(image)

    for obj in decodedObjects:
        if obj.type == "EAN13" or obj.type == "EAN10":
            ISBN = obj.data.decode("utf-8")


            url = "https://openlibrary.org/api/books?bibkeys=ISBN:" + ISBN + "&format=json&jscmd=data"
            
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                for obj in data:
                    title = data[obj]["title"]
                    author = data[obj]["authors"][0]["name"]

                MetaData = {"title": title, "author": author, "ISBN": ISBN}

                # Only return the first book type ISBN recognised
                return 1, MetaData


    return 0, 0

def BookPicture(image):

    response = findClass(image)

    for obj in response["probabilities"]:
        if obj["class"] == "book_jacket" or obj["class"] == "comic_book" or 1==1:# for testing because hardly recognises book_jacket or comic_book
            response, confidenceScore = CRAFT_txt(image)
            # response is a tab of words, add them all together with a space
            
            if response == []:
                return 0, 0
            else:
                response = " ".join(response)
                
                # query openlibrary for the book in the same form as https://openlibrary.org/search.json?q=the+lord+of+the+rings
                url = "https://openlibrary.org/search.json?q=" + response.replace(" ", "+")

                response = requests.get(url) # is quite bad at recognising the books
                if response.json()["numFound"] != 0:
                    response = response.json()["docs"][0] # only the first result is returned
                    title = response["title"]
                    author = response["author_name"][0]
                    ISBN = response["isbn"][0]

                metaData = {"title": title, "author": author, "ISBN": ISBN}
                
                return 1, metaData
    return 0, 0

def RegularPicture(image):
    response, confidenceScore = CRAFT_txt(image)
    if response == []:
        return 0, 0
    else:
        metaData = {"text": response}
        return 1, metaData
    return 0, 0

# These two functions are implemented to plot the save the figures on files
# and to write the results on a tabular in a latex document
def plot_image_grid(image_datas, path):
    n = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
    _, axarr = plt.subplots(2, 5)
    axarr[0, 0].imshow(image_datas[1])
    axarr[0, 1].imshow(image_datas[2])
    axarr[0, 2].imshow(image_datas[3])
    axarr[0, 3].imshow(image_datas[4])
    axarr[0, 4].imshow(image_datas[5])
    axarr[1, 0].imshow(image_datas[6])
    axarr[1, 1].imshow(image_datas[7])
    axarr[1, 2].imshow(image_datas[8])
    axarr[1, 3].imshow(image_datas[9])
    axarr[1, 4].imshow(image_datas[10])

    for i in range(2):
        for j in range(5):
            axarr[i, j].axis('off')
            axarr[i, j].set_title('N = ' + str(n[i * 5 + j]))
    title = "1_3bis.svg"
    plt.savefig(os.path.join(path, title))
    plt.show()


def testModel():
    path = "../Testbedai/"
    for filename in os.listdir(path):
        file = os.path.join(path, filename)
        print(
            "\\raisebox{-0.5\\totalheight}{\\includegraphics[width=0.3\\textwidth, height=30mm]{resources/TestModelImage/" + filename + "}} & \\begin{tabular}{c c}"
            )
        print()
        print()
        findClass(file)
        print()
        print("\\end{tabular}\\\\")
        print()
        print("\\hline")


if __name__ == '__main__':
    testModel()
