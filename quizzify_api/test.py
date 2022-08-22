from quizzify_core.quiz_generation.quiz_assembler import test


text = """In the morning, according to images recorded by TV Globo, the Youtuber asks Bolsonaro about the seal given to the project that limited the plea bargain mechanism. Right after that, he calls Bolsonaro a "centrão [pork-barrel faction in Congress] sweetheart", "a rascal" and a "lazy slob".

"I want to see you have the guts to talk to me, 'centrão [pork-barrel faction in Congress] sweetheart'. Valdemar da Costa Neto, he owns you", says Wilker, quoting the leader of the PL, a party of which Bolsonaro is a part.

As the YouTuber spoke, the president tried to exit the place, but came back and grabbed Wilker by the collar.

Then, with more controlled tempers, they talk. "I can't be a 100% president, it's going to displease some people in one thing or another".

Bolsonaro defended the alliance with the pork barrel politics and said that in order to govern, he needs the support of the group, which includes about 300 of the 513 federal deputies"""


test(text)