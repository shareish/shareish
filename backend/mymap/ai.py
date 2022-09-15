import torch
from PIL import Image
from torchvision import transforms
from matplotlib import pyplot as plt
from torchvision import models
import os
import re
import pytesseract

model = torch.hub.load('pytorch/vision:v0.10.0', 'mobilenet_v3_large', weights=models.MobileNet_V3_Large_Weights.IMAGENET1K_V1)
model.eval()

def getImage(filename):
    RESIZE = transforms.Resize((256, 256))
    NORMALIZE = transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
    image = transforms.functional.pil_to_tensor(Image.open(filename).convert('RGB'))
    image = RESIZE.forward(image)
    image = image.unsqueeze(0) #create a mini-batch as expected by the model
    image = image.to(dtype=torch.float32)
    image = image/256
    image = NORMALIZE.forward(image)
    return image

def showImage(image):
    f = plt.figure()
    invTrans = transforms.Compose([ transforms.Normalize(mean = [ 0., 0., 0. ],
                                                        std = [ 1/0.229, 1/0.224, 1/0.225 ]),
                                    transforms.Normalize(mean = [ -0.485, -0.456, -0.406 ],
                                                        std = [ 1., 1., 1. ]),
                                    ])

    image = invTrans(image)
    image = image.squeeze(0)
    plt.imshow(image.transpose(0, 2).transpose(0, 1))
    plt.savefig("testdimage.png", format='png', bbox_inches='tight', dpi=80)
    plt.close(f)

def getCategories(filename):
    with open(filename, "r") as f:
        categories = [s.strip() for s in f.readlines()]
    return categories


def findOCR(filename):
    #predicted_result = pytesseract.image_to_string(Image.open(filename), lang='eng')
    predicted_result = pytesseract.image_to_string(Image.open(filename))
    clean_predicted_result = re.sub(r'\n+', '\n', predicted_result).strip()
    return clean_predicted_result


def findClass(filename):
    image = getImage(filename)

    #call pytesseract for OCR
    detected_text = findOCR(filename)
    print(detected_text)
    
    if torch.cuda.is_available():
        image = image.to('cuda')
        model.to('cuda')

    with torch.no_grad():
        output = model(image)

    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    
    categories = getCategories("./mymap/imagenet_classes.txt")

    top5_prob, top5_catid = torch.topk(probabilities, 5)
    for i in range(top5_prob.size(0)):
        print(str(categories[top5_catid[i]]) + " & " + str(top5_prob[i].item()) + "\\\\")

    return categories[top5_catid[0]],detected_text

# These two functions are implemented to plot the save the figures on files
# and to write the results on a tabular in a latex document
def plot_image_grid(image_datas, path):
    n = [500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000]
    _, axarr = plt.subplots(2,5)
    axarr[0,0].imshow(image_datas[1])
    axarr[0,1].imshow(image_datas[2])
    axarr[0,2].imshow(image_datas[3])
    axarr[0,3].imshow(image_datas[4])
    axarr[0,4].imshow(image_datas[5])
    axarr[1,0].imshow(image_datas[6])
    axarr[1,1].imshow(image_datas[7])
    axarr[1,2].imshow(image_datas[8])
    axarr[1,3].imshow(image_datas[9])
    axarr[1,4].imshow(image_datas[10])

    for i in range(2):
        for j in range(5):
            axarr[i, j].axis('off')
            axarr[i, j].set_title('N = ' + str(n[i*5 + j]))
    title = "1_3bis.svg"
    plt.savefig(os.path.join(path, title))
    plt.show()

def testModel():
    path = "../Testbedai/"
    for filename in os.listdir(path):
        file = os.path.join(path, filename)
        print("\\raisebox{-0.5\\totalheight}{\\includegraphics[width=0.3\\textwidth, height=30mm]{resources/TestModelImage/" + filename + "}} & \\begin{tabular}{c c}")
        print()
        print()
        findClass(file)
        print()
        print("\\end{tabular}\\\\")
        print()
        print("\\hline")

if __name__ == '__main__':
    testModel()
