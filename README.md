# utbtn
Underground Transport Battalion: An app for transporting a file across two networks that are not connected via printed pages.

## Motivation
I have been in at a workplace where the internal network is completely separated from the internet,
hence one cannot possibly get any files from the internet.

The only thing that would have been possible is that, one could open a text file,
print it out, then type it again at the computer that is connected to the internal network,
which was a time-consuming job, and would be unrealistic for any other file than a text file.

With this project, I came up with a way to "generalize" the idea of this task to a general file.

Note that the first version of this app is meant not to use any clever external OCR software
so that one could deploy this solution in a place without internet.

## Installation
```
pip install .
```

## Usage
For encoding a file called "file.txt" to printable A4 images.
```
utbtn encode file.txt
```

For reconstructing file.txt from printable A4 images.
```
utbtn decode file.txt file_0.png file_1.png file_2.png
```