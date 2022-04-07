from datetime import datetime, timedelta, timezone

TZ_UTC = timezone.utc
TZ_KST = timezone(timedelta(hours=9))

DATE_LENGTH = len("0000-00-00") # 10
DATETIME_LENGTH = len("0000-00-00 00:00:00") # 19

if __name__ == "__main__":

    # timezone 정보가 없는 datetime 객체의 timezone은 시스템 시간대로 간주된다
    tz_unaware_now = datetime.now()

    # timezone 정보를 GMT+0으로 설정한 datetime 객체
    utc_now = tz_unaware_now.astimezone(TZ_UTC) # 또는 datetime.now(TZ_UTC)


    """
    GET API 요청 시, DB의 KST date를 UTC datetime으로 변환하는 방법
    """

    db_date_kst = "2022-04-07"
    tz_aware_midnight_kst = datetime.fromisoformat(f"{db_date_kst} 00:00:00+09:00")
    api_datetime_utc = tz_aware_midnight_kst.astimezone(TZ_UTC)
    result_string = str(api_datetime_utc)[:DATETIME_LENGTH]
    print(f"{db_date_kst} -> {result_string}")

    """
    POST/PATCH API 요청 시, 클라이언트의 UTC datetime을 KST date로 변환하는 방법
    """

    client_datetime_utc = "2022-04-06 15:00:00"

    # 저장해야하는 날짜의 기준 timezone이 UTC면, 여기서 멈추고 그냥 client_datetime_utc 를 쓰면 된다

    tz_aware_datetime_utc = datetime.fromisoformat(f"{client_datetime_utc}+00:00")
    tz_aware_datetime_kst = tz_aware_datetime_utc.astimezone(TZ_KST)
    result_string = str(tz_aware_datetime_kst)[:DATE_LENGTH]
    print(f"{client_datetime_utc} -> {result_string}")
