import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
from pathlib import Path
import numpy as np
import keras_cv
import keras
import cv2
from PIL import Image


model_path = Path(__file__).parent.joinpath("model")

prediction_decoder_plate_position = keras_cv.layers.NonMaxSuppression(
    bounding_box_format="xyxy",
    from_logits=True,
    confidence_threshold=0.65,
    max_detections=1
)
model_plate_position = keras.models.load_model(
    model_path.joinpath('plate_position_model.keras'),
    compile=False
)
model_plate_position.prediction_decoder = prediction_decoder_plate_position


def crop_plate(img: Image.Image, bbox: list) -> Image.Image:
    size = max(img.size)
    img_resized = Image.new(mode="RGB", size=(size, size))
    img_resized.paste(img, (0, 0))
    return img_resized.crop(
        (
            img_resized.width * bbox[1],
            img_resized.height * bbox[0],
            img_resized.width * bbox[3],
            img_resized.height * bbox[2]
        )
    )


def recognize_plate(
        image: Image.Image,
        model: keras.models = model_plate_position
) -> tuple[Image.Image]:

    # make image preprocessing before model input
    img = np.array(image)
    img_with_box = img.copy()
    resizer = keras_cv.layers.Resizing(
        640,
        640,
        pad_to_aspect_ratio=True
    )
    img = resizer([img])

    # make prediction
    y_pred = model.predict((img), verbose=0)

    if y_pred["classes"][0][0] == -1:
        return img, None, None

    y_pred = keras_cv.bounding_box.convert_format(
        y_pred,
        images=img,
        source="xyxy",
        target="rel_yxyx",
    )

    # draw box on original image
    size = max(img_with_box.shape)
    box_xmin = int(y_pred["boxes"][0][0][1] * size)
    box_xmax = int(y_pred["boxes"][0][0][3] * size)
    box_ymin = int(y_pred["boxes"][0][0][0] * size)
    box_ymax = int(y_pred["boxes"][0][0][2] * size)
    cv2.rectangle(
        img_with_box,
        (box_xmin, box_ymin),
        (box_xmax, box_ymax),
        (255, 255, 0),
        3
    )
    img_with_box = Image.fromarray(img_with_box)
    plate = crop_plate(image, y_pred["boxes"][0][0].numpy().tolist())
    box = box_xmin, box_ymin, box_xmax, box_ymax
    return img_with_box, plate, box
