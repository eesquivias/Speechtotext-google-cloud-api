import srt, os
from google.cloud import speech
#from google.cloud.speech import enums
from google.cloud import storage
from google.oauth2 import service_account
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=  'clave.json'

storage_uri='gs://speechtotextpoca/normalized_loud_quiet16_mono_0_ff_intro.wav'
def long_running_recognize(args):
    print('Transcribing {}...'.format(args.storage_uri))
    client= speech.SpeechClient()
    operation = client.long_running_recognize(
        config=
        {
            "enable_word_time_offsets": True,
            "enable_automatic_punctuation": True,
            "sample_rate_hertz": 16000,
            "language_code": 'es-ES',
            "audio_channel_count": 1,
            "encoding": args.encoding,
        },
        audio={"uri": args.storage_uri},
  )
    response= operation.result()
  #  print(response)

    subs = []
    for result in response.results:

          # First alternative is the most probable result
        subs = break_sentences(args, subs, result.alternatives[0])

    print("Transcribing finished")
    return subs


def break_sentences(args, subs, alternative):
    firstword = True
    charcount = 0
    idx = len(subs) + 1
    content = ""

    for w in alternative.words:
        if firstword:
            # first word in sentence, record start time
            start = w.start_time

        charcount += len(w.word)
        content += " " + w.word.strip()

        if ("." in w.word or "!" in w.word or "?" in w.word or
                charcount > args.max_chars or
                ("," in w.word and not firstword)):
            # break sentence at: . ! ? or line length exceeded
            # also break if , and not first word
            subs.append(srt.Subtitle(index=idx,
                                     start=start,
                                     end=w.end_time,
                                     content=srt.make_legal_content(content)))
            firstword = True
            idx += 1
            content = ""
            charcount = 0
        else:
            firstword = False
    return subs


def write_srt(args, subs):
    srt_file = args.out_file + ".srt"
    print("Writing {} subtitles to: {}".format(args.language_code, srt_file))
    f = open(srt_file, 'w')
    f.writelines(srt.compose(subs))
    f.close()
    return


def write_txt(args, subs):
    txt_file = args.out_file + ".txt"
    print("Writing text to: {}".format(txt_file))
    f = open(txt_file, 'w')
    for s in subs:
        f.write(s.content.strip() + "\n")
    f.close()
    return


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--storage_uri",
        type=str,
        default="gs://speechtotextpoca/normalized_loud_quiet16_mono_0_ff_intro.wav",
    )
    parser.add_argument(
        "--language_code",
        type=str,
        default="es-ES",
    )
    parser.add_argument(
        "--sample_rate_hertz",
        type=int,
        default=16000,
    )
    parser.add_argument(
        "--out_file",
        type=str,
        default="subtitle",
    )
    parser.add_argument(
        "--max_chars",
        type=int,
        default=40,
    )
    parser.add_argument(
        "--encoding",
        type=str,
        default='LINEAR16'
    )
    parser.add_argument(
        "--audio_channel_count",
        type=int,
        default=1
    )
    args = parser.parse_args()

    subs = long_running_recognize(args)
    write_srt(args, subs)
    write_txt(args, subs)


if __name__ == "__main__":
    main()

    #media_uri='gs://speechtotextpoca/normalized_loud_quiet16_0.wav'
#long_audio_wav= speech.RecognitionAudio(uri=media_uri)
"""
    "encoding": "LINEAR16",
    "languageCode": "es-CO",
    "sampleRateHertz": 44100,
    "audioChannelCount": 2,
    "alternativeLanguageCodes": [],
    "speechContexts": [],
    "adaptation": {
      "phraseSets": [],
      "phraseSetReferences": [],
      "customClasses": []
    },
    "enable_word_time_offsets": true,
    "model": "default"
  }
  """
#input= "C:\Users\...\normalized_loud_quiet16_0.wav"
#output= "baseline_diagnosis.html"
"""config= {
      "enable_word_time_offsets": True,
      "enable_automatic_punctuation":True,
      "language_code": args.language_code,
      "encoding":args.encoding
      #model='video',
      #"use_enhanced":True,
      "sample_rate_hertz": args.sample_rate_hertz,
      "audio_channel_count"= args.audio_channel_count,
  }
audio={"uri":args.storage_uri}
    
#audio=speech.RecognitionAudio(uri=media_uri)

operation= client.long_running_recognize(config,audio)
"""

"""
for result in response.results:
    alternative=result.alternatives[0]
    start_hhmmss= time.strftime('%H:%M:%S',time.gmtime(
        alternative.words[0].start_time.seconds))
    start_mmss=int
    ))
    #print(result.alternatives[0].transcript)
    print(result.alternatives[0].confidence)
    print()
i=1
srt_text=[]
text=[]
for result in response.results:
"""