"""
기사의 키워드를 추출하는 모듈.
"""
import os
import sys
import re
import time
import math

ARTICLE_ARCHIVE_PATH = '/Users/mingeun/KeywordKatch/articles/'
FREQUENT_SPECIAL_CHARS = ['▲', '=']

################################# 자체 제작 함수 #################################

def read_article(file_path):
    '''
    전달 받은 경로의 기사를 메모리로 읽어 본문을 문자열 형태로 반환한다.
    '''
    with open(file_path, 'r', encoding='utf-8') as f:
        body = f.read()
    return body


def get_paths_to_article(press):
    '''
    해당 언론사의 모든 기사 파일 제목(절대 경로 아님)을 리스트 형태로 반환한다.
    press - 언론사 이름
    '''
    paths  = [ARTICLE_ARCHIVE_PATH + press + '/' + file \
            for file in os.listdir(ARTICLE_ARCHIVE_PATH + press) if file[0]!='.']
    return paths


def refine(content):
    '''
    의미 없는 기호(탈출문자, 구두점 등)를 제거한다.
    '''
    # 줄바꿈, 괄호 공백으로 변환
    content = re.sub('[\t\n()=.<>◇\[\]"“‘”’·○▲△▷,\']', ' ', content)           
    # 대괄호, 큰따옴표, 작은따옴표 제거
    # content = re.sub('[\[\]"“‘”’·○▲△▷,\']', '', content)       
    return content


def get_n_grams(content, n):
    '''
    전달받은 문자열의 n-gram을 배열 형태로 반환한다.
    '''
    content = refine(content)
    content = content.split(' ')
    output = []
    for i in range(len(content)-n+1):
        output.append(content[i:i+n])
    return output


def tokenize(content):
    '''
    전달받은 문자열을 이루는 단어가 원소인 리스트를 반환한다.
    '''
    tokens = refine(content)
    tokens = [word  for word in tokens.split(' ') if len(word)>0]

    return tokens


def get_presses():
    '''
    언론사 목록 획득
    '''
    result = [press for press in os.listdir(ARTICLE_ARCHIVE_PATH) if press[0] != '.']
    return result


def get_n_tokens(tokens, n):
    '''
    길이가 n인 토큰들로 이루어진 리스트를 반환한다.
    '''
    result = [token for token in tokens if len(token) == n]
    return result


def get_filtered_tf(documents, n_min, n_max):
    '''
    전체 토큰 중 길이가 start이상이고 end보다 작은 토큰들의 빈도수가 기록된 
    딕셔너리 리스트를 반환한다.
    반환된 배열은 
    [{token: f, token: f, ...}, {token: f, token: f, ...}, ...] 형태이다.
    documents - 원소가 하나의 문서에서 추출한 모든 토큰 리스트인 리스트 
    n_min - 토큰 길이 최솟값 
    n_max - 토큰 길이의 상한값 (excluded)
    '''
    result = []
    # fij 계산
    for document in documents:
        frequencies = {}
        for token in document:
            if n_min <= len(token) < n_max:
                if token not in frequencies:
                    frequencies[token] = 1
                else:
                    frequencies[token] += 1
        # 기사의 모든 토큰이 n_min보다 짧은 경우
        if len(frequencies) > 0:
            result.append(frequencies)
    return result


def is_reducable(term1, term2):
    '''
    두 단어가 적당히 비슷한지 판단한다.
    '''
    s_term = term1 if len(term1) < len(term2) else term2
    l_term = term2 if len(term1) < len(term2) else term1
    common_part_length = 0
    i = 0
    while i < len(s_term) and s_term[i] == l_term[i]:
        common_part_length += 1
        i+=1
    if common_part_length > 1 and common_part_length >= len(s_term)/3:
        return True
    else:
        return False


def get_common_str(term1, term2):
    '''
    두 단어에서 공통된 부분을 반환한다.
    '''
    s_term = term1 if len(term1) < len(term2) else term2
    l_term = term2 if len(term1) < len(term2) else term1
    common_str = ''
    i = 0
    while i < len(s_term) and s_term[i] == l_term[i]:
        common_str += s_term[i]
        i+=1
    return common_str


def reduce(term_frequencies):
    '''
    하나의 문서에서 적당히 비슷한 토큰을 하나로 합친다.
    term_frequencies - 하나의 문서에 대한 term_frequencies 딕셔너리
    {term: f, term: f, ...} 형태
    '''
    result = {}
    reduced_keys = set()
    terms = list(term_frequencies.keys())
    for i, term in enumerate(terms):
        if term not in reduced_keys:
            for other in terms[i+1:]:
                if is_reducable(term, other):
                    new_key = get_common_str(term, other)
                    if new_key in result:
                        result[new_key] += 1
                    else:
                        result[new_key] = term_frequencies[term] + term_frequencies[other]
                    reduced_keys.add(term)
                    reduced_keys.add(other)
    # 합쳐지지 않은 토큰들을 보존해야 TF.IDF에서 유효한 결과가 나온다.
    # 희귀한 단어들을 돋보이게 만든다.
    for term in terms:
        if term not in reduced_keys:
            result[term] = term_frequencies[term]
    return result

def normalize_frequency(documents):
    '''
    토큰의 빈도를 최대값으로 나눈다.
    documents - {term: freq} 딕셔너리 배열 (각 원소는 하나의 문서에 대응)
    '''
    for document in documents:
        max_freq = max(document.values())
        for term, freq in document.items():
            document[term] = freq/max_freq
    return documents


def get_idf(documents):
    '''
    모든 토큰의 IDF값을 구하여 반환한다.
    '''
    result = []
    N = len(documents)  # 문서 개수
    for document in documents:
        idf = dict()
        for term in document.keys():
            n = 0
            for doc in documents:
                if term in doc:
                    n += 1
            idf[term] = math.log2(N/n)
        result.append(idf)
    return result


def get_df(documents):
    '''
    모든 토큰의 DF값을 구하여 반환한다.
    핫 키워드를 찾는데 사용한다.
    '''
    result = []
    N = len(documents)  # 문서 개수
    for document in documents:
        df = dict()
        for term in document.keys():
            n = 0
            for doc in documents:
                if term in doc:
                    n += 1
            df[term] = 1/math.log2(N/n)
        result.append(df)
    return result


def tf_idf_score(tf, idf):
    '''
    각 토큰의 TF.IDF 점수를 반환한다.
    '''
    result = list()
    if len(tf) != len(idf):
        print('[ERROR] tf_idf_score')
        exit()
    for i in range(len(tf)):
        scores = dict()
        for term in tf[i].keys():
            scores[term] = tf[i][term] * idf[i][term]
        result.append(scores)
    return result


######################## for dev ###############################

def print_distribution(tokens):
    '''
    토큰 길이별 개수 출력   
    '''
    max_len = len(tokens[0])
    min_len = len(tokens[0])
    for token in tokens:
        token_len = len(token)
        if max_len < token_len:
            max_len = token_len
        if min_len > token_len:
            min_len = token_len
    frequencies = [0]*(max_len+1)
    total_count = len(tokens)
    for token in tokens:
        frequencies[len(token)] += 1
    for i, n in enumerate(frequencies):
        print("%2d-length token: %5d (%.2f%%)" % (i, n, (n/total_count)*100))

def print_n_tokens(tokens, n):
    '''
    길이가 n인 모든 토큰 출력
    '''
    for token in tokens:
        if len(token) == n:
            print(token)
    print()


def print_token_score(score):
    count = 0
    for t, s in score.items():
        if s>1:
            count += 1
            print("%-4s : %-5d" % (t, s))
    print(f'2번 이상 등장한 토큰의 개수: {count}')


def print_stage_info(stage):
    stage_name = 'unnamed'
    if stage == 1:
        stage_name = 'tokenize&map'
    elif stage == 2:
        stage_name = 'filter'
    elif stage == 3:
        stage_name = 'reduce'
    elif stage == 4:
        stage_name = 'normalization'
    elif stage == 5:
        stage_name = 'IDF'
    elif stage == 6:
        stage_name = 'TF*IDF'
    print('[stage%d] %15s is done.' % (stage, stage_name))


############################# main #############################
if __name__ == "__main__":
    presses = get_presses()
    documents_tokens = []
    count_article = 0
    start_time = time.time()        # [dev] 
    ''' 
    stage 1 - 모든 기사를 읽어 토큰화한다.
    documents_tokens - 각 원소가 토큰화된 기사인 리스트 
    (리스트의 크기가 기사의 개수와 일치)
    '''
    for press in presses:
        paths_to_article = get_paths_to_article(press)
        for path in paths_to_article:
            try:
                body = read_article(path)
                # 기사 파일만 있고 내용이 없는 경우 패스
                if len(body) == 0:
                    print(path)
                    continue
                documents_tokens.append(tokenize(body))
                count_article += 1
            except Exception as error:
                print(f'[{error}]: {path}')
    print_stage_info(1)
    '''
    stage 2 - filter
    크기가 3~10인 토큰만 남긴다. 
    기사의 모든 토큰이 3보다 작은 경우가 있다.
    '''
    term_freqs = get_filtered_tf(documents_tokens, 3, 11)
    print_stage_info(2)
    '''
    stage 3 - reduce
    적당히 비슷한 토큰을 합친다.
    '''
    for i, document in enumerate(term_freqs):
        term_freqs[i] = reduce(reduce(document))
        # term_freqs[i] = reduce(document)
    print_stage_info(3)
    '''
    stage 4 - normalize
    모든 토큰의 TF값 계산
    '''
    term_freqs = normalize_frequency(term_freqs)
    print_stage_info(4)
    '''
    stage 5 - IDF
    모든 토큰의 IDF 계산 
    O(T*N) N은 문서의 개수, T는 모든 토큰의 개수 
    139565 * 1178
    '''
    # inverse_doc_freqs = get_idf(term_freqs)
    # print_stage_info(5)
    '''
    stage 6 - TF*IDF 계산
    '''
    # scores = tf_idf_score(term_freqs, inverse_doc_freqs)
    # print_stage_info(6)
    end_time = time.time()          # [dev]
    # print
    total_token_count = 0
    for i, document in enumerate(term_freqs):
        print('document%4d==========='%i)
        for term, freq in document.items():
            if freq > 0.3:
                print('%-10s : %-0.3f' % (term, freq)) 
        total_token_count += len(document)
        print()
    print()
    print(f"analyzed {count_article} articles.")
    print("기사 한 개당 평균 토큰 개수: %0.1f" % (total_token_count/len(term_freqs)))
    print('전체 토큰 개수: %d' % total_token_count)
    print("elapsed time: %0.2f" % (end_time - start_time))


