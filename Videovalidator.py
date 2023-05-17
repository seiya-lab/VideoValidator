import os
import cv2
import datetime
# 取得された動画が解析に有効であるかどうかをチェックし、集計する。また、有効な動画をwebm形式からmp4形式に変換する。

def get_video_length(video_path):
    try:
        video = cv2.VideoCapture(video_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = frame_count / fps
        video.release()
        return duration
    except Exception as e:
        print("Error occurred while getting video length:", str(e))
        return None
    
# 有効な動画とは、
#   (動画のファイルサイズ)/(動画の長さ)が10KBであること、
#   動画の解像度が1280x720であること、
#   動画のファイルサイズが1MB以上であること、
#   ファイル名に(数字)が入っていないこと
# を指す。
def is_valid(video_path):
    # 動画のファイルサイズを取得
    video_size = os.path.getsize(video_path)
    # 動画の長さを取得
    video_length = get_video_length(video_path)
    # 動画の解像度を取得
    video = cv2.VideoCapture(video_path)
    width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    video.release()
    # ファイル名に(数字)が入っていないかどうかをチェック
    filename = os.path.basename(video_path)
    if filename.find("(") != -1 and filename.find(")") != -1:
        return False
    # 動画のファイルサイズが1MB以上であるかどうかをチェック
    if video_size < 1000000:
        return False
    # 動画の長さが0であるかどうかをチェック
    if video_length == 0:
        return False
    # 動画の解像度が1280x720であるかどうかをチェック
    if width != 1280 or height != 720:
        return False
    # 動画のファイルサイズが動画の長さの10000倍以上であるかどうかをチェック
    if video_size > video_length * 10000:
        return False
    return True
    
# webm動画をmp4動画に変換する関数
# 元動画のpathは、../data/ユーザID/動画ID.webmとすると
# 変換後の動画のpathは、../processed_data/ユーザID/動画ID.mp4となる。
def convert_webm_to_mp4(video_path):
    try:
        # 動画のpathを取得
        video_dir = os.path.dirname(video_path)
        video_id = os.path.basename(video_path).split(".")[:-1]
        # 動画のpathを設定
        output_dir = video_dir.replace("data", "processed_data")
        mp4_video_path = os.path.join(output_dir, video_id + ".mp4")
        # 動画をwebmからmp4に変換
        os.system("ffmpeg -i " + video_path + " -vcodec h264 -c:v copy" + mp4_video_path)
        return True
    except Exception as e:
        print("Error occurred while converting webm to mp4:", str(e))
        return False
    
# すでにmp4動画に変換されているかどうかをチェックする関数
def is_converted(video_path):
    # 動画のpathを取得
    video_dir = os.path.dirname(video_path)
    video_id = os.path.basename(video_path).split(".")[:-1]
    # 動画のpathを設定
    output_dir = video_dir.replace("data", "processed_data")
    mp4_video_path = os.path.join(output_dir, video_id + ".mp4")
    # mp4動画が存在するかどうかをチェック
    if os.path.exists(mp4_video_path):
        return True
    else:
        return False
    
# video_pathから日付を取得する関数
def get_date(video_path):
    # 動画ファイル名の中に、標準時の時間が含まれているので、日本時間に変換し取得する。
    # 例えばrec__s__8d8621b1-c250-4c13-8647-7cfcdf5f09b2__2023-04-14T05_26_23.644Z.webm→04/14
    filename = os.path.basename(video_path)
    # 標準時の時間を取得する
    utc_time = filename.split("__")[-1].split(".")[0].replace("T", " ").replace("_", ":")
    # 日本時間の日付に変換、jst_dateに日付のみ格納する
    jst_date = datetime.datetime.strptime(utc_time, "%Y-%m-%d %H:%M:%S.%f").astimezone(datetime.timezone(datetime.timedelta(hours=9))).strftime("%m/%d")
    return jst_date
    
    
    
if __name__ == "__main__":
    # データのパスを設定
    data_dir = "../data"
    # データのパスを取得
    user_dirs = os.listdir(data_dir)
    print(user_dirs)
    
    # ユーザごとに、有効だった動画をmp4に変換し、その日付ごとに動画の総合計時間を計算し、出力する。
    for user_dir in user_dirs:
        # ビデオのパスを取得
        video_paths = os.listdir(os.path.join(data_dir, user_dir))
        # 有効な動画のpathを格納するリスト
        valid_video_paths = []
        # 有効な動画のpathを取得
        for video_path in video_paths:
            # 動画のpathを設定
            video_path = os.path.join(data_dir, user_dir, video_path)
            # 動画が有効であるかどうかをチェック
            if is_valid(video_path):
                # 動画が有効であれば、mp4に変換
                if not is_converted(video_path):
                    convert_webm_to_mp4(video_path)
                # 有効な動画のpathをリストに追加
                valid_video_paths.append(video_path)
                
        # 有効な動画の総合計時間を計算し、出力する。
        # 日付ごとに動画の総合計時間を計算するため、日付ごとに動画のpathを格納するリストを作成する。
        date_video_paths = {}
        for video_path in valid_video_paths:
            # 動画の日付を取得
            date = get_date(video_path)
            # 日付ごとに動画のpathを格納するリストを作成
            if date not in date_video_paths:
                date_video_paths[date] = []
            # 日付ごとに動画のpathを格納
            date_video_paths[date].append(video_path)
        # 日付ごとに動画の総合計時間を計算し、出力する。
        for date in date_video_paths:
            # 日付ごとに動画の総合計時間を計算
            total_time = 0
            for video_path in date_video_paths[date]:
                total_time += get_video_length(video_path)
            # 日付ごとに動画の総合計時間を出力
            print(user_dir, date, total_time)
        