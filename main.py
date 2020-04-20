import csv
import Feature_extraction as urlfeature
import trainer as tr
import pandas as pd

og_df=pd.read_csv('./dataset/new_dataset.csv')
y=og_df['label']

def resultwriter(feature,output_dest):
    columns=[
        'URL','rank_host','rank_country','host','path','Length_of_url',
        'Length_of_host','No_of_dots','avg_token_length','token_count',
        'largest_token','avg_domain_token_length','domain_token_count',
        'largest_domain','avg_path_token','path_token_count','largest_path',
        'sec_sen_word_cnt','IPaddress_presence','ASNno','label'
    
        ]
    start=61940


    try:
        with open(output_dest,'a') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=columns)
            # writer.writeheader()
            feature['label']=y[start]
            writer.writerow(feature)
            start+=1
    except IOError:
        print('IOError')




def process_test_list(file_dest,output_dest):
    # feature=[]
    i=0
    with open(file_dest) as file:
        for line in file:
            url=line.strip()
            if url!='':
                i=i+1
                print('working on: ',i)
                url='https://www.'+url       #showoff
                ret_dict=urlfeature.feature_extract(url)
                # print(ret_dict)
                # feature.append([url,ret_dict])
                resultwriter(ret_dict,output_dest)


def main():
    process_test_list("query.txt",'./dataset/faizan_features.csv')

if __name__ == '__main__':
    main()
