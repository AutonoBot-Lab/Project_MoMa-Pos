from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def cosine_similarity_vectors(vec1, vec2):
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)
    return cosine_similarity(vec1, vec2)[0][0]


def Sort_Similarity(embeddings):
    target_embedding = embeddings['Bowl_Target']
    # 初始化一个字典来保存相似度结果
    similarities = {}
    # 计算每个嵌入向量与"Bowl_Target"的余弦相似度
    for node, embedding in embeddings.items():
        # 使用cosine_similarity函数，注意它期待2D数组作为输入
        sim = cosine_similarity([target_embedding], [embedding])[0][0]
        similarities[node] = sim

    # 根据相似度排序，返回一个列表，内容是(节点, 相似度)元组
    sorted_similarities = sorted(similarities.items(), key=lambda item: item[1], reverse=True)
    # min_sim = sorted_similarities[-1][1]
    # max_sim = sorted_similarities[0][1]
    # normalized_similarities = [(node, (sim - min_sim) / (max_sim - min_sim)) for node, sim in sorted_similarities]

    return sorted_similarities

