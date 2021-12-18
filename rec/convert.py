from pydub import AudioSegment
sound = AudioSegment.from_wav("name0.wav")
sound = sound.set_channels(2)
sound.export("name3.wav", format="wav")