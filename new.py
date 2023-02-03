#Connectings to Milvus, BERT and Postgresql
from pymilvus import connections
import psycopg2
connections.connect(
  alias="default", 
  host='localhost', 
  port='19530'
)


conn = psycopg2.connect(host='localhost', port='5438', user='postgres', password='postgres')

cursor = conn.cursor()

TABLE_NAME = "text_collection"
field_name = "example_field"

from pymilvus import Collection, CollectionSchema, FieldSchema, DataType
pk = FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True)
field = FieldSchema(name=field_name, dtype=DataType.FLOAT_VECTOR, dim=768)
schema = CollectionSchema(fields=[pk,field], description="example collection")

collectionn = Collection(name=TABLE_NAME, schema=schema)
# collectionn.close()
# collectionn.release()
# collectionn.drop()

#----------------------------------------------------------------------------------

# index_param = {
#         "metric_type":"L2",
#         "index_type":"IVF_SQ8",
#         "params":{"nlist":1024}
#     }

# collectionn.create_index(field_name=field_name, index_params=index_param)

#### Deleting previouslny stored table for clean run


# drop_table = "DROP TABLE IF EXISTS " + TABLE_NAME
# cursor.execute(drop_table)
# conn.commit()

# try:
#     sql = "CREATE TABLE if not exists " + TABLE_NAME + " (ids bigint, title text, text text);"
#     cursor.execute(sql)
#     conn.commit()
#     print("create postgres table successfully!")
# except Exception as e:
#     print("can't create a postgres table: ", e)
    
#----------------------------------------------------------------------------------

    
from sentence_transformers import SentenceTransformer
import pandas as pd
from sklearn.preprocessing import normalize

model = SentenceTransformer('paraphrase-mpnet-base-v2')
# # Get questions and answers.
data = pd.read_csv('data/example.csv')
title_data = data['title'].tolist()
text_data = data['text'].tolist()

sentence_embeddings = model.encode(title_data)


#----------------------------------------------------------------------------------

# sentence_embeddings = normalize(sentence_embeddings)
# print(type(sentence_embeddings))

# em =list(sentence_embeddings)
# mr = collectionn.insert([em])
# ids = mr.primary_keys
# dicts ={}

# import os 

# def record_temp_csv(fname, ids, title, text):
#     with open(fname,'w') as f:
#         for i in range(len(ids)):
#             line = str(ids[i]) + "|" + title[i] + "|" + text[i] + "\n"
#             f.write(line)

# def copy_data_to_pg(table_name, fname, conn, cur):
#     fname = os.path.join(os.getcwd(),fname)
#     try:
#         sql = "COPY " + table_name + " FROM STDIN DELIMITER '|' CSV HEADER"
#         cursor.copy_expert(sql, open(fname, "r"))
#         conn.commit()
#         print("Inserted into Postgress Sucessfully!")
#     except Exception as e:
#         print("Copy Data into Postgress failed: ", e)
        
# DATA_WITH_IDS = 'data/test.csv'   

# record_temp_csv(DATA_WITH_IDS, ids, title_data, text_data)
# copy_data_to_pg(TABLE_NAME, DATA_WITH_IDS, conn, cursor)



#----------------------------------------------------------------------------------

def new(args):
    
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}

    query_vec = []

    title = args
# docker compose -f postgres up
    query_embeddings = []
    embed = model.encode(title)
    embed = embed.reshape(1,-1)
    embed = normalize(embed)
    query_embeddings = embed.tolist()

    collectionn.load()
    results = collectionn.search(query_embeddings, field_name, param=search_params, limit=9, expr=None)

    similar_titles = []

    if results[0][0].distance < 0.5:
        print("There are no similar questions in the database, here are the closest matches:")
    else:
        print("There are similar questions in the database, here are the closest matches: ")
        
    for result in results[0]:
        sql = "select title from " + TABLE_NAME + " where ids = " + str(result.id) + ";"
        cursor.execute(sql)
        rows=cursor.fetchall()
        if len(rows):
            similar_titles.append((rows[0][0], result.distance))
            print((rows[0][0], result.distance))
        
    sql = "select text from " + TABLE_NAME + " where title = '" + similar_titles[0][0] + "';"
    cursor.execute(sql)
    rows=cursor.fetchall()
    print("Title:")
    # print(title)
    # print("Text:")
    jay = "sorry"
    # if result.distance > 0.5:
    #     return jay
    # else:
    return rows[0][0]
        
    
# print(new("Loosing the War on Terrorism"))

