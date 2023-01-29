import importlib.resources
import os

# TODO: how to get this flat?
from match_engine.match_engine import MatchEngine

words_file = str(importlib.resources.path("static", "words.txt"))
# TODO: why doesn't this work?
# match_engine = MatchEngine.from_file(words_file)
with open(words_file) as f:
    match_engine = MatchEngine(f.read())
