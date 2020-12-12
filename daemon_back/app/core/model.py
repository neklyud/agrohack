import cv2
import albumentations as A
from albumentations.pytorch import ToTensorV2
import torch


class Model(object):
    def __init__(self,
                 model_path='best_accuracy.pth',
                 size=800,
                 img_path='img.jpg',
                 cuda=True):

        self.img_path = img_path
        # определяем наличие куды, если нет ее, вычисляем на проце
        if torch.cuda.is_available() and cuda:
            self.device = 'cuda'
        else:
            self.device = 'cpu'
        # загружаем модель
        self.inference = torch.load(model_path).to(self.device)
        # указываем препроцессинг
        self.transforms = A.Compose([
            A.Resize(height=size, width=size, p=1.0),
            A.Normalize(p=1.0),
            ToTensorV2(p=1.0),
        ])

    def predict(self):
        # загружаем изображение  по пути, указанном в inite.
        # альтернативно можно сразу в аргумент фнкции подавать изображение (в формате numpy.ndarray)
        img = cv2.imread(self.img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        transformed = self.transforms(image=img)
        img = transformed['image'].unsqueeze(0).to(self.device)
        pred = self.inference(img).detach().cpu()
        # выдает значение 1, если растение больное, 0 - здоровое. Формат на выходе numpy.ndarray
        return int(torch.round(torch.sigmoid(pred)).numpy())

if __name__ == "__main__":
    inference = Model()
    output = inference.predict()
    print('Здоровое' if output != 1 else 'Больное')
