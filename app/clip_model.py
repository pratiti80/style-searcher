import clip
import torch
from PIL import Image

model, preprocess = clip.load("ViT-B/32")

image = preprocess(Image.open("app/PEGASUS+EASYON.png")).unsqueeze(0)
text = clip.tokenize(["a photo of sneakers","a photo of a laptop"])

with torch.no_grad():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text)
    similarity = (image_features @ text_features.T).softmax(dim=-1)
    
print(similarity)

