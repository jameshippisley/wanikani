# Rendaku information generation scripts

This is an as-is check-in of the scripts which were used to generate
the "Wanikani Rendaku Information" user script.

To regenerate rendaku_information_data.json, do:
       
```
python3 rendaku2json.py > rendaku_information_data.json
```

To test how many times the script is right and wrong about whether a
word rendakus, and print all the messages for the cases where the
script is wrong, do:

```
python3 rendaku_test.py        
```

These scripts are not fully functional at this time because I am not
checking in the full database of Wanikani vocab and kanji readings. A
small sample of data (enough to make the scripts run) is checked in
the the files

* data/kanji.txt
* data/vocab.txt

I am not checking in the full database so as not to infringe Wanikani
copyright. To regenerate the full database, you will need to populate
kanji.txt and vocab.txt with the full Wanikani database. I
originally generated these files using
http://wanikanitoanki.com, but that tool is no longer working, so
another method would be needed. It would be nice to update the
scripts here to automatically populate kanji.txt and vocab.txt via the
user's API key.

The heart of the rendaku predictor is the function "predict_rendaku()"
in data/vocab.py. If you want to improve the script's accuracy, you
would need to tweak that function.

          

        
        

     