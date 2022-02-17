# -----------------------------------------------------------------------------
# - Name : get_accounts
# - Desc : 잔고정보 조회
# - Input
#   1) except_yn : KRW 및 소액 제외
#   2) market_code : 마켓코드 추가(매도시 필요)
# - Output
#   1) 잔고 정보
# -----------------------------------------------------------------------------
# 계좌 조회
def get_accounts(except_yn, market_code):
    try:

        rtn_data = []

        # 소액 제외 기준
        min_price = 5000

        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
        }

        jwt_token = jwt.encode(payload, secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorize_token}

        res = send_request("GET", server_url + "/v1/accounts", "", headers)
        account_data = res.json()

        for account_data_for in account_data:

            # KRW 및 소액 제외
            if except_yn == "Y" or except_yn == "y":
                if account_data_for['currency'] != "KRW" and Decimal(str(account_data_for['avg_buy_price'])) * (
                        Decimal(str(account_data_for['balance'])) + Decimal(
                        str(account_data_for['locked']))) >= Decimal(str(min_price)):
                    rtn_data.append(
                        {'market': market_code + '-' + account_data_for['currency'],
                         'balance': account_data_for['balance'],
                         'locked': account_data_for['locked'],
                         'avg_buy_price': account_data_for['avg_buy_price'],
                         'avg_buy_price_modified': account_data_for['avg_buy_price_modified']})
            else:
                rtn_data.append(
                    {'market': market_code + '-' + account_data_for['currency'], 'balance': account_data_for['balance'],
                     'locked': account_data_for['locked'],
                     'avg_buy_price': account_data_for['avg_buy_price'],
                     'avg_buy_price_modified': account_data_for['avg_buy_price_modified']})

        return rtn_data

    # ----------------------------------------
    # Exception Raise
    # ----------------------------------------
    except Exception:
        raise