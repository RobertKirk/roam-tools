# Roam Tools

This is a small collection of scripts and other things which help me work with [Roam Research](https://roamresearch.com/). They're written in python.

## Setup

### Requirements

* Linux
* Bash
* Python 3
* A clipboard manager which enables you to access your clipboard history

### Installing

Run the following commands in this repository:

```bash
python -m venv .roam-ve

source .roam-ve/bin/activate

pip install -r requirements.txt
```

## Usage

Run

```bash
python generate_page.py --arxiv-url https://arxiv.org/abs/1601.01705
```

or


```bash
python generate_page.py --arxiv-id 1601.01705
```

to generate the page.

If you want it to be even quicker, you can copy the `arxiv-to-roam` script (making sure to adjust the paths to point to the correct places) to somewhere on your `$PATH` (i.e. `$HOME/local/bin/arxiv-to-roam`). Then running `arxiv-to-roam` with an arxiv url copied to your clipboard (which you can do on most browsers with `Ctrl-l` then `Ctrl-c`) will put the page title and the contents in your clipboard. You'll need a clipboard manager to access both of them.

## Hacking

If you want to template to look different, or have more information, fork the repository and edit it (or just use a local branch).
