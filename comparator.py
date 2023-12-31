from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

from utils import combine_similarities, compute_cosine_similarity

class AssignmentEvaluator:
    # compute_marks computes marks of a document (passed as index)
    def compute_marks(self, documentIndex):
        numerator = 0
        denominator = 0
        for index in range(len(self.similarities)):
            marks = self.assignments[index]["marks"]
            # Skip documents with no marks.
            if (not marks): continue

            numerator += self.similarities[index][documentIndex] * float(marks) 
            denominator += self.similarities[index][documentIndex]

        # Check for div by 0.
        if not denominator:
            predicted_marks = 0
        else:
            predicted_marks = numerator/denominator

        return predicted_marks

    # get_similarity returns the similarity of two documents from similarity matrix.
    def get_similarity(self, doc1, doc2, similarity_array):
        doc1_index = self.text_files.index(doc1)                                                                                                                                                                                                                      
        doc2_index = self.text_files.index(doc2)                                                                                                                                                                                                                      

        return similarity_array[doc1_index][doc2_index]

    # fit function creates a similarity matrix between files
    # data -> data is a list of files along with marks. {file, marks}
    def fit(self, data):
        # file paths and marks are stored in assignments.
        self.assignments = data
        documents = [open(assignment['path']).read() for assignment in self.assignments]
        tfidf = TfidfVectorizer().fit_transform(documents)
        countVectors = CountVectorizer().fit_transform(documents).toarray()

        pairwise_similarity = tfidf * tfidf.T

        tf_similarity = pairwise_similarity.toarray()     
        count_similarity = compute_cosine_similarity(countVectors)

        # Combine count vector and tfidf scores.
        self.similarities = combine_similarities(count_similarity, 0.3, tf_similarity, 0.7)




                                                                                                                                                                                                                 

    
