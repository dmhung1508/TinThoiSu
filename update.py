import numpy as np
import time,traceback
import openai
from tqdm import tqdm
from collections import Counter
from database import Database
from pymongo import MongoClient
from generate_openai import generate_new_paper, generate_title_paper, generate_keyword, generate_summary_paper, generate_keyword_of_cluster,generate_keyword_ver2, generate_new_paper_comment
from ranking import ranking_clustering, ranking_algorithm
from audio import getAudio, generate_audio
import traceback
import uuid
from fact import check_fact
from utils import clean_text
def most_frequent(List):
    counter = 0
    num = List[0]
     
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
 
    return num

def update_clusters(config, clusters_outputs, posts, list_data_clean, embeddings, time_now, esp, model):
    # score_cluster = ranking_clustering(clusters_outputs, posts, time_now)
    score_cluster = ranking_algorithm(clusters_outputs, posts, list_data_clean, time_now, model, config)
    db = Database(config, time_now)

    clusters_outputs = dict(sorted(score_cluster.items(), key=lambda item: item[1]['score'], reverse=True))
    new_cluster_outputs = {}
    for idx in clusters_outputs:
        new_cluster_outputs[idx] = clusters_outputs[idx]["ids"]

    list_cluster = []
    count_cluster = 0
    listTitles = []
    listSummary = []
    listImageContent = []
    list_text = []
    listID = []
    for ids in new_cluster_outputs:
        new_post = {}
        titlePaper = str(ids)
        new_post["name"] = str(ids)
        newPaper = ""
        summaryPaper = ""

        try:
            #newPaper = generate_new_paper_comment(new_cluster_outputs[ids], list_data_clean, config)

            content = []
            for id in tqdm(new_cluster_outputs[ids]):
                content.append(list_data_clean[id][1])

                
            #print("newPaper:",newPaper)
        except Exception as e:
            print(traceback.format_exc())
            print("error generate new paper")
            # Sử dụng giá trị dự phòng cho newPaper nếu gặp lỗi
            newPaper = list_data_clean[ids][1]  # Nội dung bài báo đầu tiên
            print("Error generating new paper:", e)
            content = list_data_clean[ids][2]



        try:
            titlePaper = generate_title_paper(new_cluster_outputs[ids], list_data_clean, config)
            print("titlePaper:", titlePaper)
        except Exception as e:
            titlePaper = ""
            print("Error generating title paper:", e)
            traceback.print_exc()

        try:
            if count_cluster < config.CLUSTER_TO_DAY:
                #summaryPaper = generate_summary_paper(new_cluster_outputs[ids], list_data_clean, config)
                #print("summaryPaper: ", summaryPaper)
                pass
        except:
            summaryPaper = ""

        try:
            #text_6w2h = generate_6w2h_cluster(new_cluster_outputs[ids], list_data_clean, config)
            text_6w2h = ""
        except:
            text_6w2h = ""
            print("error generate 6w2h")
            traceback.print_exc()

        new_post["sumaryCluster"] = titlePaper
        # new_post["keywords"] = keyword
        new_post["createdAt"] = time_now
        new_post["updatedAt"] = time_now
        new_post["newPaper"] = newPaper
        new_post['text_6w2h'] = text_6w2h
        new_post["ids"] = score_cluster[ids]['ids']
        new_post["score"] = score_cluster[ids]["score"]
        list_cluster.append(new_post)

        if count_cluster < config.CLUSTER_TO_DAY:
            listTitles.append(titlePaper)
            listSummary.append(summaryPaper)
            listImageContent.append(posts[score_cluster[ids]['ids'][0]]["imageContents"])
            listID.append(score_cluster[ids]['ids'][0])
            list_text.append(content)
        count_cluster += 1

    if count_cluster >= config.CLUSTER_TO_DAY:
        # try:
        #     keyword = generate_keyword_ver2(listTitles, config)
        # except:
        #     keyword = ""
        #     print("error apikey title keyword")

        # insert 8amToDay
        # try:
        #     generate_audio(keyword, "audio/audio.mp3", config)
        # except:
        #     print("lõi voice")
        #     pass

        todayNews = {}
        #todayNews["keywords"] = keyword
        todayNews["createdAt"] = time_now
        todayNews["news"] = []

        for idx in range(len(listTitles)):
            news = {}
            news["title"] = listTitles[idx]
            news["summary"] = listSummary[idx]
            news["text"] = list_text[idx]
            if idx == 0:
                first = "tin thứ nhất: "
            elif idx == 1:
                first = "tin thứ hai: "
            elif idx == 2:
                first = "tin thứ ba: "
            elif idx == 3:
                first = "tin thứ tư: "
            elif idx == 4:
                first = "tin thứ năm: "
            elif idx == 5:
                first = "tin thứ sáu: "
            elif idx == 6:
                first = "tin thứ bảy: "
            elif idx == 7:
                first = "tin thứ tám: "

            text_audio = first + listTitles[idx] + ". " + listSummary[idx]
            news["createdAt"] = time_now
            news["imageContents"] = listImageContent[idx]
            # file_audio_save = "audio" + "/" + str(idx) + ".mp3"

            # try:
            #     generate_audio(text_audio, file_audio_save, config)
            #     # getAudio(text_audio, "audio.mp3", db)
            # except:
            #     pass



            # with open(file_audio_save, 'rb') as mp3_file:
            #     mp3_content = mp3_file.read()

            # news["audio"] = mp3_content
            news["id"]= str(uuid.uuid4())
            todayNews["news"].append(news)

        db.delete_todaynews()
        time.sleep(1)
        print("delete successfull")

        db.vn_newflow["todaynews"].insert_one(todayNews)

    db.delete_db()

    #insert database
    for cluster in list_cluster:
        id_post = cluster["ids"].copy()
        cluster_insert = cluster.copy()
        cluster_categori = cluster.copy()

        listCategories = []

        for ids in id_post:
            if "sourceCategoryId" in posts[ids] and "newPaper" not in posts[ids]:
                if posts[ids]["sourceCategoryId"] != "097912d8-eb57-4c1f-8a8a-64ea02e52030":
                    listCategories.append(posts[ids]["sourceCategoryId"])
        if len(listCategories) == 0:
            continue

        maxFrequently_category = most_frequent(listCategories)

        list_time = [posts[idx]["createdAt"] for idx in id_post]
        list_imageContents = [posts[idx]["imageContents"] for idx in id_post]

        sorted_time = sorted(list_time, key=lambda x: x.timestamp(), reverse=True)
        cluster_insert["updatedAt"] = sorted_time[0]
        keyword_cluster = ""
        try:
            keyword_cluster = generate_keyword_of_cluster(cluster_insert["sumaryCluster"], config)
        except:
            keyword_cluster = "None"
            pass
        all_links = []
        offical_paper = []
        offical_link = []
        for idx in id_post:
            all_links.append(posts[idx]["link"])
            if posts[idx]["type"] not in ["FB_POST", "YOUTUBE", "TIKTOK", "YOUTUBE_SHORT"]:
                offical_paper.append(posts[idx]["textContent"])
                offical_link.append(posts[idx]["link"])
            # print("-----------------")
            # print(posts[idx])
        cluster_insert["id_post"] = id_post
        cluster_insert["postId"] = id_post[0]
        cluster_insert["links"] = all_links
        cluster_insert["keywords"] = keyword_cluster
        cluster_insert["categoryId"] = maxFrequently_category
        cluster_insert["createdDate"] = time_now.strftime("%Y-%m-%d %H")

        # cluster_insert["createdDate"] = sorted_time[0].strftime("%Y-%m-%d %H")
        cluster_insert["createdDate"] = time_now.strftime("%Y-%m-%d %H")
        cluster_insert["imageContents"] = list_imageContents
        list_sentences_cluster = list(
            db.vn_newflow["unseen_cluster"]
            .find({}, {"_id": 1, "embedding": 1, "sentence": 1, "all_link": 1})  # Chỉ lấy các trường cần thiết
            .sort("createdAt", -1)  # Sắp xếp theo trường "createdAt" giảm dần
            .limit(200)  # Lấy tối đa 20 tài liệu
        )

        # Lấy các ID của các tài liệu mới nhất
        latest_ids = [doc['_id'] for doc in list_sentences_cluster]

        # Chuyển đổi "embedding" từ danh sách Python về numpy.ndarray
        latest_embeds = [np.array(doc['embedding'], dtype=np.float32) for doc in list_sentences_cluster]
        latest_links = [doc['all_link'] for doc in list_sentences_cluster]
        db.vn_newflow["unseen_cluster"].delete_many({"_id": {"$nin": latest_ids}})
        embed_keyword = model.get_embedding_sentence(cluster_insert["keywords"])
        status, links = model.compare_2_sentences(embed_keyword, latest_embeds, latest_links)
        if status:
            cluster_insert["isUnseen"] = False
            cluster_insert["newLinkList"] =[]
        else:
            cluster_insert["isUnseen"] = True
            cluster_insert["newLinkList"] = list(set(all_links) - set(links))
            
            db.vn_newflow["unseen_cluster"].insert_one({
                "sentence": cluster_insert["keywords"], 
                "createdAt": time_now, 
                "embedding": embed_keyword.tolist(),  # Chuyển numpy.ndarray sang danh sách Python
                "all_link": all_links
            })

        clusterInsert = db.vn_newflow["clusters"].insert_one(cluster_insert)
        # clusterCategori = db.vn_newflow["clusters"].insert_one(cluster_categori)

        id_cluster = clusterInsert.inserted_id
        # id_clusterCategori = clusterCategori.inserted_id
        count_index = 0

        first_article = {}
        first_article["title"] = cluster_insert["sumaryCluster"]

        first_article["description"] = ""
        for idxs in id_post:
            first_article["sourceId"] = posts[idxs]["sourceId"]
            first_article["imageContents"] = list_imageContents
            first_article["videoContents"] = posts[idxs]["videoContents"]
            first_article["createdAt"] = posts[idxs]["createdAt"]
            first_article["postedAt"] = posts[idx]["postedAt"]
            first_article["link"] = posts[idxs]["link"]
            first_article["renderedContent"] = posts[idxs]["renderedContent"]
            first_article["updatedAt"] = cluster_insert["updatedAt"]
            try:
                if posts[idxs]["classification"] is not None:
                    first_article["classification"] = posts[idxs]["classification"]
                else:
                    first_article["classification"] = "NORMAL"
            except:
                first_article["classification"] = "NORMAL"
            
            try:
                if posts[idxs]["probabilityOfClassification"] is not None:
                    first_article["probabilityOfClassification"] = posts[idxs]["probabilityOfClassification"]
                else:
                    first_article["probabilityOfClassification"] = 0.0
            except:
                first_article["probabilityOfClassification"] = 0.0
            break
        first_article["textContent"] = cluster_insert["newPaper"]
        first_article["text_6w2h"] = cluster_insert["text_6w2h"]
        first_article["likes"] = 0
        first_article["shares"] = 0
        first_article["type"] = "AI"
        first_article["comments"] = 0
        first_article["totalReactions"] = 0
        first_article["editedTextContent"] = 0
        first_article["isPositive"] = False
        first_article["isNegative"] = False
        first_article["clusterId"] = id_cluster
        first_article["index"] = 0
        first_article["sourceCategoryId"] = maxFrequently_category
        result = db.vn_newflow["articles"].insert_one(first_article)

        for idx in id_post:
            count_index += 1
            new_article = {}
            if posts[idx]["type"] in ["FB_POST", "YOUTUBE", "TIKTOK", "YOUTUBE_SHORT" ]:
                new_article["title"] = posts[idx]["title"]
                new_article["sourceId"] = posts[idx]["sourceId"]
                new_article["description"] = "string"
                new_article["imageContents"] = posts[idx]["imageContents"]
                new_article["videoContents"] = posts[idx]["videoContents"]
                new_article["link"] = posts[idx]["link"]
                new_article["type"] = posts[idx]["type"]
                new_article["likes"] = posts[idx]["likes"]
                new_article["shares"] = posts[idx]["shares"]
                new_article["comments"] = posts[idx]["comments"]
                new_article["totalReactions"] = posts[idx]["totalReactions"]
                new_article["editedTextContent"] = posts[idx]["editedTextContent"]
                new_article["isPositive"] = False
                new_article["isNegative"] = False
                new_article["clusterId"] = id_cluster
                new_article["createdAt"] = posts[idx]["createdAt"]
                new_article["renderedContent"] = posts[idx]["renderedContent"]
                new_article["updatedAt"] = time_now
                new_article["index"] = count_index
                new_article["postedAt"] = posts[idx]["postedAt"]
                try:
                    if posts[idx]["classification"] is not None:
                        new_article["classification"] = posts[idx]["classification"]
                    else:
                        new_article["classification"] = "NORMAL"
                except:
                    new_article["classification"] = "NORMAL"
                try:
                    if posts[idx]["probabilityOfClassification"] is not None:
                        new_article["probabilityOfClassification"] = posts[idx]["probabilityOfClassification"]
                    else:
                        new_article["probabilityOfClassification"] = 0.0
                except:
                    new_article["probabilityOfClassification"] = 0.0
                if "sourceName" in posts[idx]:
                    new_article["sourceName"] = posts[idx]["sourceName"]
                else:
                    new_article["sourceName"] = "Null"
                try:
                    new_article["sourceCategoryId"] = posts[idx]["sourceCategoryId"]
                    new_article["sourceLink"] = posts[idx]["sourceLink"]
                    new_article["sourceType"] = posts[idx]["sourceType"]
                    new_article["sourceAvatar"] = posts[idx]["sourceAvatar"]
                except:
                    new_article["sourceCategoryId"] = "Null"
                    new_article["sourceLink"] = "Null"
                    new_article["sourceType"] = "Null"
                    new_article["sourceAvatar"] = "Null"
                # new_article["score"] = cluster_insert["score"][cnt-1]
                # if len(offical_paper) == 0:
                #     new_article["isLegit"] = False
                #     new_article["offical_link"] = []
                # else:
                #     offical_paper_text = "\n".join(offical_paper)
                #     if check_fact(posts[idx]["textContent"], offical_paper_text):
                #         new_article["isLegit"] = True
                #         new_article["offical_link"] = offical_link
                #     else:
                #         new_article["isLegit"] = False
                #         new_article["offical_link"] = []
                new_article["FactCheck"], new_article["isLegit"] = check_fact(posts[idx]["textContent"], offical_paper, offical_link)
                if "TopicsOnContents" in posts[idx]:
                    new_article["TopicsOnContents"] = posts[idx]["TopicsOnContents"]
                result = db.vn_newflow["articles"].insert_one(new_article)
            else:
                new_article["title"] = posts[idx]["title"]
                new_article["textContent"] = posts[idx]["textContent"]
                new_article["sourceId"] = posts[idx]["sourceId"]
                new_article["description"] = "string"
                new_article["imageContents"] = posts[idx]["imageContents"]
                new_article["videoContents"] = posts[idx]["videoContents"]
                new_article["link"] = posts[idx]["link"]
                new_article["type"] = posts[idx]["type"]
                new_article["likes"] = posts[idx]["likes"]
                new_article["shares"] = posts[idx]["shares"]
                new_article["comments"] = posts[idx]["comments"]
                new_article["totalReactions"] = posts[idx]["totalReactions"]
                new_article["editedTextContent"] = posts[idx]["editedTextContent"]
                new_article["renderedContent"] = posts[idx]["renderedContent"]
                new_article["postedAt"] = posts[idx]["postedAt"]
                new_article["isPositive"] = False
                new_article["isNegative"] = False
                new_article["clusterId"] = id_cluster
                new_article["createdAt"] = posts[idx]["createdAt"]
                new_article["updatedAt"] = time_now
                try:
                    if posts[idx]["classification"] is not None:
                        new_article["classification"] = posts[idx]["classification"]
                    else:
                        new_article["classification"] = "NORMAL"
                except:
                    new_article["classification"] = "NORMAL"
                try:
                    if posts[idx]["probabilityOfClassification"] is not None:
                        new_article["probabilityOfClassification"] = posts[idx]["probabilityOfClassification"]
                    else:
                        new_article["probabilityOfClassification"] = 0.0
                except:
                    new_article["probabilityOfClassification"] = 0.0

                if "sourceName" in posts[idx]:
                    new_article["sourceName"] = posts[idx]["sourceName"]
                else:
                    new_article["sourceName"] = "Null"
                try:
                    new_article["sourceCategoryId"] = posts[idx]["sourceCategoryId"]
                    new_article["sourceLink"] = posts[idx]["sourceLink"]
                    new_article["sourceType"] = posts[idx]["sourceType"]
                    new_article["sourceAvatar"] = posts[idx]["sourceAvatar"]
                except:
                    new_article["sourceCategoryId"] = "Null"
                    new_article["sourceLink"] = "Null"
                    new_article["sourceType"] = "Null"
                    new_article["sourceAvatar"] = "Null"
                # new_article["score"] = cluster_insert["score"][cnt-1]
                new_article["index"] = count_index
                if "TopicsOnContents" in posts[idx]:
                    new_article["TopicsOnContents"] = posts[idx]["TopicsOnContents"]
                result = db.vn_newflow["articles"].insert_one(new_article)

    # getAudio(text_audio, "audio.mp3", db)
