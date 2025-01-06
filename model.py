from sentence_transformers import SentenceTransformer
# from pyvi.ViTokenizer import tokenize
from sklearn.metrics.pairwise import cosine_similarity

from tqdm import tqdm
print("Load model vnCoreNLP")

class SentenceEmbedding():
    def __init__(self, path_model):
        self.path_model = path_model
        self.model = SentenceTransformer(self.path_model)
    def get_embedding(self, articles):
        id_articles, embeddings, titlePapers = [], [], []
        for article in tqdm(articles):
            outputs = self.model.encode(article[1])
            # print(article[1])
            # print(outputs)
            id_articles.append(article[0])
            embeddings.append(outputs)
        return id_articles, embeddings, titlePapers
    def get_model(self):
        return self.model
    def get_embedding_sentence(self, sentence):
        return self.model.encode(sentence).reshape(1, -1)
    def compare_2_sentences(self, sentence1, list_sentence, list_links):

        if len(list_sentence) == 0:
            print("Error: List sentence is empty!")
            return False, []
        i = 0
        for embed in list_sentence:
            score = cosine_similarity(sentence1, embed)
            if score[0][0] > 0.8:
                return True, list_links[i]
            i += 1
        return False, []

