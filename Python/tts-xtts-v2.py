from TTS.api import TTS
from sympy import false

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)

liara_txt = "To może być ten artefakt, ale bez badaczek ciężko jest to stwierdzić."
liara_path = "C:/Users/Karol/Desktop/LegendaryExplorerAIDubbing/Python/me3_generated/original_liara_en_me3.wav"
out_path = "C:/Users/Karol/Desktop/LegendaryExplorerAIDubbing/Python/me3_generated/generated_liara_pl_me3_xtts-en.wav"

tts.tts_to_file(text=liara_txt,
                file_path=out_path,
                speaker_wav=liara_path,
                language="pl")