### Approach for ner
This doc is meant to briefly describe resources and approaches
used in using the named entity recognizition software from Stanford
to tag the content of the texts

#### Resources
[Software mainpage](https://nlp.stanford.edu/software/CRF-NER.html)
[stanford-ner.jar](http://www.java2s.com/Code/Jar/s/Downloadstanfordnerjar.htm)
[**Models**](https://stanfordnlp.github.io/CoreNLP/index.html#download)

#### Approach
Get the entire CoreNLP and add it to the java $CLASSPATH:
```
path_corenlp=path/to/corenlp/
export CLASSPATH="$CLASSPATH:`realpath $path_corenlp/src/`";
for file in `find $path_corenlp -name "*.jar"`; do 
export CLASSPATH="$CLASSPATH:`realpath $file`";
done;
```
The above can be added to `~/.profile` for continous work with corenlp.

Example usage:
```
java -mx3g edu.stanford.nlp.pipeline.StanfordCoreNLP -file input.txt
```

To use python's NLTK library with the stanford NER, start a StanfordCore Server:
```
java -mx3g edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 
```

Then in python:
```
from nltk.tag.stanford import CoreNLPNERTagger 
sentence="In Denmark there is 7314 kilometers of costline, excluding Greenland and the Faroe Islands"
ner = CoreNLPNERTagger(url="http://localhost:9000')
ner.tag(sentence.split())
```
