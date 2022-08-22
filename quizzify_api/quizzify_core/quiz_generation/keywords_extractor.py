from flashtext import KeywordProcessor
import traceback
import pke
import string
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')


def get_nouns_multipartite(content):
    out = []
    try:
        extractor = pke.unsupervised.MultipartiteRank()
        extractor.load_document(input=content, language='en')
        #    not contain punctuation marks or stopwords as candidates.
        pos = {'PROPN', 'NOUN'}
        #pos = {'PROPN','NOUN'}
        stoplist = list(string.punctuation)
        stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
        stoplist += stopwords.words('english')
        # extractor.candidate_selection(pos=pos, stoplist=stoplist)
        extractor.candidate_selection(pos=pos)
        # 4. build the Multipartite graph and rank candidates using random walk,
        #    alpha controls the weight adjustment mechanism, see TopicRank for
        #    threshold/method parameters.
        extractor.candidate_weighting(alpha=1.1,
                                      threshold=0.75,
                                      method='average')
        keyphrases = extractor.get_n_best(n=15)

        for val in keyphrases:
            out.append(val[0])
    except:
        out = []
        traceback.print_exc()

    return out


def get_keywords(originaltext, summarize_text=None):
    keywords = get_nouns_multipartite(originaltext)
    print("keywords unsummarized: ", keywords)
    if summarize_text:
        keyword_processor = KeywordProcessor()
        for keyword in keywords:
            keyword_processor.add_keyword(keyword)

        keywords_found = keyword_processor.extract_keywords(summarize_text)
        keywords_found = list(set(keywords_found))
        print("keywords_found in summarized: ", keywords_found)

        important_keywords = []
        for keyword in keywords:
            if keyword in keywords_found:
                important_keywords.append(keyword)

        return keywords_found

    return keywords
