Voice-Controlled Desktop Assistant (David AI)

Overview:

This project implements a voice-controlled Desktop assistant using Python. The assistant, named "David AI", can:
- Respond to voice queries.
- Open common websites and system applications.
- Play specific or random music from a directory.
- Answer queries using Cohere's AI model.
- Maintain conversation history in text files.

Technologies Used:

- speech_recognition: For capturing and transcribing voice input.
- pyttsx3: For speech synthesis.
- cohere: For AI-based responses.
- webbrowser, os, sys, subprocess: For interacting with the system.
- datetime, random, re: For utility functions.

Directory Structure:

- music/: Contains music files.
- Generated/: Automatically created folder to store conversation logs and AI responses.

Instructions:

1. Speak into the microphone after the assistant says "Listening...".
2. You can give commands like:
   - "Open YouTube"
   - "Play break music"
   - "Open notepad"
   - "What is the time"
   - "Using AI model explain quantum computing"
	By running query including "using AI mode", responses get separately stored in `Generated/` folder.
3. Conversations are saved in the `Generated/` folder.
4. Say "David quit" to exit the assistant.
