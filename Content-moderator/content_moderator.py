import os.path
from pprint import pprint
import time
from io import BytesIO
from random import random
import uuid

# Funciona para conectar el recurso del Servicio Cognitivo
from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
import azure.cognitiveservices.vision.contentmoderator.models
# Para autenticar el acceso
from msrest.authentication import CognitiveServicesCredentials

# Variables para punto de conexión y clave del Servicio Cognitivo
PUNTO_DE_CONEXION = "https://primer-content-moderator.cognitiveservices.azure.com/"
CLAVE = "df5fc468739f4ad893fe2d5e2a495e0f"

# Referencia a la carpeta de textos
TEXT_FOLDER = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "text_files")

# Crea una instancia de cliente => da acceso al recurso de Content Moderator
cliente = ContentModeratorClient(
    endpoint=PUNTO_DE_CONEXION,
    credentials=CognitiveServicesCredentials(CLAVE)
)

# Screen the input text: check for profanity,
# do autocorrect text, and check for personally identifying
# information (PII)
with open(os.path.join(TEXT_FOLDER, 'content_moderator_text_moderation.txt'), "rb") as text_fd:
    screen = cliente.text_moderation.screen_text(
        text_content_type="text/plain",
        text_content=text_fd,
        language="eng",
        autocorrect=True,
        pii=True
    )
    # assert isinstance(screen, Screen)
    pprint(screen.as_dict())
