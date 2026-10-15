# Música de fondo local con MusicGen (gratis, sin claves). Uso: python3 generar_musica.py salida.wav "soft emotional piano…"
# Requiere: pip install transformers torch soundfile. Sale un tramo de ~28 s: alárgalo con ffmpeg (acrossfade) al largo del video.
# (facebook/musicgen-small): un tramo de ~28 s, sin claves ni internet después de bajar el modelo.
import sys
import numpy as np
import soundfile as sf
import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration

salida, prompt = sys.argv[1], sys.argv[2]
dispositivo = "mps" if torch.backends.mps.is_available() else "cpu"
proc = AutoProcessor.from_pretrained("facebook/musicgen-small")
modelo = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small").to(dispositivo)
torch.manual_seed(7)
ent = proc(text=[prompt], padding=True, return_tensors="pt").to(dispositivo)
audio = modelo.generate(**ent, do_sample=True, guidance_scale=3.0, max_new_tokens=1400)
sr = modelo.config.audio_encoder.sampling_rate
sf.write(salida, audio[0, 0].float().cpu().numpy(), sr)
print("listo", salida, sr)
