from FlagEmbedding import FlagReranker
from collections import defaultdict
import json
reranker = FlagReranker('namdp-ptit/ViRanker',
                        use_fp16=True)  # Setting use_fp16 to True speeds up computation with a slight performance degradation




def analyze_component_similarity(six_w2h_list, component, similarity_threshold=0.8):
    """
    Phân tích độ tương đồng giữa các bài viết theo 6W2H.
    """
    component_list = [
        article[component] 
        for article in six_w2h_list 
        if article and component in article and article[component] is not None
    ]
    similarity_count = defaultdict(set)
    processed_pairs = set()

    for i in range(len(component_list)):
        for j in range(i + 1, len(component_list)):
            if (i, j) not in processed_pairs:
                if component_list[i] and component_list[j]:
                    score = reranker.compute_score(
                        [component_list[i], component_list[j]],
                        normalize=True
                    )[0]
                else:
                    continue

                if score > similarity_threshold:
                    similarity_count[i+1].add(j+1)
                    similarity_count[j+1].add(i+1)
                    processed_pairs.add((i, j))
                    processed_pairs.add((j, i))

    similarity_count = {k: sorted(list(v)) for k, v in similarity_count.items()}
    filtered_results = {}
    processed_articles = set()

    for article, similar_list in sorted(
        similarity_count.items(),
        key=lambda x: len(x[1]),
        reverse=True
    ):
        if article not in processed_articles:
            filtered_results[article] = similar_list
            processed_articles.add(article)
            processed_articles.update(similar_list)

    filtered_results = {
        article: similar_list
        for article, similar_list in filtered_results.items()
        if len(similar_list) > 1
    }

    # Nếu không có kết quả, trả về bài đầu tiên làm đại diện
    if not filtered_results:
        return {
            "component": component,
            "similarities": [],
            "disimilarities": [
                {
                    "article_id": i + 1,
                    "text": six_w2h_list[i][component]
                }
                for i in range(len(six_w2h_list))
                if component in six_w2h_list[i] and six_w2h_list[i][component] is not None
            ]
        }

    # Trả về các kết quả thông thường nếu có
    similarities = []
    disimilarities = []

    all_articles = set(range(1, len(six_w2h_list) + 1))
    processed_articles = set()

    for article, similar_list in sorted(
        filtered_results.items(),
        key=lambda x: len(x[1]),
        reverse=True
    ):
        if article not in processed_articles:
            similarities.append({
                "article_id": article,
                "text": six_w2h_list[article-1][component],
                "similar_articles": [
                    {
                        "id": similar_id,
                        "text": six_w2h_list[similar_id-1][component]
                    }
                    for similar_id in similar_list
                ],
                "occurrence_count": len(similar_list)
            })
            processed_articles.add(article)
            processed_articles.update(similar_list)

    disimilar_articles = all_articles - processed_articles
    for article_id in disimilar_articles:
        disimilarities.append({
            "article_id": article_id,
            "text": six_w2h_list[article_id-1][component]
        })

    return {
        "component": component,
        "similarities": similarities,
        "disimilarities": disimilarities
    }

def analyze_all_components(six_w2h_list, seen_links):
    """
    Performs similarity analysis for all 6W2H components

    Args:
        six_w2h_list (list): List of dictionaries containing 6W2H analysis
    
    Returns:
        str: JSON string containing analysis results
    """
    components = ["Who", "What", "Where", "When", "Why", "Whom", "How", "HowMuch"]
    
    results = []
    for component in components:
        component_result = analyze_component_similarity(six_w2h_list, component)
        if component_result:  # Only add if there are significant similarities
            results.append(component_result)
    
    final_results = {
        "link": list(seen_links),
        "analysis_results": results,
        "total_components_analyzed": len(results)
    }
    
    return json.dumps(final_results, indent=2, ensure_ascii=False)