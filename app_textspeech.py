### Text-to-speech Original Doc:
# https://cloud.google.com/text-to-speech/docs/quickstart-client-libraries
# Synthesizes speech from the input string of text or ssml. ssml must be well-formed according to:
# https://www.w3.org/TR/speech-synthesis/

### Authenticate credentials & Install library
# !sudo -H pip3 install --upgrade google-cloud-texttospeech
# !export GOOGLE_APPLICATION_CREDENTIALS="./secret-gcp.json" <= this is instead done by python below

### Instantiate GCP account and Authenticate credentials in secret.json
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./secret-gcp.json"

### Define Function of Text To Speech
def texttospeech(text = "こんにちは、たける", lang="JP", gender="male"):
  # Import texttospeech
  from google.cloud import texttospeech

  # Instantiates a client
  client = texttospeech.TextToSpeechClient()

  # Set the text input to be synthesized
  synthesis_input = texttospeech.SynthesisInput(text = text)

  # Set param: language code ("en-US")
  lang_code={
    "EN": "en-US",
    "JP": "ja-JP"
  }

  # Set param: ssml voice gender ("neutral")
  # Ref. https://cloud.google.com/text-to-speech/docs/reference/rest/v1/SsmlVoiceGender
  gender_type = {
    "default": texttospeech.SsmlVoiceGender.SSML_VOICE_GENDER_UNSPECIFIED,
    "male": texttospeech.SsmlVoiceGender.MALE,
    "female": texttospeech.SsmlVoiceGender.FEMALE,
    "neutral": texttospeech.SsmlVoiceGender.NEUTRAL
  }

  # Build the voice request with selected params
  voice = texttospeech.VoiceSelectionParams(
    language_code=lang_code[lang], ssml_gender=gender_type[gender]
  )

  # Select the type of audio file you want returned
  audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
  )

  # Perform the text-to-speech request
  # with the selected voice parameters and audio file type into the object: response
  response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
  )
  return response

  # Perform the text-to-speech request and prepare the mp3. *wb: write binary
  # filename = "output.mp3"
  # with open(filename, "wb") as out:
  #   # Write the response to the output file.
  #   out.write(response.audio_content)
  #   print(f'Audio content written to file {filename}.')


### Build app with Steramlit
import streamlit as st
st.title("音声出力アプリ")

# Let use select the process
input_option = st.selectbox(
  "入力データの選択",
  ("直接入力","テキストファイル")
)

### Process text data
input_data = None
# Direct text copy
if input_option == "直接入力":
  input_data = st.text_area(
    "テキストをこちらに入力してください",    # label
    value = "Sample Text will be read",   # placeholder
  )
# File Upload
else:
  uploaded_file = st.file_uploader("ファイルをアップロードしてください", ["txt"])
  if uploaded_file is not None:
    # To read file as string and decode to utf8
    content = uploaded_file.read()
    input_data = content.decode("utf-8")

# Confirm text data in case of the uploaded file
if input_data is not None:
  if input_option == "テキストファイル":
    st.write("入力データ")
    st.write(input_data)

### Parameter setup
st.markdown("## パラメータ設定")

st.subheader("言語設定")
lang = st.selectbox(
  "入力データの選択",
  ("EN","JP")
)

st.subheader("話者性別設定")
gender = st.selectbox(
  "入力データの選択",
  ("default","male","female","neutral")
)

### Perform Voice Synthesis
st.markdown("### 音声合成")
st.write("### こちらの文章で音声ファイルの生成を行いますか?")

# button to judge click state
if st.button("生成"):
  # Prepare comment element under button
  comment = st.empty()
  comment.write("音声の生成を開始します")

  # Get Audio data
  response = texttospeech(input_data, lang, gender)

  # Display Audio to play audio_content in the object response
  st.audio(response.audio_content)
  comment.write("完了しました")
