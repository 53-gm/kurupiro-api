import requests
import zipfile
import io
import pandas as pd
import shutil
import datetime

URL = "https://ajt-mobusta-gtfs.mcapps.jp/static/8/current_data.zip"
DATA_DIR = "./data/gtfs-static"


# GTFS staticファイルのダウンロード
def dl_gtfs_static_files():
    shutil.rmtree(DATA_DIR)  # 前のファイルが残って居た場合に消去する

    with (
        requests.get(URL) as res,
        io.BytesIO(res.content) as bytes_io,
        zipfile.ZipFile(bytes_io) as zip,
    ):
        zip.extractall(DATA_DIR)


# GTFS staticのデータを整形して一つのファイルにする関数
# gtfs-static.csv
def generate_gtfs_data():

    # 必要なtxtファイルをGTFS staticから読み込み
    stop_times = pd.read_csv(DATA_DIR + "/stop_times.txt")
    trips = pd.read_csv(DATA_DIR + "/trips.txt")
    calendar = pd.read_csv(DATA_DIR + "/calendar.txt")
    routes = pd.read_csv(DATA_DIR + "/routes.txt")
    stops = pd.read_csv(DATA_DIR + "/stops.txt")
    stops_direction = pd.read_csv(DATA_DIR + "/stops_direction.txt")
    routes_jp = pd.read_csv(DATA_DIR + "/routes_jp.txt")

    # データ整形
    df = pd.merge(stop_times, trips, on="trip_id")
    df2 = pd.merge(df, calendar, on="service_id")
    df3 = pd.merge(df2, routes, on="route_id")
    df4 = pd.merge(df3, stops, on="stop_id")
    df5 = pd.merge(df4, stops_direction, on="stop_id")
    df6 = pd.merge(df5, routes_jp, on="route_id")

    # 保存
    df_result = df6[
        [
            "stop_id",
            "stop_name",
            "arrival_time",
            "stop_headsign",
            "trip_headsign",
            "route_long_name",
            "jp_parent_route_id",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]
    ]
    df_result.to_csv(DATA_DIR + "/gtfs-static.csv")

    return


weekday_dic = {
    0: "monday",
    1: "tuesday",
    2: "wednesday",
    3: "thursday",
    4: "friday",
    5: "saturday",
    6: "sunday",
}


# 今日来るバスの時刻表を取得 (引数: 停留所)
def today_bus_times(stop_name: str):
    now_time = datetime.datetime.now() + datetime.timedelta(hours=9)
    now_date = now_time.strftime("%Y-%m-%d")
    now_weekday = weekday_dic[now_time.weekday()]

    df_gtfs = pd.read_csv(DATA_DIR + "/gtfs-static.csv")

    df_stop = df_gtfs[(df_gtfs["stop_name"] == stop_name) & (df_gtfs[now_weekday] == 1)]
    df_stop["arrival_time"] = df_stop["arrival_time"].apply(
        lambda x: datetime.datetime.strptime((now_date + " " + x), "%Y-%m-%d %H:%M:%S")
    )

    df_stop_and_time = df_stop[df_stop["arrival_time"] > now_time].sort_values(
        "arrival_time"
    )

    print(df_stop_and_time)

    return df_stop_and_time


def main():
    # generate_gtfs_data()
    # today_bus_times("市立大学前")
    print("success")


if __name__ == "__main__":
    main()
