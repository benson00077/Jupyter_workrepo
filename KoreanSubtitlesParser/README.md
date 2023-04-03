# Usage
A parent file for 3 modules processing korean subtitles and it's translation.

Python 3.9.0 under 64 bit (AMD64) windows OS

Run scripts as below order
```bash
# for ko pos
$ python ./dumpJsonForKoPos/main.py
# for translation>
$ python ./dumpJsonForAlignedTraslation/main.py
```

# Roadmap
- [x] update directory logic && .gitignore 
  - [x] csv && json dumper might use same origin subtitles file, need some opt
- [x] docs for each files, use notes from ipynb
- [ ] time.time()
- [ ] Refactor
  - [ ] Laverage parent module && child modules feature, abstract repeated logic
  - [ ] Main entry point for all 3 submoduels
