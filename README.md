# babbleon
A free, basic, and open source voice transcription app for Windows that uses OpenAI's Whisper and your API key.
![BabbleOn v1 screenshot](https://github.com/user-attachments/assets/a3c007a2-32ee-44c1-9903-bd5e3e0d912a)
BabbleOn is built using Claude AI (Sonnet 3.5) with Python.

### To run it:

First, you'll need to have Python installed on your computer. If you don't have it already, here's how to get it:

- Go to the official Python website: https://www.python.org/downloads/
- Click on the big yellow button that says "Download Python" (it should show the latest version)
- Once it's downloaded, run the installer and make sure to check the box that says "Add Python to PATH" before you click "Install Now"

Now that you have Python, you'll use something called "pip" to install the other stuff we need. Pip is like a magic wand that installs cool Python tools for you. It comes with Python, so you don't need to download it separately.

### Here's how to install the dependencies:

Open the Command Prompt (on Windows, you can do this by pressing the Windows key, typing "cmd", and hitting Enter)
Now, you'll type these commands one by one, pressing Enter after each:
```
pip install tkinter  
pip install pyaudio  
pip install openai  
pip install pydub  
pip install pygame
```

Each of these will download and install the tool we need.  

You can then run the app by simply double-clicking on the Python file in your file explorer.  

### Here's how to use it:  

- Enter your OpenAI API key in the top field.
You can either record audio or select an existing file to transcribe.

- To record, click "Record" to start and click it again to stop.
To use an existing file, click "Select File" and choose your audio file.

- Click "Transcribe" to send the audio to OpenAI for transcription.
The transcription will appear in the text box.  

You can play the audio by clicking "Play Audio".  
To copy the transcription without timestamps, click "Copy Text".
