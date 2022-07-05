##Go through smarthome.community, get all posts and save in file.

import re
import requests

import pandas as pd

def reduce_text(text: str) -> str:
    """Remove HTML tags, unncessary whitespaces and newlines from text.

    Parameters
    ----------
    text : str
        The text to strip.

    Returns
    -------
    str
        The stripped text.
    """
    # Get rid of HTML tags
    text = re.sub(r"<.*?>", "", text)
    # Get rid of newline characters
    text = text.replace("\n", " ")
    # Collapse multiple spaces into one
    return re.sub(f"\s+", " ", text)


def write_topics_to_file(file_path: str, num_topics: int) -> None:
    """Go through smarthome.community and write posts to JSON-file.

    Parameters
    ----------
    file_path : str
        The file_path of the file to save to (JSON).
    num_topics : int
        The amount of topics to search for.
    """
    num_found_topics = 0
    num_found_posts = 0

    result = {}
    for i in range(num_topics):
        url = f"https://smarthome.community/api/topic/{i}"
        response = requests.get(url)
        if response.status_code >= 300:
            # Probably unauthorized or not a topic
            print(f"Topic {i} failed: {response.status_code}")
            continue
        num_found_topics += 1
        response_content = response.json()

        # Get posts and write to file
        posts = []
        for post in response_content["posts"]:
                    num_found_posts += 1
                    postID = post["pid"]
                    topicID = post["tid"]
                    posttimestamp = post["timestampISO"]
                    postUID = post["uid"]
                    postdeleted = post["deleted"]
                    postupvotes = post["upvotes"]
                    postdownvotes = post["downvotes"]
                    edited = post["edited"]
                    bookmarks = post["bookmarks"]
                    votes = post["votes"]
                    index = post["index"]
                    text = reduce_text(post["content"])

                    username = post["user"]["username"]
                    postuserID = post["user"]["uid"]
                    reputation = post["user"]["reputation"]
                    userpostcount = post["user"]["postcount"]
                    usertopiccount = post["user"]["topiccount"]
                    banned = post["user"]["banned"]
                    bannedExpire = post["user"]["banned:expire"]
                    status = post["user"]["status"]
                    lastonline = post["user"]["lastonlineISO"]
                    group = post["user"]["groupTitleArray"]
                    bannedUntil = post["user"]["banned_until_readable"]
                    selectedGroups = post["user"]["selectedGroups"]
                    profileInfo = post["user"]["custom_profile_info"]

                    replyshasMore = post["replies"]["hasMore"]
                    replyuser = post["replies"]["users"]
                    replytext = reduce_text(post["replies"]["text"])
                    replycount = post["replies"]["count"]

                    posts.append(
                        {
                            "text": text,
                            "postID": postID,
                            "toopicID": topicID,
                            "posttimestamp": posttimestamp,
                            "postUID": postUID,
                            "postdeleted": postdeleted,
                            "postupvotes": postupvotes,
                            "postdownvotes": postdownvotes,
                            "edited": edited,
                            "bookmarks": bookmarks,
                            "votes": votes,
                            "index": index,

                            "username": username,
                            "postuserID": postuserID,
                            "reputation": reputation,
                            "userpostcount": userpostcount,
                            "usertopiccount": usertopiccount,
                            "banned": banned, 
                            "bannedExpire": bannedExpire,
                            "status": status,
                            "lastonline": lastonline,
                            "group": group,
                            "bannedUntil": bannedUntil, 
                            "selectedGroups": selectedGroups,
                            "profileInfo": profileInfo,

                            "replyshasMore": replyshasMore,
                            "replyuser": replyuser,
                            "replytext": replytext,
                            "replycount": replycount

                        }
                    )

        # Get remaining posts
        if response_content["postcount"] > 20:
            cnt = 30
            while cnt <= response_content["postcount"]:
                url = f"https://smarthome.community/api/topic/{response_content['slug']}/{cnt}"
                response_content = requests.get(url).json()
                for post in response_content["posts"]:
                    num_found_posts += 1
                    postID = post["pid"]
                    topicID = post["tid"]
                    posttimestamp = post["timestampISO"]
                    postUID = post["uid"]
                    postdeleted = post["deleted"]
                    postupvotes = post["upvotes"]
                    postdownvotes = post["downvotes"]
                    edited = post["edited"]
                    bookmarks = post["bookmarks"]
                    votes = post["votes"]
                    index = post["index"]
                    text = reduce_text(post["content"])

                    username = post["user"]["username"]
                    postuserID = post["user"]["uid"]
                    reputation = post["user"]["reputation"]
                    userpostcount = post["user"]["postcount"]
                    usertopiccount = post["user"]["topiccount"]
                    banned = post["user"]["banned"]
                    bannedExpire = post["user"]["banned:expire"]
                    status = post["user"]["status"]
                    lastonline = post["user"]["lastonlineISO"]
                    group = post["user"]["groupTitleArray"]
                    bannedUntil = post["user"]["banned_until_readable"]
                    selectedGroups = post["user"]["selectedGroups"]
                    profileInfo = post["user"]["custom_profile_info"]

                    replyshasMore = post["replies"]["hasMore"]
                    replyuser = post["replies"]["users"]
                    replytext = reduce_text(post["replies"]["text"])
                    replycount = post["replies"]["count"]

                    posts.append(
                        {
                            "text": text,
                            "postID": postID,
                            "toopicID": topicID,
                            "posttimestamp": posttimestamp,
                            "postUID": postUID,
                            "postdeleted": postdeleted,
                            "postupvotes": postupvotes,
                            "postdownvotes": postdownvotes,
                            "edited": edited,
                            "bookmarks": bookmarks,
                            "votes": votes,
                            "index": index,

                            "username": username,
                            "postuserID": postuserID,
                            "reputation": reputation,
                            "userpostcount": userpostcount,
                            "usertopiccount": usertopiccount,
                            "banned": banned, 
                            "bannedExpire": bannedExpire,
                            "status": status,
                            "lastonline": lastonline,
                            "group": group,
                            "bannedUntil": bannedUntil, 
                            "selectedGroups": selectedGroups,
                            "profileInfo": profileInfo,

                            "replyshasMore": replyshasMore,
                            "replyuser": replyuser,
                            "replytext": replytext,
                            "replycount": replycount

                        }
                    )
                cnt += 20            
                
            if len(posts) < response_content["postcount"]:
                url = f"https://smarthome.community/api/topic/{response_content['slug']}/{cnt - 9}"
                response_content = requests.get(url).json()
                for post in response_content["posts"][9:]:
                    num_found_posts += 1
                    postID = post["pid"]
                    topicID = post["tid"]
                    posttimestamp = post["timestampISO"]
                    postUID = post["uid"]
                    postdeleted = post["deleted"]
                    postupvotes = post["upvotes"]
                    postdownvotes = post["downvotes"]
                    edited = post["edited"]
                    bookmarks = post["bookmarks"]
                    votes = post["votes"]
                    index = post["index"]
                    text = reduce_text(post["content"])

                    username = post["user"]["username"]
                    postuserID = post["user"]["uid"]
                    reputation = post["user"]["reputation"]
                    userpostcount = post["user"]["postcount"]
                    usertopiccount = post["user"]["topiccount"]
                    banned = post["user"]["banned"]
                    bannedExpire = post["user"]["banned:expire"]
                    status = post["user"]["status"]
                    lastonline = post["user"]["lastonlineISO"]
                    group = post["user"]["groupTitleArray"]
                    bannedUntil = post["user"]["banned_until_readable"]
                    selectedGroups = post["user"]["selectedGroups"]
                    profileInfo = post["user"]["custom_profile_info"]

                    replyshasMore = post["replies"]["hasMore"]
                    replyuser = post["replies"]["users"]
                    replytext = reduce_text(post["replies"]["text"])
                    replycount = post["replies"]["count"]

                    posts.append(
                        {
                            "text": text,
                            "postID": postID,
                            "toopicID": topicID,
                            "posttimestamp": posttimestamp,
                            "postUID": postUID,
                            "postdeleted": postdeleted,
                            "postupvotes": postupvotes,
                            "postdownvotes": postdownvotes,
                            "edited": edited,
                            "bookmarks": bookmarks,
                            "votes": votes,
                            "index": index,

                            "username": username,
                            "postuserID": postuserID,
                            "reputation": reputation,
                            "userpostcount": userpostcount,
                            "usertopiccount": usertopiccount,
                            "banned": banned, 
                            "bannedExpire": bannedExpire,
                            "status": status,
                            "lastonline": lastonline,
                            "group": group,
                            "bannedUntil": bannedUntil, 
                            "selectedGroups": selectedGroups,
                            "profileInfo": profileInfo,

                            "replyshasMore": replyshasMore,
                            "replyuser": replyuser,
                            "replytext": replytext,
                            "replycount": replycount

                        }
                    )


        result[f"topic_{i}"] = {
            "question": response_content["isQuestion"] if response_content.get("isQuestion") else "NA",
            "solved": response_content["isSolved"] if response_content.get("isSolved") else "NA",
            "chapterID": response_content["cid"],
            "lasttime": response_content["lastposttimeISO"],
            "mainPid": response_content["mainPID"] if response_content.get("mainPID") else "NA",
            "postcount": response_content["postcount"],
            "topicID": response_content["tid"],
            "createdat": response_content["timestampISO"],
            "topicname": response_content["titleRaw"],
            "creatorID":response_content["uid"],
            "views": response_content["viewcount"],
            "posters": response_content["postercount"],
            "teaserPid": response_content["teaserPID"] if response_content.get("teaserPID") else "NA",
            "downvotes": response_content["downvotes"],
            "upvotes": response_content["upvotes"],
            "deleted": response_content["deleted"],
            "locked": response_content["locked"],
            "pinned": response_content["pinned"],
            "pinExpiry": response_content["pinExpiry"],
            "topic_votes": response_content["votes"],
            "posts": posts
        }

    result_list = []
    for topic in result.values():
        posts = topic["posts"]
        topic.pop("posts")
        for post in posts:
            result_list.append(topic | post)

    result_dict = {}
    for cat in result_list[0]:
        result_dict[cat] = []

    for post in result_list:
        for key in post:
            result_dict[key].append(post[key])

    
    df = pd.DataFrame(result_dict)
    df.to_csv(file_path)

    print(f"Number of topics found: {num_found_topics}")
    print(f"Number of posts found: {num_found_posts}")
#    with open(file_path, "w") as f:
#        json.dump(result_dict, f)

#store the data in a csv file
if __name__ == "__main__":
    file_path = "automation_posts_12_06.csv"
    write_topics_to_file(file_path, 1000)


