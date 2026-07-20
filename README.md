# AI Virtual Assistant (Mini) — Task 8

A minimal voice-controlled assistant built with Python. It listens for spoken
commands, converts them to text, matches them against a small set of known
commands, and responds with speech + on-screen text.

**Goal:** Learn voice interface basics using `speech_recognition` (speech-to-text)
and `pyttsx3` (text-to-speech).

---

## How It Works

```
Microphone --> speech_recognition --> text --> if/elif command matching --> action
                                                          |
                                                          v
                                                      pyttsx3 (speaks response)
```

| Component            | Role                          | Direction     |
|-----------------------|-------------------------------|---------------|
| `speech_recognition`  | Ears — captures & transcribes | Audio → Text  |
| Command matching (if/elif) | Brain — decides what to do | Text → Decision |
| `webbrowser`, `os`, `subprocess`, `datetime` | Hands — performs the action | Decision → Action |
| `pyttsx3`             | Mouth — speaks the response    | Text → Audio  |

Speech recognition requires an internet connection (it uses Google's free
speech-to-text API via `recognize_google`). Text-to-speech (`pyttsx3`) works
fully offline using your OS's built-in voice engine.

---

## Compatibility

| Requirement        | Recommended                                  |
|---------------------|-----------------------------------------------|
| **Python version**  | **3.9 – 3.12** (3.11 confirmed working)     |
| **Avoid**           | Python 3.13 / 3.14 — no precompiled `PyAudio` wheels yet; requires Microsoft C++ Build Tools to compile from source |
| **OS**              | Windows (tested), macOS, Linux — all supported, but the "open/close app" commands (`notepad`, `calculator`) are **Windows-only** (`os.startfile`, `taskkill`) |
| **Internet**        | Required for speech recognition; not required for speech output |
| **Microphone**      | Required, with OS-level mic permission granted to your terminal/IDE |

> **Why avoid 3.13/3.14:** `PyAudio` ships prebuilt wheels only for actively
> supported, stable Python versions. On very new Python releases, pip falls
> back to compiling from source, which fails on Windows without Microsoft
> Visual C++ Build Tools installed. Using Python 3.11 avoids this entirely.

---

## Setup

### 1. Install a compatible Python version
Check your version:
```bash
python --version
```
If it's 3.13+ and you hit install errors, install Python 3.11 from
python.org alongside your existing version.

### 2. Create and activate a virtual environment
```bash
py -3.11 -m venv venv
```

**Windows (Command Prompt):**
```bash
venv\Scripts\activate.bat
```
**Windows (PowerShell)** — only if script execution is enabled:
```bash
venv\Scripts\activate
```
> If PowerShell blocks this with a `running scripts is disabled` error, either
> switch to Command Prompt, or run as Administrator:
> `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

**macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt once active.

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

**macOS users:** install `portaudio` first via Homebrew:
```bash
brew install portaudio
```

**Linux (Debian/Ubuntu) users:**
```bash
sudo apt install portaudio19-dev python3-pyaudio
```

### 4. Find your microphone (if voice isn't being detected properly)
```bash
python list_mics.py
```
This prints all available mic devices with an index number. If the wrong
mic is being used by default, open `voice_assistant.py` and change:
```python
with sr.Microphone() as source:
```
to:
```python
with sr.Microphone(device_index=1) as source:  # use your correct index
```

### 5. Run the assistant
```bash
python voice_assistant.py
```
Grant microphone access if your OS prompts for it.

---

## Supported Voice Commands

| Say this                  | It does                                 |
|-----------------------------|------------------------------------------|
| "open google"               | Opens Google in your browser             |
| "open youtube"              | Opens YouTube                            |
| "open whatsapp"             | Opens WhatsApp Web                       |
| "search for [anything]"     | Google-searches that phrase              |
| "open notepad"              | Launches Notepad (Windows only)          |
| "open calculator"           | Launches Calculator (Windows only)       |
| "close youtube / google / whatsapp / chrome" | Closes all Chrome windows (see note below) |
| "close notepad"             | Closes Notepad                           |
| "close calculator"          | Closes Calculator                        |
| "what's the date"           | Speaks today's date                      |
| "what's the time"           | Speaks the current time                  |
| "hello" / "hi"              | Time-appropriate greeting                |
| "tell me a joke"            | Speaks a random joke                     |
| "stop" / "exit"             | Ends the assistant                       |

> **Note on "close" commands:** `webbrowser.open()` doesn't return a handle
> to the specific tab it opened, so there's no clean way to close just the
> YouTube tab. "Close" commands close the entire Chrome process — meaning
> all open Chrome windows/tabs will close, not only the one the assistant
> opened.

---

## Troubleshooting

| Problem                                   | Fix |
|--------------------------------------------|-----|
| `PyAudio` fails to build with a C++ compiler error | Use Python 3.11/3.12, or install Microsoft C++ Build Tools |
| PowerShell blocks `venv\Scripts\activate`  | Use Command Prompt instead, or change the execution policy (see Setup step 2) |
| Assistant doesn't hear you / mishears often | Run `list_mics.py` and set the correct `device_index`; make sure you're in a quiet room during the startup calibration |
| Long delay before it responds              | Check your internet speed — `recognize_google` needs a round trip to Google's servers; this can't be sped up locally |
| "Speech service is unavailable" message    | No internet connection, or Google's API is temporarily unreachable |
| Nothing happens after "open google"        | Confirm your default browser is set correctly on your OS |

---

## Files in This Project

- `voice_assistant.py` — main assistant script
- `list_mics.py` — helper to list available microphone devices
- `requirements.txt` — pinned dependency versions
- `README.md` — this file
