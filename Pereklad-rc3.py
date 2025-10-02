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
                entry.insert("end", " [Мову не зрозуміло]")
            except sr.RequestError as e:
                entry.insert("end", f" [Проблеми з API: {e}]")
    
    threading.Thread(target=_listen, daemon=True).start()

def clear_func():
    entry.delete(0, "end")
    result_label.configure(text="")

# сігмаінтерфейс
win = CTk.CTk()
win.title("Non-Corrupted Translator")
win.geometry("445x295")

entry = CTk.CTkEntry(win, width=280, height=30, placeholder_text="Enter text to translate")
entry.pack(pady=20)

clear_button = CTk.CTkButton(win, text="❌", command=clear_func, width=22, height=22)
clear_button.place(x=300, y=130.5)

language_map = {name.capitalize(): code for code, name in LANGUAGES.items()}
language_names = list(language_map.keys())

lang_var = CTk.StringVar(value='English')
language_menu = CTk.CTkOptionMenu(win, values=language_names, variable=lang_var)
language_menu.pack(pady=10)

async def transl():
    translator = Translator()
    user_text = entry.get().lower()

    # 🔹 Easter Egg
    if "живчик" in user_text:
        res_text = "відсилка на сергія"
    else:
        res = await translator.translate(entry.get(), dest="en")
        res_text = res.text

    old = result_label.cget("text")
    new_text = old + ("\n" if old else "") + f"{entry.get()} -> {res_text}"
    result_label.configure(text=new_text)
    result_frame._parent_canvas.yview_moveto(1.0)

    with open("history.txt", "a", encoding="utf-8") as f:
        f.write(f"{entry.get()} -> {res_text}\n")


translate_button = CTk.CTkButton(win, text="Translate", command=lambda: asyncio.run(transl()))
translate_button.pack(pady=10)

micro = CTk.CTkButton(win, text="Speak", width=25, height=25, command=listen)
micro.pack(pady=0)

result_frame = CTk.CTkFrame(win, width=400, height=30, fg_color="black")
result_frame.pack(pady=20, fill="x")

result_label = CTk.CTkLabel(result_frame, text="", width=280, height=30, text_color="white")
result_label.pack(pady=0)

win.mainloop()
