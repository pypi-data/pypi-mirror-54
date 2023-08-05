# Coreference Resolution wrapper

Coreference Resolution is the task of finding all expressions that refer to the same entity in a text. It is an important step for a lot of higher level NLP tasks that involve natural language understanding such as document summarization, question answering, and information extraction.

This is a simple library that wrap two Coreference Resolution models form StanfordNLP package: the statistic and neural models. We use here the SpaCy package to load the neural model (a.k.a, *NeuralCoref*), and the stanfordnlp package to load the statistic model (a.k.a, *CoreNLPCoref*).

## Requirements

```bash
pip3 install spacy
pip3 install stanfordnlp
pip3 install wrapperCoreference
```

StanfordNLP also require the manual downloading of a core of modules, review [here](https://stanfordnlp.github.io/CoreNLP/download.html) for more details.

```bash
wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip
```

## Methods
Example of usage of the neural model 
```python
from wrapperCoreference import WrapperCoreference
wc = WrapperCoreference()
wc.NeuralCoref(u'My sister has a dog. She loves him.')
#output: [{'start': 21, 'end': 24, 'text': 'She', 'resolved': 'My sister'}, {'start': 31, 'end': 34, 'text': 'him', 'resolved': 'a dog'}]
```


Example of usage of the statistic model 
```python
from wrapperCoreference import WrapperCoreference
wc = WrapperCoreference()
wc.setCoreNLP('/tmp/stanford-corenlp-full-2018-10-05')
print(wc.CoreNLPCoref(u'My sister has a dog. She loves him.'))
#output: [{'start': 31, 'end': 34, 'text': 'him', 'resolved': 'a dog', 'fullInformation': [{'start': 14, 'end': 19, 'text': 'a dog'}]}, {'start' : 21, 'end': 24, 'text': 'She', 'resolved': 'My sister', 'fullInformation': [{'start': 0, 'end': 9, 'text': 'My sister'}]}]
```
