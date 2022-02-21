import os
import sys
import time
import logging
import traceback
import requests

# 공통 모듈 Import
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from module import upbit

# Program Name
pgm_name = 'mon_notice'
pgm_name_kr = '업비트 공지사항 크롤링'

# Headers & Page URLs
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
page_url = 'https://api-manager.upbit.com/api/v1/notices?page=1&per_page=20&thread_name=general'
query_url = 'https://upbit.com/service_center/notice?id='



# -----------------------------------------------------------------------------
# - Name : mon_notice
# - Desc : 업비트 공지사항 크롤링
# -----------------------------------------------------------------------------
def mon_notice():
    try:

        while True:  # 반복설정
            logging.info('업비트 공지사항 크롤링 중...')  #로그 하나 띄우고

            test = []

            response = requests.get(page_url, headers=headers) #추출
            upbit_notice = response.json() # json 형식으로

            for notice in upbit_notice['data']['list']:

                # 제목 & 입력일시 & 글 번호 추출
                title = notice['title'] # str 타입
                dt = notice['created_at']
                article_no = notice['id']



                tmp_notice = {'title': title, 'dt': dt, 'article_no': article_no} #합체

                # 기존 공지사항 목록 조회
                prev_notice_list = upbit.read_file(pgm_name) # pgm_name 메모장에 저장된거 리스트 형식으로 들고옴

                # 기존 공지내역이 있으면 비교하기
                if len(prev_notice_list) > 0:
                    # 기존 공지내역이 있으면 PASS
                    # and len(list(filter(lambda x: x['dt'] == dt, prev_notice_list))) > 0 \
                    #https://blog.naver.com/star7sss/222275439291 람다에 대하여
                    if len(list(filter(lambda x: x['title'] == title, prev_notice_list))) > 0 \
                            and len(list(filter(lambda x: x['article_no'] == article_no, prev_notice_list))) > 0:
                        # x는 prev_notice_list의 리스트에서 title 이 title을 만족할때
                        logging.info('기존 공지내역이 있음!')
                        logging.info(tmp_notice) # 제목 로그로 띄움

                    else:

                        logging.info('기존 공지내역이 없음! 메세지 발송!')

                        # 메세지 발송
                        msg_contents = '[' + pgm_name_kr + '] 신규 공지 등록'
                        msg_contents = msg_contents + '\n\n- 제목: ' + str(title)
                        msg_contents = msg_contents + '\n- 작성시간: ' + str(dt)
                        msg_contents = msg_contents + '\n\n- 글 확인하기: ' + str(query_url) + str(article_no)

                        title_main = title[0:4]
                        if title_main == "[거래]":
                            print(title_main)
                            test.append(title_main)


                        # 메세지 발송
                        #upbit.send_telegram_message(msg_contents)

                        # 공지내역에 추가
                        logging.info('신규 공지내역 추가!')
                        logging.info(tmp_notice)

                        # 신규 공지내역 추가
                        upbit.write_config_append(pgm_name, '\n' + str(tmp_notice))

                        # 공지 작성 후 1초 대기
                        time.sleep(1)

                # 기존 공지내역이 없으면 파일에 쓰기
                else:

                    logging.info('공지내역 최초 추가!')
                    logging.info(tmp_notice)

                    # 신규 공지내역 추가
                    upbit.write_config_append(pgm_name, tmp_notice)

                    # 공지 작성 후 1초 대기
                    time.sleep(1)

                # 5초 간격으로 조회
            time.sleep(5)

    # ---------------------------------------
    # 모든 함수의 공통 부분(Exception 처리)
    # ----------------------------------------
    except Exception:
        raise


# -----------------------------------------------------------------------------
# - Name : main
# - Desc : 메인
# -----------------------------------------------------------------------------
if __name__ == '__main__':

    # noinspection PyBroadException
    try:
        print("***** USAGE ******")
        print("[1] 로그레벨(D:DEBUG, E:ERROR, 그외:INFO)")

        if sys.platform.startswith('win32'):
            # 로그레벨(D:DEBUG, E:ERROR, 그외:INFO)
            log_level = 'I'
            upbit.set_loglevel(log_level)
        else:
            # 로그레벨(D:DEBUG, E:ERROR, 그외:INFO)
            log_level = sys.argv[1].upper()
            upbit.set_loglevel(log_level)

        if log_level == '':
            logging.error("입력값 오류!")
            sys.exit(-1)

        logging.info("***** INPUT ******")
        logging.info("[1] 로그레벨(D:DEBUG, E:ERROR, 그외:INFO):" + str(log_level))

        # ---------------------------------------------------------------------
        # Logic Start!
        # ---------------------------------------------------------------------
        mon_notice()

    except KeyboardInterrupt:
        logging.error("KeyboardInterrupt Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(-100)

    except Exception:
        logging.error("Exception 발생!")
        logging.error(traceback.format_exc())
        sys.exit(-200)