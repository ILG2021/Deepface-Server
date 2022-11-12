from retinaface import RetinaFace
from deepface import DeepFace

DeepFace.build_model("Race")
RetinaFace.build_model()
exec(open("api.py").read())

