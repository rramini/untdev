import RandomFloat

class Savecombine:

    def __init__(self, out_file_path, and_score_list, or_score_list, and_id_list, or_id_list):
        self.out_file_path = out_file_path
        self.and_scores = []
        self.and_urls = []
        self.or_scores = []
        self.or_urls = []
        self.score_res = []
        self.url_res = []
        self.and_score_list = and_score_list
        self.and_query_id_list = and_id_list
        self.or_score_list = or_score_list
        self.or_query_id_list = or_id_list
        self.combineScores()

    def extractAndScores(self):
        for result in self.and_score_list:
            url = list()
            score = list()
            for res in result['hits']['hits']:
                url.append(self.__prepareDocId(res['_source']['url']))
                score.append(res['_score'])
            self.and_scores.append(score)
            self.and_urls.append(url)

    def extractORScores(self):
        for result in self.or_score_list:
            url = list()
            score = list()
            for res in result['hits']['hits']:
                url.append(self.__prepareDocId(res['_source']['url']))
                score.append(res['_score'])
            self.or_scores.append(score)
            self.or_urls.append(url)


    def combineScores(self):
        self.extractAndScores()
        self.extractORScores()
        for andscore, andurl, orscore, orurl in zip(self.and_scores, self.and_urls, self.or_scores, self.or_urls):
            final_list = list()
            for ascore, aurl,  in zip(andscore, andurl):
                try:
                    index = orurl.index(aurl)
                    del orurl[index]
                    del orscore[index]
                    final_list.append(index)
                except:
                    pass
            andscore.extend(orscore)
            andurl.extend(orurl)
            self.score_res.append(andscore)
            self.url_res.append(andurl)
            print("### Output #########")
            print(len(self.and_query_id_list))
            print(len(self.score_res))
            print(len(self.url_res))
        self.savescores()

    def __prepareDocId(self, url):
        head, tail = url.split("httpsclinicaltrialsgovshow")
        return tail

    def getQueryIdList(self, query_id, count):
        query_id_list = list()
        for _ in range(count):
            query_id_list.append(query_id)
        return query_id_list

    '''
            Prepare scores document
    '''

    def savescores(self):
        ran_obj = RandomFloat.GenerateRandomFloat()
        random_numbers = ran_obj.genereate1000FloatNumbers()
        for query_id, doc_id_list, score_list in zip(self.and_query_id_list, self.url_res, self.score_res):
            query_id_list = self.getQueryIdList(query_id, len(doc_id_list))
            print(len(query_id_list))
            print(len(doc_id_list))
            print(len(score_list))
            print(len(random_numbers))
            for query_id, doc_id, score, random_number in zip(query_id_list, doc_id_list, score_list, random_numbers):
                if score > 0.0:
                    with open(self.out_file_path, "a") as outFile:
                        outFile.write(str(query_id) + "\t" + doc_id.upper() + '\t' + str(score) + '\t' + str(random_number) + "\n")

