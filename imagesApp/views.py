from django.shortcuts import render
from .models import MyModel
from django.shortcuts import render, redirect
from .forms import MyForm

from .models import Stylized
import tensorflow_hub as hub
import tensorflow as tf
from matplotlib import pyplot as plt
import numpy as np
import cv2
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string

model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')


def load_image(img_path):
    img = tf.io.read_file(img_path)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = img[tf.newaxis, :]
    return img


def upload_image(request):
    ms=['filt1','filt2','filt3']
    if request.method == 'POST':
        form = MyForm(request.POST, request.FILES)
        images=request.POST.getlist('image')
        if form.is_valid():
            form.save()
            return redirect('display_image', form.instance.pk,images)
    else:
        form = MyForm()

    return render(request, 'upload_image.html', {'form': form })


def display_image(request, my_model_id,images):

    my_model_instance = MyModel.objects.get(pk=my_model_id)
    print(my_model_instance.pk)
    image_url = my_model_instance.image.path
    # print(images)
    if(images=="['filt1']"):
        style_image = load_image(r'static\styles\style_1.jpg')
    elif(images=="['filt2']"):
        style_image = load_image(r'static\styles\style_2.jpg')
    else :
        style_image = load_image(r'static\styles\style_3.jpg')
    
    content = img_to_sketch(image_url,style_image)

    stylized_image_path = Stylized.objects.create(
        original=my_model_instance, styled_image=content)
    
    print(stylized_image_path.styled_image.url)
    return render(request, 'display_image.html', {'image_url': stylized_image_path.styled_image.url})



def img_to_sketch(image_path,style_image):
    content_image = load_image(image_path)
    stylized_image = model(tf.constant(content_image),
                           tf.constant(style_image))[0]

    stylized_image= cv2.cvtColor(np.squeeze(stylized_image)*255, cv2.COLOR_BGR2RGB)
    ret, buf = cv2.imencode('.jpg', stylized_image)
    content = ContentFile(buf, get_random_string(length=10))
    return content

