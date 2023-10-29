from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

from utils import fetch_files, combine_similarities, compute_cosine_similarity

class AssignmentEvaluator:
    # data -> data is a list of files along with marks. {file, marks}
    def __init__(self, data):
        # files are loaded from /input directory.
        self.text_files = fetch_files()
        # data contains marks of each file.
        self.assignments = data

    # compute_marks computes marks of a document (passed as index)
    def compute_marks(self, documentIndex):
        numerator = 0
        denominator = 0
        for index in range(len(self.similarities)):
            # Skip documents with no marks.
            if (not self.marks[index]): continue

            numerator += self.similarities[index][documentIndex] * self.marks[index] 
            denominator += self.similarities[index][documentIndex]
        if denominator:
            marks = numerator/denominator
        else:
            marks = 0
        return marks

    # get_similarity returns the similarity of two documents from similarity matrix.
    def get_similarity(self, doc1, doc2, similarity_array):
        doc1_index = self.text_files.index(doc1)                                                                                                                                                                                                                      
        doc2_index = self.text_files.index(doc2)                                                                                                                                                                                                                      

        return similarity_array[doc1_index][doc2_index]

    # fit function creates a similarity matrix between all uploaded assignments.
    def fit(self):
        documents = [open("./input/" + f).read() for f in self.text_files]
        tfidf = TfidfVectorizer().fit_transform(documents)
        countVectors = CountVectorizer().fit_transform(documents).toarray()

        pairwise_similarity = tfidf * tfidf.T

        tf_similarity = pairwise_similarity.toarray()     
        count_similarity = compute_cosine_similarity(countVectors)

        # Combine count vector and tfidf scores.
        self.similarities = combine_similarities(count_similarity, 0.3, tf_similarity, 0.7)

        return self.compute_marks(1)



                                                                                                                                                                                                                 

    
