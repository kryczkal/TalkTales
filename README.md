
# TalkTales

<div align="center">
<img src="assets/logo_full.png" alt="Logo" width="160" height="160">
</div>

## About the project

The primary objective of this project is to develop a specialized tool aimed at assisting deaf individuals in their 
day-to-day interactions. While the overarching goal is to convert spoken language into text, 
the unique aspect of this project lies in its approach to speaker differentiation.
By highlighting changes in the speaker's voice within the transcribed text, our tool aims to offer an 
enhanced contextual understanding, a feature often missing in traditional speech-to-text services.

We leverage the open-source Vosk model for the core speech-to-text translation. 
However, our methodology diverges from mainstream solutions, as we are intent on reducing our dependence on machine learning algorithms. 
The goal is not merely to create a functional tool but to deepen our understanding of sound and voice phenomena. 
Most of the concepts are explained in detail inside the docs directory.

**The development of the repository is currently halted due to high intensity of university tasks**

## Getting Started

### Prerequisites

- Python 3.10+ installed
- `git` installed

### Installation

First, clone the repository to your local machine:
```shell
git clone https://github.com/kryczkal/TalkTales.git ; cd TalkTales
```

Before installation of the dependencies, it is highly recommended to set up a virtual environment inside the project
```shell
python -m venv `myPythonEnv`
source `myPythonEnv`/bin/activate
```
Then install the python dependencies with pip
```shell
pip install -r requirements.txt
```

You are ready to go

## Usage
### Main App
Run the application with

```shell
python main.py
```

or on linux

```shell
./main.py
```

### Utilities
Various utilities are also provided alongside the main app.
These include:
#### DiarizationTester
Program used to invoke Diarizers components without application frontend. 
It either loads an audio file or connects to live stream. It should then write speaker changes to stdout.
If set to plot (With Settings file), it will also make plot of speakers across time.

##### Usage
```shell
python DiarizationTester.py [optional: filename]
```
or

```shell
./DiarizationTester.py [optinal: filename]
```
#### Suggestions Library
The suggestions folder is an experimental answer to the following problem: 'how to deal with artifacts in
speech-to-text algorithms'. Given that speech-to-text algorithms are imperfect, and minor artifacts in them can greatly 
disrupt the flow of the conversation, we've wanted to make a second-degree security measure. That would be scanning the
sentences for unlikely utterances, and highlighting them as 'unlikely', then providing the suggested, most probable word.
This is achieved with herbert language model, unfortunately turned out to work too slow for real time usage.

It can be tested with:
##### 
```shell
python src/suggestions/testing.py
```
or
```shell
./src/suggestions/testing.py
```
The script will ask for input sentences, and struggle to find improbable utterances in it, and suggest improvements.
#### Matlab Folder
The matlab folder provides simple scripts that were used during the stage of acquiring sound samples in different places.
In order to analyze human speech in different environments and construct a tool that can diarize human speech, 
we've made a set of different wave plots, spectrograms, mel spectrograms etc. In the early stages of development,
this served as a reference for our understanding of human speech.

## Roadmap

- [x] Simple diarization model
- [x] Multithreaded backend design
- [ ] Diarization model tuning and upgrades
- [ ] Multi-language support
- [ ] More detailed examples
- [ ] Android application front-end

## Authors

- [Lukasz Kryczka](https://github.com/kryczkal)
- [Jakub Lisowski](https://github.com/Jlisowskyy)
- [Tomasz Mycielski](https://github.com/Al-Gor1thm)
- [Michal Kwiatkowski](https://github.com/KwiatkowskiML)
- [Ernest Molczan](https://github.com/molczane)
- [Wojtek Matejuk](https://github.com/WojciechMat)
- [Mateusz Mikiciuk](https://github.com/chefxxx)
- [Sofiia Kuzmenko](https://youtu.be/dQw4w9WgXcQ)

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.