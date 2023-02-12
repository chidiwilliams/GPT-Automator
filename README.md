# GPT Automator

![App](assets/app.png)

Your voice-controlled assistant. GPT Automator lets you perform tasks on your computer using your voice.

Made by [Luke Harries](https://harries.co/) and [Chidi Williams](https://chidiwilliams.com/) at
the [London EA Hackathon, February 2023](https://forum.effectivealtruism.org/events/gTSwA8RoGidjpLnf6/london-ea-hackathon).

## Instructions

1. Install the requirements from the `requirements.txt` or `pyproject.toml` files.
2. Create a `.env` file from the `.env.example` file and fill in the OpenAI API key.
2. Run `python gui.py` to run the GUI and click 'Record' to say your prompt. Alternatively,
   run `python main.py [prompt]`
   to run the CLI.

## How it works

GPT Automator converts your audio input to text using OpenAI's Whisper. Then, it executes a sequence
of [LangChain](https://github.com/hwchase17/langchain) actions, generating AppleScript (for desktop automation) and
JavaScript (for browser automation) commands from your prompt using OpenAI's GPT-3 ("text-davinci-003"),
and then executing the resulting script.

## Example prompts

* Find the result of a calculation. Prompt: "What is 2 + 2?"
* Find restaurants nearby. Prompt: "Find restaurants near me"
* Play a game of chess. Prompt: "Play a game of chess"

## Disclaimer

This project executes code generated from natural language and may be susceptible
to [prompt injection](https://en.wikipedia.org/wiki/Prompt_engineering#Prompt_injection) and similar
attacks. This work was made as a proof-of-concept and is not intended for production use.
