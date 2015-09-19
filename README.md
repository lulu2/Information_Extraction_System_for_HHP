# Information_extraction_frame_for_HHP

This repo contains implementation of information extraction frames using current NLP tools, including StanfordCore nlp, nltk, openie, etc.

extraction_java folder contains programs used as base for webapp, which is based on Stanford core nlp. It requires both stanford-corenlp.jar and stanford-corenlp-models.jar to run.

extraction_python has programs in python. One version uses a testing simple coreference solution based on NER and POS bundled with nltk, one uses Stanford coreference resolution, with another python wrapper.

Above two are based on openie 4.0. To run them openie-assembly.jar should be included in the working directory. openie is written in scala, one could use sbt to generate this jar file as explained on its github repo.

inintial_effort is an early version of extraction frame, which is based on ollie, openie 3.0.

related folder contains related works, including a simple IE program based on dependency graph analysis.
