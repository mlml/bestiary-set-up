# Bestiary analysis and set up

These instructions assume that the user has a superuser account .

Adding new datasets
-------------------

First step is to upload the aligned corpus to the prosodylab.org server via scp or some other similar tool.  The location of the corpora is 
`/home/linguistics/chael/data/PolyglotData`.  In that folder, you should see many different corpora currently there,
i.e. `cont`, `dimensions`, `fogirA4`, etc.  These corpora are structured so that all audio and alignments are in
a `textgrid-wav` subfolder, with the wav and TextGrid files separated by speaker (this is necessary for proper speaker
parsing when importing the dataset).  The default format supported is that output by the Montreal Forced Aligner.

Once the corpus is all uploaded, go to the [http://prosodylab.org/pg/](http://prosodylab.org/pg/) home page and the list of corpora should update to
include the new corpus.

Setting up the corpus for bestiary
----------------------------------

In general, you can follow the [basic tutorial for ISCAN](https://iscan-server.readthedocs.io/en/latest/tutorials_iscan.html).

The steps specifically needed from it are:

1. Import
2. Syllabic subset
3. Syllables
4. Pause subset
5. Utterances (Set the minimum pause duration high, i.e. 10000 ms to ensure one utterance per file)

In addition to the enrichment steps in the basic tutorial, pitch tracks must be encoded via the `Pitch tracks` button under
acoustics.  Pitch can be relativized per speaker (and optionally per segment) via the `Relativize track` enrichment.

Once these are done, then the bestiary plot in "Intonational bestiary" for the corpus should work.

If you would like to add properties to sound files (i.e., experimental conditions, etc.), those can be added via the 
`Properties from a CSV` enrichment.  The structure of the file mirrors that of the speaker CSV used in the tutorial (first column
for the name of the sound file (no .wav extension), remaining columns are named properties per sound file).

Correcting pitch tracks
-----------------------

Go to the corpus page for the dataset, and make a new query under "Utterances", with the name of something like "Pitch correction".

Once it's been run, click on the magnifying glass of the first row to inspect the utterance with its pitch track at the bottom.
The primary pitch correction functions currently available are doubling and halving (to fix octave jump errors).  Smoothing
and removing points are also available for non-octave errors.  New pitch tracks with different settings can be generated
first before correction.  Once you're happy with the track, clicking "Save pitch" will upload it to the database.

If you need to continue correcting pitch in a different session, you can refresh the query and sort by the "Pitch last edited"
field, which will allow you to find all the ones that haven't been updated and start on those.