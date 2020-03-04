
# readability_classification_w122019_y121059

## Introduction
Readability is the ease with which a reader can understand a written text, a score to know how it will be accessible to readers. From a linguistic perspective, the readability of a text is determined by much more than a few superﬁcial textual features. For example, does the reader know most of the words? Does the text contain complex grammatical structures? Are there enough connectives to explain the ﬂow of the text? Is the text about a lot of different concepts? Measuring the readability of a text has a long history, mainly in the educational domain. **Second Language Acquisition** (SLA) is applied as a base method of combining Lexical and Syntactic features.
**Our article:**  

## Dataset

We use 2 dataset in English.

**OneStopCorpusEnglish**
This dataset is collected from **ACL anthology** and created by **Sowmya Vajjala** and **Ivana Lucic** from the Iowa State University, USA.

It consists of about 509 documents classiﬁed into 3 reading levels for English as Second Language learners: 

 - Advanced
 - Intermediate
 - Elementary


The original articles of this dataset is collected from **The Guardian newspaper** and had been rewritten to suit the three levels of English learners on onestopenglish.com, a website run by MacMillan Education.

*More Information:* [https://www.aclweb.org/anthology/W18-0535/](https://www.aclweb.org/anthology/W18-0535/)

*Download:* [https://github.com/nishkalavallabhi/OneStopEnglishCorpus/tree/master/Texts-SeparatedByReadingLevel](https://github.com/nishkalavallabhi/OneStopEnglishCorpus/tree/master/Texts-SeparatedByReadingLevel)

**Cambridge Readability Dataset**
This dataset is created by **Menglin Xia**, **Ekaterina Kochmar**, and **Ted Briscoe** from University of Cambridge.
It composes of reading passages from the 5 reading levels which target at ESL learners: 

  - CPE
 - CAE
 - FCE
 - PET
-  KET

and contains about 282 documents.

*More Information and Download:* [https://ilexir.co.uk/datasets/index.html](https://ilexir.co.uk/datasets/index.html)

## Evaluation

**Accuracy:** this is the percentage let us know how well the model is. It is calculated by dividing the number of matching label by the total number of reference label. For each of the dataset, our method is calculating the accuracy of each level and then get the average number to get the ﬁnal accuracy. 

## Our method:


## Result:
**OneStopCorpusEnglish** best performance: **81.71%**

**Cambridge Readability Dataset** best performance : **70.56%**

## How to run
**Required packages:**

 - nltk
 - numpy
 - statistics


Guide for MacOS.
> `cd Readability-Classification-W122019-Y121059`<br/>
> `alias runn='bash run/run.sh'`<br/>
> `runn`


