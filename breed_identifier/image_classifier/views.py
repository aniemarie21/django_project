from django.shortcuts import render
from .forms import ImageUploadForm
from .models import Image
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

# Load pre-trained model for image classification
model = tf.keras.applications.MobileNetV2(weights='imagenet')

def classify_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

    preds = model.predict(img_array)
    decoded_preds = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3)[0]
    return decoded_preds[0][1]  # Return the top prediction (breed name)

def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the image and classify the breed
            img_instance = form.save()
            breed = classify_image(img_instance.image.path)

            # Save the breed in the Image instance
            img_instance.breed = breed
            img_instance.save()

            # Return the result template with the image and breed
            return render(request, 'image_classifier/result.html', {'breed': breed, 'image': img_instance})

    else:
        form = ImageUploadForm()

    return render(request, 'image_classifier/upload.html', {'form': form})
