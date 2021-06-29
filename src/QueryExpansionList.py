import pandas as pd

class ExapndedQuery:
    def __init__(self, query_path):
        self.query_path = query_path

    def readfile(self):
        expansion_dataframe = pd.read_csv(self.query_path)
        return expansion_dataframe

    def getTopicIDList(self):
        expansion_dataframe = self.readfile()
        topic_id_list = expansion_dataframe['TopicID']
        return topic_id_list

    def getTopicIDList1(self, df):
        topic_id_list = df['group_topic_id']
        return topic_id_list

    def groupByTopicId(self):
        topic_id_list = list()
        topic_list = self.getTopicIDList()
        for topic in topic_list:
            if "gene" in topic:
                topic_id = topic.split("gene")
                topic_id = str(topic_id[0]).split('T')
                topic_id_list.append(int(topic_id[1]) + 1)
            elif "disease" in topic:
                topic_id = topic.split("disease")
                topic_id = str(topic_id[0]).split('T')
                topic_id_list.append(int(topic_id[1]) + 1)
        return topic_id_list

    def removeDuplicates(self):
        topicIdList = self.groupByTopicId()
        unique_Id_list = list(set(topicIdList))
        return unique_Id_list

    def addColoumnToDataFrame(self):
        expansion_dataFrame = self.readfile()
        topic_id_list = self.groupByTopicId()
        print(topic_id_list)
        expansion_dataFrame["group_topic_id"] = topic_id_list
        print(expansion_dataFrame)
        return expansion_dataFrame

    def getGroupedData(self):
        df = self.addColoumnToDataFrame()
        df['query_concept'] = df["query_concept"].astype(str)
        df['new_extended'] = df['new_extended'].astype(str)
        df['combined'] = df[['query_concept', 'new_extended']].agg('#'.join, axis=1)
        df['Topics'] = df['group_topic_id']
        df = df.groupby(['group_topic_id']).agg(lambda x: x.tolist())
        combined = df['combined'].tolist()
        topic_id_lsit = df['Topics'].tolist()
        topics = self.getTopicIdList(topic_id_lsit)
        return combined, topics

    def getTopicIdList(self, topic_id_lsit):
        topics = list()
        for topic_list in topic_id_lsit:
            topics.append(str(topic_list[0]))
        return topics