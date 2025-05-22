

import tkinter as tk
import pyttsx3
import webbrowser
import threading
import speech_recognition as sr
from topic_parser import parse_topic
from explanation_generator import generate_explanation
from resource_finder import find_articles, find_youtube_videos
from tkinter import messagebox


# Voice setup
engine = pyttsx3.init()
speaking_thread = None
is_speaking = False

def toggle_speech(text):
    global speaking_thread, is_speaking
    if is_speaking:
        engine.stop()
        is_speaking = False
    else:
        def run():
            global is_speaking
            is_speaking = True
            try:
                engine.say(text)
                engine.runAndWait()
            except RuntimeError:
                pass
            is_speaking = False

        speaking_thread = threading.Thread(target=run)
        speaking_thread.daemon = True
        speaking_thread.start()

def get_voice_input_and_search():
    print("🎙 Voice input started")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        mic_button.config(text="🎙 Recording...")
        try:
            audio = recognizer.listen(source)
            print("🎧 Audio captured")
            mic_button.config(text="🎤")
            query = recognizer.recognize_google(audio)
            print(f"🗣 Recognized: {query}")
            input_entry.delete(0, tk.END)
            input_entry.insert(0, query)
            handle_query()
        except sr.UnknownValueError:
            print("🤷 Could not understand audio")
            input_entry.delete(0, tk.END)
            input_entry.insert(0, "Sorry, couldn't catch that 🥲")
        except sr.RequestError as e:
            print("⚠ Google API error:", e)
            input_entry.delete(0, tk.END)
            input_entry.insert(0, "Network error. Try again.")
        except Exception as e:
            print("❌ Error:", e)
            input_entry.delete(0, tk.END)
            input_entry.insert(0, "Voice input failed.")
        finally:
            mic_button.config(text="🎤")

def save_note():
    prompt = input_entry.get()
    explanation = explanation_text.get("1.0", tk.END).strip()
    article_basic = articles.get('basic', '')
    article_depth = articles.get('depth', '')
    video_basic = videos.get('basic', '')
    video_depth = videos.get('depth', '')

    if not explanation or not prompt or prompt == "ask anything":
        return

    with open("saved_notes.txt", "a", encoding="utf-8") as file:
        file.write(f"📝 {prompt}:\n{explanation}\n\n")
        file.write("📚 Articles:\n")
        file.write(f"Basic: {article_basic}\n")
        file.write(f"In-depth: {article_depth}\n\n")
        file.write("🎥 Videos:\n")
        file.write(f"Basic: {video_basic}\n")
        file.write(f"In-depth: {video_depth}\n")
        file.write("\n" + "-" * 50 + "\n\n")

    # ✅ Show a quick popup message (like other actions)
    tk.messagebox.showinfo("Note Saved", "✅ Note saved successfully!")



def view_notes():
    notes_window = tk.Toplevel()
    notes_window.title("📓 Saved Notes")
    notes_window.geometry("800x600")
    notes_text = tk.Text(notes_window, wrap="word", font=("Segoe UI", 11), bg="white")
    notes_text.pack(fill="both", expand=True)

    try:
        with open("saved_notes.txt", "r", encoding="utf-8") as file:
            content = file.read()
            notes_text.insert("1.0", content)
    except FileNotFoundError:
        notes_text.insert("1.0", "No notes saved yet.")

    def open_link(event):
        index = notes_text.index("@%s,%s" % (event.x, event.y))
        line = notes_text.get(index + " linestart", index + " lineend")
        if line.startswith("http"):
            webbrowser.open(line)

    notes_text.tag_config("link", foreground="blue", underline=True)
    notes_text.bind("<Button-1>", open_link)

def run_app():
    def on_closing():
        if is_speaking:
            engine.stop()
        root.destroy()

    root = tk.Tk()
    root.title("📚 StudySage – AI Study Helper")
    root.geometry("900x800")
    root.config(bg="#f9f6ff")
    root.protocol("WM_DELETE_WINDOW", on_closing)

    FONT_HEADING = ("Segoe UI", 16, "bold")
    FONT_NORMAL = ("Segoe UI", 12)

    top_buttons = tk.Frame(root, bg="#f9f6ff")
    top_buttons.pack(anchor="ne", padx=20, pady=(10, 0))

    save_btn = tk.Button(top_buttons, text="💾 Save Note", font=FONT_NORMAL, bg="#6a0dad", fg="white",
                         command=save_note)
    save_btn.pack(side="right", padx=5)

    view_btn = tk.Button(top_buttons, text="📂 View Notes", font=FONT_NORMAL, bg="#6a0dad", fg="white",
                         command=view_notes)
    view_btn.pack(side="right", padx=5)

    input_frame = tk.Frame(root, bg="#f9f6ff")
    input_frame.pack(pady=20, fill="x", padx=20)

    center_container = tk.Frame(input_frame, bg="#f9f6ff")
    center_container.pack()

    entry_container = tk.Frame(center_container, bg="white", bd=1, relief="solid")
    entry_container.pack(side="left")

    global input_entry
    input_entry = tk.Entry(entry_container, font=FONT_NORMAL, bd=0, relief="flat", width=35, fg="gray")
    input_entry.insert(0, "ask anything")

    def on_focus_in(event):
        if input_entry.get() == "ask anything":
            input_entry.delete(0, tk.END)
            input_entry.config(fg="black")

    def on_focus_out(event):
        if input_entry.get() == "":
            input_entry.insert(0, "ask anything")
            input_entry.config(fg="gray")

    input_entry.bind("<FocusIn>", on_focus_in)
    input_entry.bind("<FocusOut>", on_focus_out)
    input_entry.pack(side="left", ipady=6, padx=(5, 0))

    global mic_button
    mic_button = tk.Button(entry_container, text="🎤", font=FONT_NORMAL, bg="white", fg="gray", bd=0,
                           command=lambda: threading.Thread(target=get_voice_input_and_search).start())
    mic_button.pack(side="right", padx=5)

    search_button = tk.Button(center_container, text="🔍", font=FONT_NORMAL, bg="#6a0dad", fg="white",
                              activebackground="#7f3bbf", width=4, command=lambda: handle_query())
    search_button.pack(side="left", padx=5)

    loading_label = tk.Label(root, text="", font=("Segoe UI", 10), bg="#f9f6ff", fg="green")
    loading_label.pack()

    header_frame = tk.Frame(root, bg="#f9f6ff")
    header_frame.pack(fill="x", padx=40)

    explanation_label = tk.Label(header_frame, text="📘 Explanation", font=FONT_HEADING, bg="#f9f6ff", fg="#4b0082")
    explanation_label.pack(side="left")

    speak_button = tk.Button(header_frame, text="🔊", font=("Segoe UI", 11), bg="#f9f6ff", fg="#4b0082", bd=0,
                             command=lambda: toggle_speech(explanation_text.get("1.0", tk.END)))
    speak_button.pack(side="right")

    global explanation_text
    explanation_text = tk.Text(root, wrap="word", width=95, height=10, font=FONT_NORMAL,
                               bg="white", relief="solid", bd=1)
    explanation_text.pack(padx=20, pady=(0, 10), fill="both", expand=True)
    explanation_text.config(state="disabled")

    resources_label = tk.Label(root, text="🔗 Resources", font=FONT_HEADING, bg="#f9f6ff", fg="#4b0082")
    resources_label.pack(anchor="w", padx=40)

    resource_frame = tk.Frame(root, bg="#f9f6ff")
    resource_frame.pack(padx=20, pady=10, fill="both", expand=True)

    global articles_text, videos_text, articles, videos
    articles_text = tk.Text(resource_frame, wrap="word", width=50, height=20, font=FONT_NORMAL,
                            bg="white", relief="groove", bd=2)
    articles_text.pack(side="left", fill="both", expand=True, padx=(0, 10))
    articles_text.insert(tk.END, "📚 Articles\n\n", ("heading",))
    articles_text.tag_config("heading", font=FONT_HEADING, foreground="#6a0dad")
    articles_text.config(state="disabled")

    videos_text = tk.Text(resource_frame, wrap="word", width=50, height=20, font=FONT_NORMAL,
                          bg="white", relief="groove", bd=2)
    videos_text.pack(side="right", fill="both", expand=True)
    videos_text.insert(tk.END, "▶ YouTube Videos\n\n", ("heading",))
    videos_text.tag_config("heading", font=FONT_HEADING, foreground="#6a0dad")
    videos_text.config(state="disabled")

    def make_clickable(textbox, link, title):
        start = textbox.index("end")
        textbox.insert("end", f"{title}\n{link}\n\n", ("link",))
        textbox.tag_config("link", foreground="blue", underline=True)
        textbox.tag_bind("link", "<Button-1>", lambda e: webbrowser.open(link))

    def handle_query():
        global articles, videos
        topic = input_entry.get()
        if not topic.strip() or topic.strip() == "ask anything":
            return

        loading_label.config(text="⌛ Loading resources, please wait...")
        root.update_idletasks()

        parsed = parse_topic(topic)
        explanation = generate_explanation(parsed)
        articles = find_articles(parsed)
        videos = find_youtube_videos(parsed)

        explanation_text.config(state="normal")
        explanation_text.delete("1.0", tk.END)
        explanation_text.insert("1.0", explanation)
        explanation_text.config(state="disabled")

        articles_text.config(state="normal")
        articles_text.delete("2.0", tk.END)
        articles_text.insert(tk.END, "\n📘 Basic:\n", ("subheading",))
        make_clickable(articles_text, articles['basic'], "Read More")
        articles_text.insert(tk.END, "\n📗 In-depth:\n", ("subheading",))
        make_clickable(articles_text, articles['depth'], "Explore Further")
        articles_text.tag_config("subheading", font=("Segoe UI", 11, "bold"), foreground="#4b0082")
        articles_text.config(state="disabled")

        videos_text.config(state="normal")
        videos_text.delete("2.0", tk.END)
        videos_text.insert(tk.END, "\n🎬 Basic:\n", ("subheading",))
        make_clickable(videos_text, videos['basic'], "Watch Now")
        videos_text.insert(tk.END, "\n🎥 In-depth:\n", ("subheading",))
        make_clickable(videos_text, videos['depth'], "Deep Dive")
        videos_text.tag_config("subheading", font=("Segoe UI", 11, "bold"), foreground="#4b0082")
        videos_text.config(state="disabled")

        loading_label.config(text="✅ Loaded successfully!")

    root.mainloop()

if __name__ == "__main__":
    run_app()
