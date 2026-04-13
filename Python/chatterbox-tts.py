
import torchaudio as ta
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

model = ChatterboxMultilingualTTS.from_pretrained(device="cpu")

liara_txt = "To może być ten artefakt, ale bez badaczek ciężko jest to stwierdzić."
liara_path = "C:/Users/Karol/Desktop/LegendaryExplorerAIDubbing\Python\me3_generated\original_liara_pl_me1.wav"

wav_liara = model.generate(
    text=liara_txt,
    language_id="pl",
    audio_prompt_path=liara_path
)
ta.save("me3_generated/generated_liara_pl_me3_2.wav", wav_liara, model.sr)

# TODO: Trim noise (sound end)
# TODO: Better model for polish speech