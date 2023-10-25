from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

from utils import fetch_files, combine_similarities, compute_cosine_similarity

class Comparator:
    def __init__(self):
        self.text_files = fetch_files()
        self.marks = [8, 7, 10, None]

    # compute_marks computes marks of a document (passed as index)
    def compute_marks(self, documentIndex, similarities):
        numerator = 0
        denominator = 0
        for index in range(len(similarities)):
            # Skip documents with no marks.
            if (not self.marks[index]): continue

            print(similarities[index][documentIndex])
            numerator += similarities[index][documentIndex] * self.marks[index] 
            denominator += similarities[index][documentIndex]
        if denominator:
            marks = numerator/denominator
        else:
            marks = 0
        return marks

    def compute_marks_of_document(self, documentIndex):
        documents = [open("./input/" + f).read() for f in self.text_files]
        tfidf = TfidfVectorizer().fit_transform(documents)
        countVectors = CountVectorizer().fit_transform(documents).toarray()

        pairwise_similarity = tfidf * tfidf.T

        tf_similarity = pairwise_similarity.toarray()     
        count_similarity = compute_cosine_similarity(countVectors)

        # Combine count vector and tfidf scores.
        similarity = combine_similarities(count_similarity, 0.3, tf_similarity, 0.7)

        return self.compute_marks(documentIndex, similarity)

    # get_similarity returns the similarity of two documents from similarity matrix.
    def get_similarity(self, doc1, doc2, similarity_array):
        doc1_index = self.text_files.index(doc1)                                                                                                                                                                                                                      
        doc2_index = self.text_files.index(doc2)                                                                                                                                                                                                                      

        return similarity_array[doc1_index][doc2_index]



                                                                                                                                                                                                                 

    
