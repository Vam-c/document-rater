from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from numpy.linalg import norm
import numpy as np     
from pathlib import Path

# get_similarity returns the similarity of two documents from similarity matrix.
def get_similarity(doc1, doc2, similarity_array):
    doc1_index = text_files.index(doc1)                                                                                                                                                                                                                      
    doc2_index = text_files.index(doc2)                                                                                                                                                                                                                      
    return similarity_array[doc1_index][doc2_index]

# Combines similarity scores from tf-idf and count vectors with assigned weights.
def combine_similarities(count_similarities, count_weightage, tf_similarities, tf_weightage): 
    similarity = [ [0 for x in range( len(count_similarities) )] for y in range( len(count_similarities) ) ]   
    for doc1 in range(len(count_similarities)):
        for doc2 in range(doc1, len(count_similarities)):
            similarity[doc1][doc2] = count_similarities[doc1][doc2] * count_weightage + tf_similarities[doc1][doc2] * tf_weightage
            similarity[doc2][doc1] = count_similarities[doc1][doc2] * count_weightage + tf_similarities[doc1][doc2] * tf_weightage
    
    return similarity

# computes cosine similarity matrix from vectors.
def compute_cosine_similarity(vectors):
    similarity = [ [0 for x in range( len(vectors) )] for y in range( len(vectors) ) ]   
    for document_1_Index in range(len(vectors)):
        for document_2_Index in range(document_1_Index, len(vectors)):
            vector1 = vectors[document_1_Index]
            vector2 = vectors[document_2_Index]
            value = np.dot(vector1, vector2)/(norm(vector1) * norm(vector2))
            similarity[document_1_Index][document_2_Index] = value
            similarity[document_2_Index][document_1_Index] = value

    return similarity

def fetch_files():
    files = []
    for child in Path('./input').iterdir():
        if child.is_file():
            files.append(child.name)
    return files

text_files = fetch_files()
marks = [8, 10, 3]

documents = [open("./input/" + f).read() for f in text_files]
tfidf = TfidfVectorizer().tfmodel.fit_transform(documents)
countVectors = CountVectorizer().fit_transform(documents).toarray()

pairwise_similarity = tfidf * tfidf.T

tf_similarity = pairwise_similarity.toarray()     
count_similarity = compute_cosine_similarity(countVectors)

# Combine count vector and tfidf scores.
similarity = combine_similarities(count_similarity, 0.3, tf_similarity, 0.7)

print(similarity)


                                                                                                                                                                                                                 

    
