#jieba-calcu

with jieba we can cut the sentence into word.
and this tools is for us to generate a new "Launch probability matrix" and a new "Transition probability matrix"

## quick start
```
import jieba-calcu # import package
from jieba-calcu import JiebaCalcu # import class
filepaths = ['./docs','../pre_docs'] # set input-file path
mJiebaCalcu = JiebaCalcu(filepaths) # instance
res = mJiebaCalcu.word_discovery(1.0) # word-discovery

```
