import csv
import Feature_extraction as urlfeature
import trainer as tr

def resultwriter(feature,output_dest):
    flag=True
    with open(output_dest,'wb') as f:
        for item in feature:
            w = csv.DictWriter(f, item[1].keys())
            if flag:
                w.writeheader()
                flag=False
            w.writerow(item[1])

def process_URL_list(file_dest,output_dest):
    feature=[]
    with open(file_dest) as file:
        for line in file:
            url=line.split(',')[0].strip()
            malicious_bool=line.split(',')[1].strip()
            if url!='':
                print('working on: '+url)           #showoff
                ret_dict=urlfeature.feature_extract(url)
                ret_dict['malicious']=malicious_bool
                feature.append([url,ret_dict]);
    resultwriter(feature,output_dest)

def process_test_list(file_dest,output_dest):
    feature=[]
    with open(file_dest) as file:
        for line in file:
            url=line.strip()
            if url!='':
                print('working on: '+url)           #showoff
                ret_dict=urlfeature.feature_extract(url)
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
        process_test_list("query.txt",'query_features.csv')
        tr.train('url_features.csv','query_features.csv')      #testing with urls in query.txt

if __name__ == '__main__':
    main()
