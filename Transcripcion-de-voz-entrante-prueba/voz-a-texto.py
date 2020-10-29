# Uso de paquete de las funcionalidades de Speech
import azure.cognitiveservices.speech as speechsdk

# Variables para tener acceso a la API
clave_suscripcion = "Aquí va la clave"
ubicacion = "Aquí la va región-ubicación"

# Acceso al recurso
speech_config = speechsdk.SpeechConfig(subscription=clave_suscripcion, region=ubicacion)

# El idioma configurado al momento del reconocimiento de voz
idioma = speechsdk.languageconfig.SourceLanguageConfig(language="es-MX")

# Se envía la configuración anterior y reconoce tu voz
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, 
    source_language_config=idioma)

print("Habla en 3, 2, 1, ahora =>")

# Guarda en resultado lo que detectó el speech_recognizer hasta un máximo de 15
# segundos o cuando no escuche nada
resultado = speech_recognizer.recognize_once()

# Muestra el resultado en cuanto si existen errores, si hizo el reconocimiento de voz,
# etc.
if resultado.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Lo que dijiste :D: {}".format(resultado.text))
elif resultado.reason == speechsdk.ResultReason.NoMatch:
    print("No reconocí nada: {}".format(resultado.no_match_details))
elif resultado.reason == speechsdk.ResultadoReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Reconocimiento de voz cancelado: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Detalles del error: {}".format(cancellation_details.error_details))