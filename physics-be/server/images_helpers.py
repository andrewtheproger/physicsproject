from .models import Image
import json


def to_models_list(images):
    return [to_model(i) for i in images]


def to_model(image):
    return {
        'id': image.id,
        'created_date': image.created_date,
        'updated_date': image.updated_date,
        'url': image.url,
        'thumbnail_url': image.thumbnail_url
    }
