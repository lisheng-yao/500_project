import speech_recognition as sr
from playsound import playsound
import sys
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_DIR = os.path.join(BASE_DIR, "sound")

responses = {
    "你好": os.path.join(SOUND_DIR, "self.mp3"),
    "說愛你": os.path.join(SOUND_DIR, "loveu.mp3"),
    "媽媽": os.path.join(SOUND_DIR, "thx.mp3"),
    "準備好了嗎": os.path.join(SOUND_DIR, "check.mp3"),
    "喜歡誰": os.path.join(SOUND_DIR, "likejj.mp3"),
    "哪國人": os.path.join(SOUND_DIR, "kp.mp3"),
}

recognizer = sr.Recognizer()


def rec():
    print("請說話...", flush=True)
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)  # 自動調整背景噪音
            print("已調整背景噪音，開始錄音...", flush=True)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            print("錄音完成！", flush=True)

            # 嘗試進行語音辨識
            try:
                text = recognizer.recognize_google(audio, language="zh-TW")
                print(f"你說了: {text}", flush=True)
                return text
            except sr.UnknownValueError:
                print("無法辨識語音，請再試一次。", flush=True)
            except sr.RequestError as e:
                print(f"語音辨識服務出錯: {e}", flush=True)
    except Exception as e:
        print(f"發生錯誤: {e}", flush=True)
    return None


def play_response(text):
    # 根據辨識結果播放音檔，支援部分匹配
    for keyword, audio_file in responses.items():
        if keyword in text:  # 使用部分比對邏輯
            if os.path.exists(audio_file):
                print(f"播放音檔: {audio_file}", flush=True)
                playsound(audio_file)
                return  # 播放後跳出迴圈
            else:
                print(f"音檔 {audio_file} 不存在。", flush=True)
                return
    print("沒有對應的回覆", flush=True)


def main():
    while True:
        text = rec()  # 進行語音辨識
        if text:
            play_response(text)  # 播放對應的音檔
        print("準備下一次錄音...\n", flush=True)


if __name__ == "__main__":
    main()
