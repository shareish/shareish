import torch
from PIL import Image
from torchvision import transforms
from matplotlib import pyplot as plt
from torchvision import models

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
    
def findClass(filename):
    image = getImage(filename)

    # move the input and model to GPU for speed if available
    if torch.cuda.is_available():
        image = image.to('cuda')
        model.to('cuda')

    with torch.no_grad():
        output = model(image)

    # Tensor of shape 1000, with confidence scores over Imagenet's 1000 classes
    # The output has unnormalized scores. To get probabilities, you can run a softmax on it.
    probabilities = torch.nn.functional.softmax(output[0], dim=0)

    # Read the categories
    
    categories = getCategories("imagenet_classes.txt")

    # Show top categories per image
    top5_prob, top5_catid = torch.topk(probabilities, 5)
    for i in range(top5_prob.size(0)):
        print(categories[top5_catid[i]], top5_prob[i].item())

    return categories[top5_catid[0]]