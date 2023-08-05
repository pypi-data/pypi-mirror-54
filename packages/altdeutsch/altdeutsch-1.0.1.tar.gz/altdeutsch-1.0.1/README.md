[![PyPI](https://img.shields.io/pypi/v/altdeutsch)](https://pypi.org/project/altdeutsch/) [![Build Status](https://travis-ci.org/clemsciences/old_high_german_texts.svg?branch=master)](https://travis-ci.org/clemsciences/old_high_german_texts)

# Parser of Referenzkorpus Althochdeutsch exports

## Installation

```bash
$ pip install althochdeutsch
```


## License

License of the software: [MIT License](https://choosealicense.com/licenses/mit/)

License of the data: [CC BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/)

The [Referenzkorpus Altdeutsch project](https://www.deutschdiachrondigital.de/) is at the origin of annotations of the 
[data](https://www.laudatio-repository.org/browse/corpus/rmgpfWoB6bp_h9Naq45A/corpus_deutsch-diachron-digital---referenzkorpus-altdeutsch_0-1_1556880883).

## Code usage

```python
import os
from altdeutsch.reader import read_export
from altdeutsch import PACKDIR
hildebrandslied = read_export(os.path.join(PACKDIR, "tests", "data", "hildebrandslied.txt"))
print(hildebrandslied["tok"])
```

You have now the Hildebrandslied text!
