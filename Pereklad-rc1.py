import customtkinter as CTk
from googletrans import Translator
import speech_recognition as sr
import threading
import sounddevice as sd
import asyncio
from googletrans import LANGUAGES


def listen():
    def _listen():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                print("Скажіть щось...")
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio, language="uk-UA")  # potyshno-mova
                entry.insert("end", " " + text)
            except sr.UnknownValueError:
                entry.insert("end", " [Не вдалося розпізнати мову]")
            except sr.RequestError as e:
                entry.insert("end", f" [Помилка сервісу: {e}]")
    
    threading.Thread(target=_listen, daemon=True).start()


# сігмаінтерфейс
win = CTk.CTk()
win.title("Non-Corrupted Independed Translator")
win.geometry("400x250")

entry = CTk.CTkEntry(win, width=280, height=30, placeholder_text="Enter text to translate")
entry.pack(pady=20)

language_map = {name.capitalize(): code for code, name in LANGUAGES.items()}
language_names = list(language_map.keys())

lang_var = CTk.StringVar(value='English')
language_menu = CTk.CTkOptionMenu(win, values=language_names, variable=lang_var)
language_menu.pack(pady=10)

async def transl():
    translator = Translator()
    res = await translator.translate(entry.get(), dest=lang_var.get())
    result_label.configure(text=res.text)
    with open("history.txt", "a", encoding="utf-8") as f:
        f.write(f"{entry.get()} -> {res.text}\n")


# тестова кнопка
translate_button = CTk.CTkButton(win, text="Translate", command=lambda: asyncio.run(transl()))
translate_button.pack(pady=10)

micro = CTk.CTkButton(win, text="Speak", width=25, height=25, command=listen)
micro.pack(pady=0)

result_label = CTk.CTkLabel(win, text="", width=280, height=30)
result_label.pack(pady=20)

win.mainloop()
