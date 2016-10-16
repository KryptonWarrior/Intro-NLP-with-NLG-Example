import pymysql, nltk, os, re, string, json
from bottle import route, run, request, response
from operator import itemgetter
from stop_words import get_stop_words
from nltk import bigrams, trigrams

# Web Services Variables
WS_HOST = '0.0.0.0'
WS_PORT = 888
WS_DEBUG = True

@route('/')
def root():    
    response.content_type = 'application/json; charset=utf-8'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.set_header('Content-Language', 'en')
    response.status = 200
    
    callback = request.query.callback
    
    returnJson = {
        "test": 0
    } 
    
    if callback:
        return callback+'("'+returnJson+'")'
    else:
        return returnJson

os.chdir('~/Desktop/')

@route('/AskIrina')
def askIrina():

    callback = request.query.callback
    text = request.query.text.encode("utf-8")
    
    conn = pymysql.connect(host='localhost', port=3306, user='askIrina', passwd='pass123', db='vaa_poc')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM datainfo")
    data = cursor.fetchall()   
    
    # create explantion list
    comments = []
    for row in data:
        comment = row[3]
        comments.append(comment)

    # create keyword list
    KeywordList = []
    for line in data:
        lineList = line[2]
        columnKeyword = lineList.split("|")
        KeywordList.append(columnKeyword)

    # removing stopwords from the text
    stops = get_stop_words('english')
    newText = ""
    newLine = []
    for w in text.split(" "):
        if w.lower() not in stops:
            newLine.append(w)
    newText = newText + " ".join(newLine)
    
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    regexText = regex.sub('', newText)
    
    # split the text into tokens
    tokens = nltk.word_tokenize(regexText)
    uni_toekns = [token.lower() for token in tokens if len(token) > 1] #same as unigrams
    bi_tokens = bigrams (tokens)
    tri_tokens = trigrams (tokens)
    
    uni_tokenList = [(item, uni_toekns.count(item)) for item in sorted(set(uni_toekns))] 
    bi_tokenList = [(item, tokens.count(item)) for item in sorted(set(bi_tokens))] 
    tri_tokenList = [(item, tokens.count(item)) for item in sorted(set(tri_tokens))]
    
    # sort frequency of tokens (Unigram)
    sortedUni_Token = sorted(uni_tokenList, key=itemgetter(1))
    sortedUni_Token.reverse()
    # sort frequency of tokens (Biogram)
    sortedBi_Token = sorted(bi_tokenList, key=itemgetter(1))
    sortedBi_Token.reverse()
    # sort frequency of tokens (Trigram)
    sortedTri_Token = sorted(tri_tokenList, key=itemgetter(1))
    sortedTri_Token.reverse()
    
    # compare tokens with keywords
    def calculatebestfit():
        tri_count = 0
        bi_count = 0
        uni_count = 0
        a = len(sortedUni_Token)
        b = len(sortedBi_Token)
        c = len(sortedTri_Token)
        count = 0
        
        if c!= 0:
            for tri in sortedTri_Token:
                for key in KeywordList:
                    tri_count = tri_count + 1
                    for trival in key:
                        if trival == ' '.join(tri[0]):
                            count = tri_count
    
        elif b!= 0:
            for bi in sortedBi_Token:
                for key in KeywordList:
                    bi_count = bi_count + 1
                    for bival in key:
                        if bival == ' '.join(bi[0]):
                            count = bi_count
             
        elif a!= 0:
            for uni in sortedUni_Token:
                for key in KeywordList:
                    uni_count = uni_count + 1
                    for unival in key:
                        if unival == uni[0]:
                            count = uni_count

        else:
            count = 8
       
        return count

    # write the output in json format 
    commentNumber = calculatebestfit()

    ans = comments[commentNumber - 1]
    answer = json.dumps(ans)

    # return link saved with the data  
    returnJson = {
        "answer": answer,
        "link": "View Page"
    }    
    
    if callback == "":
        return json.dumps(returnJson)
    else:
        return callback+"("+json.dumps(returnJson)+")"

run(host=WS_HOST, port=WS_PORT, debug=WS_DEBUG)
