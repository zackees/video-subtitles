# video-subtitles

Adds subtitles to a movie.

[![Linting](../../actions/workflows/lint.yml/badge.svg)](../../actions/workflows/lint.yml)

[![MacOS_Tests](../../actions/workflows/push_macos.yml/badge.svg)](../../actions/workflows/push_macos.yml)
[![Ubuntu_Tests](../../actions/workflows/push_ubuntu.yml/badge.svg)](../../actions/workflows/push_ubuntu.yml)
[![Win_Tests](../../actions/workflows/push_win.yml/badge.svg)](../../actions/workflows/push_win.yml)

Run tox until it's correct.

To develop software, run `. ./activate.sh`

# Install

#### Install Python 3.10

  * Click the following:
    * https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe
  * During install MAKE SURE YOU CLICK "ADD TO PATHS" (or similar)
  * You only need to do this once

#### Install videosubtitles tool

  * Open up a windows command terminal
    * Hit the "Windows Key" + r
    * type in `cmd` and hit `enter` on the keyboard
    * type in `pip install video-subtitles`
    * Close the windows command terminal

It should now be installed.

# First run

  * Keep in mind that the first run will take a lot of time as it downloads the proper drivers for your computer. But this will only be done once. Also there is an API key
  that you will be asked about, you can skip this by putting in `free` as the key.

# Running

  * Open up a windows command terminal, as described in the previous step
  * `cd` to your video directory where you video is at
  * type in the following `videosubtitles myvideo.mp4 --languages es,fr,zh,it`
    * This will generate English, French, Chinese, Italian subtitles
    * For other subtitle languages see the language reference below
  * On the first run, you will be asked to enter in an API key from DeepL, the english -> Language X translation service. This KEY is free for upto 500,000 characters per month. If you don't like this then you can use the word `free` instead and special code will attempt to interact with the website
  and use point and clicks to get free translations. However this is extremely slow as pages need to
  be clicked by a bot. Also the translations are uploaded in chunks so you might get weird translations
  at the cutoff point. While the API key will be lightning fast and the translations have been verified
  to be excellent quality. Also, this free mode may break unexpectadly in the future.
  * After the translations are done, you'll get a new folder that is the name of the video with "test_" prepended to it. So `myvideo.mp4` will generate a "text_myvideo" with srt files for all the languages
    * in the example above, you would get
      * `text_myvideo/en.srt`
      * `text_myvideo/es.srt`
      * `text_myvideo/fr.srt`
      * `text_myvideo/zh.srt`
      * `text_myvideo/it.srt`


# How it works

  * Translation from audio -> en.srt is performed by `transcribe-anything`
    * Sadly, `transcribe-anything` can only translate to english subtitles.
  * After the english is generated, DeepL is used as a backend service to translate to english to all other languages.


# Language Reference

### Language Inputs

We use openai whisper for language input. See whisper ai documents for a full supported list


### Language outputs

We use the deepl AI for translation. The language list is as follows:

```
    BG - Bulgarian
    CS - Czech
    DA - Danish
    DE - German
    EL - Greek
    EN - English (unspecified variant for backward compatibility; please select EN-GB or EN-US instead)
    EN-GB - English (British)
    EN-US - English (American)
    ES - Spanish
    ET - Estonian
    FI - Finnish
    FR - French
    HU - Hungarian
    ID - Indonesian
    IT - Italian
    JA - Japanese
    KO - Korean
    LT - Lithuanian
    LV - Latvian
    NB - Norwegian (Bokmål)
    NL - Dutch
    PL - Polish
    PT-BR - Portuguese (Brazilian)
    PT-PT - Portuguese (all Portuguese varieties excluding Brazilian Portuguese)
    RO - Romanian
    RU - Russian
    SK - Slovak
    SL - Slovenian
    SV - Swedish
    TR - Turkish
    UK - Ukrainian
    ZH - Chinese (simplified)
```

Please see [https://www.deepl.com/docs-api/translate-text/](https://www.deepl.com/docs-api/translate-text/) for more information

# Windows

This environment requires you to use `git-bash`.

# Linting

Run `./lint.sh` to find linting errors using `ruff`, `pylint`, `flake8` and `mypy`.

# Releases

  * 1.0.11: Fix macos
  * 1.0.10: Allows app to run when not using hardware acceleration for AI.
  * 1.0.9: Fix settings.json bug in not created directories.
  * 1.0.8: Adds password field and centralizes settings.json under appdirs.
  * 1.0.7: Adds progress bar when doing work.
  * 1.0.6: Adds gui language help for language codes.
  * 1.0.5: Adds webvtt format option.
  * 1.0.4: Adds thread processor so that multiple files can be done one at a time.
  * 1.0.3: Adds gui.
  * 1.0.2: Fix bug.
  * 1.0.1: Adds retry to translation step. Also alerts when the video is done.
  * 1.0.0: Initial release.



# Future Work

### Text to Speech

It would be a good idea to convert the subtitles into a spoken track that can be integrates into a video

  * Eleven labs API
    * Website: https://beta.elevenlabs.io/
    * Rest API: https://docs.elevenlabs.io/api-reference/text-to-speech-stream
    * Python API: https://github.com/elevenlabs/elevenlabs-python