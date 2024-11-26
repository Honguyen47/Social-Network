import facebook
import json
from datetime import datetime
from collections import defaultdict
import pandas
class FacebookCollector:
    def __init__(self, access_token):
        try:
            self.access_token = access_token
            self.graph = facebook.GraphAPI(access_token)
        except Exception as e:
            print(f'Loi khoi tao: {e}')

    def check_token_validity(self):
        try:
            me = self.graph.get_object('me', fields = 'id,name')
            print('Tonken hop le')
            return True
        except Exception:
            print('Token khong hop le')
            return False
        
    def collect_data(self, limit = 5):
        try:
            #khai bao fields
            fields = (
               'id'
               ',message'
               ',created_time'
               ',comments.limit(100).summary(true)'
               '{created_time,from{id,name},message,reactions}'
               ',reactions.limit(100).summary(true)'
               '{id,type,name}'
               ',shares'
               ',type'
           ) 
            #lay bai viet
            posts = self.graph.get_objects('me/feed', fields)
            
            for post in posts.get('data', []):
                print('--------------------')
                print(post.get('message'))
                print('---------------------')
                
           
        except Exception:
            pass
    def json_to_excel(self,json, excel_file=None):
        posts = []
        for post in my_json['data']:
            post_data = {
                'id': post.get('id'),
                'created_time' :post.get('created_time', ''),
                'message': post.get('message'),
            }
            posts.append(post_data)
        df = pd.DataFrame(post)

        df['created_time'] = pd.to_datetime(df['created_time'])

        df['created_time'] = df['created_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        if not excel_file:
            pandas.Timestamp = datetime.now().str
def main():
    ACCESS_TOKEN = 'EAAPxDQtZAzT0BO9qOigWMLUc3zbGlgTl87AsszceZBYgil38aWMi03zT7EjSJKoJQlyMtCKC3UXuZB2iILhlEEhZBdPhZBNWNZBIAgd7lWB7bjzqLviSXhaIMvmysUmoTvS8gl39N575yxVTFLcD0DqJzwq78uZC2OXNOfx8NZAjH2cdlnxbcNZBhvELoHRXUcFg8tX3HcGPnEP8d90zC3BK8b66rnhbCnlDg5chopfpgQj8Ae2aDai1selp1sLnQuVsPziri8v7ZCbAAZD'
    collector = FacebookCollector(ACCESS_TOKEN)

    if(collector.check_token_validity()):
        data =collector.collect_data(limit = 2)
        collector.to_excel(data)
if __name__ == '__main__':
    main()