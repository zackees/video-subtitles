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

#### Short hand language codes

```
af,am,ar,as,az,ba,be,bg,bn,bo,br,bs,ca,cs,cy,da,
de,el,en,es,et,eu,fa,fi,fo,fr,gl,gu,ha,haw,he,hi,
hr,ht,hu,hy,id,is,it,ja,jw,ka,kk,km,kn,ko,la,lb,
ln,lo,lt,lv,mg,mi,mk,ml,mn,mr,ms,mt,my,ne,nl,nn,
no,oc,pa,pl,ps,pt,ro,ru,sa,sd,si,sk,sl,sn,so,sq,
sr,su,sv,sw,ta,te,tg,th,tk,tl,tr,tt,uk,ur,uz,vi,
yi,yo,zh
```

#### Full Language codes will also work

```
Afrikaans,Albanian,Amharic,Arabic,Armenian,Assamese,Azerbaijani,
Bashkir,Basque,Belarusian,Bengali,Bosnian,Breton,Bulgarian,Burmese,
Castilian,Catalan,Chinese,Croatian,Czech,Danish,Dutch,English,
Estonian,Faroese,Finnish,Flemish,French,Galician,Georgian,German,
Greek,Gujarati,Haitian,Haitian Creole,Hausa,Hawaiian,Hebrew,Hindi,
Hungarian,Icelandic,Indonesian,Italian,Japanese,Javanese,Kannada,
Kazakh,Khmer,Korean,Lao,Latin,Latvian,Letzeburgesch,Lingala,
Lithuanian,Luxembourgish,Macedonian,Malagasy,Malay,Malayalam,
Maltese,Maori,Marathi,Moldavian,Moldovan,Mongolian,Myanmar,Nepali,
Norwegian,Nynorsk,Occitan,Panjabi,Pashto,Persian,Polish,Portuguese,
Punjabi,Pushto,Romanian,Russian,Sanskrit,Serbian,Shona,Sindhi,
Sinhala,Sinhalese,Slovak,Slovenian,Somali,Spanish,Sundanese,Swahili,
Swedish,Tagalog,Tajik,Tamil,Tatar,Telugu,Thai,Tibetan,Turkish,
Turkmen,Ukrainian,Urdu,Uzbek,Valencian,Vietnamese,Welsh,Yiddish,
Yoruba
```

# Windows

This environment requires you to use `git-bash`.

# Linting

Run `./lint.sh` to find linting errors using `ruff`, `pylint`, `flake8` and `mypy`.

# Releases

  * 1.0.1: Adds retry to translation step. Also alerts when the video is done.
  * 1.0.0: Initial release