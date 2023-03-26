"""
기사의 키워드를 추출하는 모듈.
"""
import os
import sys
import re
import time

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
    content = re.sub('[\n()=]', ' ', content)           # 줄바꿈, 괄호 공백으로 변환
    content = re.sub('[\[\]"“‘”’▲,.\']', '', content)       # 대괄호, 큰따옴표, 작은따옴표 제거
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
    content = refine(content)
    content = [word  for word in content.split(' ') if len(word)>0]

    return content


def get_presses():
    '''
    언론사 목록 획득
    '''
    result = [press for press in os.listdir(ARTICLE_ARCHIVE_PATH) if press[0] != '.']
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

############################# main #############################
if __name__ == "__main__":
    presses = get_presses()
    tokens = []
    count_article = 0
    start_time = time.time()        # [dev] 
    for press in presses:
        paths_to_article = get_paths_to_article(press)
        for path in paths_to_article:
            try:
                body = read_article(path)
                tokens += tokenize(body)
                count_article += 1
            except Exception as error:
                print(f'[{error}]: {path}')
    end_time = time.time()          # [dev]
    # print
    print_n_tokens(tokens, 3)
    print(f"total token: {len(tokens)}")
    print("elapsed time: %0.2f" % (end_time - start_time))
    print(f"analyze {count_article} articles.")


