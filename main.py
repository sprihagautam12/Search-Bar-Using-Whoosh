import pandas as pd
data=pd.read_csv(r"Books.csv",encoding = "Latin-1")
data.drop(data.columns[[2,3,4,5,6,7,8,9,10,11]],axis=1,inplace=True)
print(data)
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis import StemmingAnalyzer
from whoosh.lang.morph_en import variations
from whoosh.analysis import RegexTokenizer
from whoosh.analysis import LowercaseFilter
from whoosh.analysis import StopFilter
my_analyzer = RegexTokenizer() | LowercaseFilter() | StopFilter()
schema = Schema( id = ID(stored=True), name =TEXT(stored=True,analyzer=my_analyzer))
import os.path
from whoosh import index
from whoosh.index import create_in

#creating and populating index

if not os.path.exists("index"):
    os.mkdir("index")
ix = create_in("index", schema)
writer=ix.writer()
papers=[data]
for paper_set in papers:
    for index, row in paper_set.iterrows():
        writer.add_document(id = row['id'],
                            name = row['name'])
writer.commit()
from whoosh.qparser import QueryParser
from whoosh.query import *
from whoosh.qparser import QueryParser
from whoosh.lang.morph_en import variations
from whoosh import qparser, query
#creating index searcher
def index_search(search_query):
    with ix.searcher() as s:
        og = qparser.OrGroup.factory(0.9)
        qp = qparser.QueryParser("name", schema=ix.schema, termclass=query.Variations, group=og)
        qp.add_plugin(qparser.FuzzyTermPlugin())
        qp.add_plugin(qparser.SequencePlugin())
        q = qp.parse(search_query)

        results = s.search(q, limit=None)
        print(q)
        print(len(results))
        list=[]
        for res in results:
            list.append(res['name'])
            list.append(res['id'])
        return list


val=input("Enter the word you wish to search")

b=index_search(val +'~')
print (b)