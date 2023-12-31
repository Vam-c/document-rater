from numpy.linalg import norm
import numpy as np     
import sqlite3
from sqlite3 import IntegrityError

def rows_to_dict(columns, data):
    result = []
    for row in data:
        dictionary = {}
        for index in range(len(columns)):
            dictionary[columns[index]] = row[index]
        result.append(dictionary)
    return result

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

def create_subject(name):
    conn = sqlite3.connect("assignment.db")

    try:
        conn.cursor().execute("INSERT INTO subject(name) VALUES(?)", (name,))
        conn.commit()
        conn.close()
    except IntegrityError:
        print("Subject Already exists, using the same database...")

    return 