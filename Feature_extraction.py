from urllib.parse import urlparse
import re
import urllib.request as urllib2
import urllib
from xml.dom import minidom
import csv
import pygeoip
import sys
import requests
from pysafebrowsing import SafeBrowsing
import ipinfo
import socket
access_token="8ede24305bd35d" #ipinfo access token


opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

nf=-1

def Tokenise(url):

        if url=='':
            return [0,0,0]
        token_word=re.split('\W+',url)
        no_ele=sum_len=largest=0
        for ele in token_word:
                l=len(ele)
                sum_len+=l
                if l>0:                                        ## for empty element exclusion in average length
                        no_ele+=1
                if largest<l:
                        largest=l
        try:
            return [float(sum_len)/no_ele,no_ele,largest]
        except:
            return [0,no_ele,largest]


def find_ele_with_attribute(dom,ele,attribute):
    for subelement in dom.getElementsByTagName(ele):
        if subelement.hasAttribute(attribute):
            return subelement.attributes[attribute].value
    return nf


def sitepopularity(host):

        xmlpath='http://data.alexa.com/data?cli=10&dat=snbamz&url='+host
        # print(xmlpath)
        try:
            xml= urllib2.urlopen(xmlpath)
            dom =minidom.parse(xml)
            rank_host=find_ele_with_attribute(dom,'REACH','RANK')
            country=find_ele_with_attribute(dom,'REACH','RANK')
            # print('Country ',country)
            rank_country=find_ele_with_attribute(dom,'COUNTRY','RANK')
            return [rank_host,rank_country]

        except:
            return [nf,nf]


def Security_sensitive(tokens_words):

    sec_sen_words=['confirm', 'account', 'banking', 'secure', 'ebayisapi', 'webscr', 'login', 'signin']
    cnt=0
    for ele in sec_sen_words:
        if(ele in tokens_words):
            cnt+=1;

    return cnt

def exe_in_url(url):
    if url.find('.exe')!=-1:
        return 1
    return 0

def Check_IPaddress(tokens_words):

    cnt=0;
    for ele in tokens_words:
        if str(ele).isnumeric():
            cnt+=1
        else:
            if cnt>=4 :
                return 1
            else:
                cnt=0;
    if cnt>=4:
        return 1
    return 0

# Implemented from scratch by ME
#https://www.ipinfo.io
def getASN(host):
    print(host)
    handler = ipinfo.getHandler(access_token)
    host_ip=''
    try:
        host_ip = socket.gethostbyname(host)
        x = requests.get('https://ipinfo.io/' + host_ip + '/json?token=' + access_token)
        ans=x.json()
        return ans['asn']['asn']
    except:
        print('Cannot get ASN Number for host: ',host)
        host_ip=''
        return 0


def web_content_features(url):
    wfeatures={}
    total_cnt=0
    try:
        source_code = urllib.request.url_open(url)
        print(requests.url_read)

        wfeatures['src_html_cnt']=source_code.count('<html')
        wfeatures['src_hlink_cnt']=source_code.count('<a href=')
        wfeatures['src_iframe_cnt']=source_code.count('<iframe')
        #suspicioussrc_ javascript functions count

        wfeatures['src_eval_cnt']=source_code.count('eval(')
        wfeatures['src_escape_cnt']=source_code.count('escape(')
        wfeatures['src_link_cnt']=source_code.count('link(')
        wfeatures['src_underescape_cnt']=source_code.count('underescape(')
        wfeatures['src_exec_cnt']=source_code.count('exec(')
        wfeatures['src_search_cnt']=source_code.count('search(')

        for key in wfeatures:
            if(key!='src_html_cnt' and key!='src_hlink_cnt' and key!='src_iframe_cnt'):
                total_cnt+=wfeatures[key]
        wfeatures['src_total_jfun_cnt']=total_cnt

    except Exception as e:
        print("Error"+str(e)+" in downloading page "+url)
        default_val=nf

        wfeatures['src_html_cnt']=default_val
        wfeatures['src_hlink_cnt']=default_val
        wfeatures['src_iframe_cnt']=default_val
        wfeatures['src_eval_cnt']=default_val
        wfeatures['src_escape_cnt']=default_val
        wfeatures['src_link_cnt']=default_val
        wfeatures['src_underescape_cnt']=default_val
        wfeatures['src_exec_cnt']=default_val
        wfeatures['src_search_cnt']=default_val
        wfeatures['src_total_jfun_cnt']=default_val

    return wfeatures


# Implemented from scratch by ME
# https://pypi.org/project/pysafebrowsing/
def safebrowsing(url):
    api_key='AIzaSyDVDkoDJ05srO3OdyZsV1R3UkGa6DB3Bz0'
    s = SafeBrowsing(api_key)
    try:
        r = s.lookup_urls([url])
        return r[url]['malicious']
    except Exception as e:
        print(e)
        return True

# Main Method
def feature_extract(url_input):

        Feature={}
        tokens_words=re.split('\W+',url_input)       #Extract bag of words stings delimited by (.,/,?,,=,-,_)
        #token_delimit1=re.split('[./?=-_]',url_input)
        #print token_delimit1,len(token_delimit1)

        obj=urlparse(url_input)
        print(obj)
        host=obj.netloc
        path=obj.path

        Feature['URL']=url_input

        Feature['rank_host'],Feature['rank_country'] =sitepopularity(host)

        Feature['host']=obj.netloc
        Feature['path']=obj.path

        Feature['Length_of_url']=len(url_input)
        Feature['Length_of_host']=len(host)
        Feature['No_of_dots']=url_input.count('.')

        Feature['avg_token_length'],Feature['token_count'],Feature['largest_token'] = Tokenise(url_input)
        Feature['avg_domain_token_length'],Feature['domain_token_count'],Feature['largest_domain'] = Tokenise(host)
        Feature['avg_path_token'],Feature['path_token_count'],Feature['largest_path'] = Tokenise(path)

        Feature['sec_sen_word_cnt'] = Security_sensitive(tokens_words)
        Feature['IPaddress_presence'] = Check_IPaddress(tokens_words)

        # print host
        # print getASN(host)
        # Feature['exe_in_url']=exe_in_url(url_input)
        Feature['ASNno']=getASN(host)
        # Feature['safebrowsing']=not safebrowsing(url_input)
        '''
        wfeatures=web_content_features(url_input)

        for key in wfeatures:
            Feature[key]=wfeatures[key]

        #debug
        # for key in Feature:
        #     print key +':'+str(Feature[key])
        '''
        return Feature

if __name__=="__main__":
    url=sys.argv[1]
    x=feature_extract(url)
    print(x)
