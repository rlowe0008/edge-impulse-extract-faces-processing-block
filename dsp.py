import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io, base64
import cv2

def generate_features(draw_graphs, raw_data, axes, sampling_freq, min_face_width, min_face_height, min_neighbours, output_width, output_height, output_grey):
    graphs = []

    # Convert raw data to image
    raw_data = raw_data.astype(dtype=np.uint32)
    width = raw_data[0]
    height = raw_data[1]

    pixels = []
    for x in np.nditer(raw_data[2:]):
        r = x >> 16 & 0xff
        g = x >> 8 & 0xff
        b = x & 0xff

        pixels.append((b << 16) + (g << 8) + (r))

    im = Image.fromarray(np.array(pixels, dtype=np.uint32).reshape(height, width, 1).view(dtype=np.uint8), mode='RGBA')
    im = im.convert(mode='RGB')

    image_as_np = np.array(im)
    # Convert RGB to BGR 
    image_as_np = image_as_np[:, :, ::-1].copy() 
    # Convert to greyscale
    gray = cv2.cvtColor(image_as_np, cv2.COLOR_BGR2GRAY)
    # Find faces
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        minNeighbors=min_neighbours,
        minSize=(min_face_width, min_face_height)
    )

    # We can only output 1 face for now. Store that face
    final_face = np.zeros((output_width, output_height, 3))
    if (output_grey):
        final_face = np.zeros((output_width, output_height))

    # For each found face...
    for (x, y, w, h) in faces:
        # Crop to face
        cropped = im.crop((x, y, x + w, y + h))
        cropped = cropped.resize((output_width, output_height))

        # Convert colour, if applicable
        if (output_grey):
            cropped = cropped.convert('L')

        final_face = cropped

        # Return base64 encoded image
        buf = io.BytesIO()
        cropped.save(buf, format='PNG')

        buf.seek(0)
        image = (base64.b64encode(buf.getvalue()).decode('ascii'))

        buf.close()

        graphs.append({
            'name': 'A face',
            'image': image,
            'imageMimeType': 'image/png',
            'type': 'image'
        })

    # For now, export only 1 face as a feature
    features = np.asarray(final_face) / 255.0
    if (output_grey):
        features = features.reshape(output_width * output_height)
        channels = 1
    else:
        features = features.reshape(output_width * output_height * 3)
        channels = 3

    image_config = { 'width': output_width, 'height': output_height, 'channels': channels }
    output_config = { 'type': 'image', 'dimensions': image_config }

    return { 'features': features.tolist(), 'graphs': graphs, 'output_config': output_config }