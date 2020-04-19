import csv
import Feature_extraction as urlfeature
import trainer as tr
import pandas as pd

og_df=pd.read_csv('./dataset/new_dataset.csv')
y=og_df['label']

def resultwriter(feature,output_dest):
    flag=True
    columns=['']
    data=[]
    # [ ['url','features] , []]
    for i in range(0,len(feature)):
        d=feature[i][1]
        d['label']=y[i]
        data.append(d)

    for i in feature[0][1].keys():
        columns.append(i)

    try:
        with open(output_dest,'a') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=columns)
            writer.writeheader()
            writer.writerows(data)
    except IOError:
        print('IOError')


def process_URL_list(file_dest,output_dest):
    feature=[]
    with open(file_dest) as file:
        for line in file:
            url=line.split(',')[0].strip()
            malicious_bool=line.split(',')[1].strip()
            if url!='':
                # print('working on: '+url)           #showoff
                ret_dict=urlfeature.feature_extract(url)
                ret_dict['malicious']=malicious_bool
                feature.append([url,ret_dict]);
    resultwriter(feature,output_dest)

def process_test_list(file_dest,output_dest):
    feature=[]
    i=0
    with open(file_dest) as file:
        for line in file:
            url=line.strip()
            if url!='':
                i=i+1
                print('working on: ',i)           #showoff
                ret_dict=urlfeature.feature_extract(url)
                # print(ret_dict)
                feature.append([url,ret_dict])
    resultwriter(feature,output_dest)


def main():
        '''
        features = []
        urls_to_test=['https://www.twitter.com','https://www.google.com']
        for line in urls_to_test:
            url = line.strip()
            if url != '':
                print 'working on: ' + url  # showoff
                feature = urlfeature.feature_extract(url)
                features.append(feature)
        print(features) #[ ['https://www.twitter.com',{<its-feature>}] ]
        '''
        process_test_list("query.txt",'./dataset/faizan_features.csv')
        # tr.train('url_features.csv','query_features.csv')      #testing with urls in query.txt

if __name__ == '__main__':
    main()
