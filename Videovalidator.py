import os
import cv2
import datetime
# 取得された動画が解析に有効であるかどうかをチェックし、集計する。また、有効な動画をwebm形式からmp4形式に変換する。
# 明らかに再生時間に対して容量が小さすぎる動画は、解析に有効でないと判断し、あとで除外する。

DATA_DIR = "../../data"
PROCESSED_DATA_DIR = "../../processed_data"
RESOLUTION_WIDTH = 1280
RESOLUTION_HEIGHT = 720
MIN_FILE_SIZE = 1000000  # 1MB
MAX_FILE_SIZE_FACTOR = 10000

def get_video_length(video_path):
    try:
        video = cv2.VideoCapture(video_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = frame_count / fps
        video.release()
        return duration
    except Exception as e:
        print("Failed to get video length:", video_path)
        print("Error occurred while getting video length:", str(e))
        return None

# 動画ファイルかどうかをチェックする関数
# webm形式の動画ファイルは、拡張子がwebmであることで判定できる。
def is_video(video_path):
    return video_path.endswith(".webm")
    
# 有効な動画とは、
#   動画ファイルであること
#   動画の解像度が1280x720であること、
#   動画のファイルサイズが1MB以上であること、
#   ファイル名に(数字)が入っていないこと
# を指す。 
def is_valid(video_path):
    if not is_video(video_path):
        return False
    video_size = os.path.getsize(video_path)
    video = cv2.VideoCapture(video_path)
    width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    video.release()
    filename = os.path.basename(video_path)
    if "(" in filename or ")" in filename:
        return False
    if video_size < MIN_FILE_SIZE:
        return False
    if width != RESOLUTION_WIDTH or height != RESOLUTION_HEIGHT:
        return False
    return True

# webm動画をmp4動画に変換する関数
# 元動画のpathは、../data/ユーザID/動画ID.webmとすると
# 変換後の動画のpathは、../processed_data/ユーザID/動画ID.mp4となる。
def convert_webm_to_mp4(video_path):
    try:
        video_dir = os.path.dirname(video_path)
        video_id = ".".join(os.path.basename(video_path).split(".")[:-1])
        output_dir = video_dir.replace(DATA_DIR, PROCESSED_DATA_DIR)
        mp4_video_path = os.path.join(output_dir, video_id + ".mp4")
        os.system("ffmpeg -i " + video_path + " -vcodec h264 -c:v copy " + mp4_video_path)
        print("Successfully converted webm to mp4:", mp4_video_path)
        return True
    except Exception as e:
        # print("Error occurred while converting webm to mp4:", ".".join(e))
        print("Failed to convert webm to mp4:", video_path)
        return False

# すでにmp4動画に変換されているかどうかをチェックする関数
def is_converted(video_path):
    video_dir = os.path.dirname(video_path)
    video_id = ".".join(os.path.basename(video_path).split(".")[:-1])
    output_dir = video_dir.replace(DATA_DIR, PROCESSED_DATA_DIR)
    mp4_video_path = os.path.join(output_dir, video_id + ".mp4")
    if os.path.exists(mp4_video_path):
        return True
    else:
        return False

# video_pathから日付を取得する関数
def get_date(video_path):
    # 動画ファイル名の中に、標準時の時間が含まれているので、日本時間に変換し取得する。
    # 例えばrec__s__8d8621b1-c250-4c13-8647-7cfcdf5f09b2__2023-04-14T05_26_23.644Z.mp4→04/14
    filename = os.path.basename(video_path)
    utc_time = filename.split("__")[-1].split(".")[0].replace("T", " ").replace("_", ":")
    jst_date = datetime.datetime.strptime(utc_time, "%Y-%m-%d %H:%M:%S").astimezone(datetime.timezone(datetime.timedelta(hours=9))).strftime("%m/%d")
    return jst_date

# 明らかに動画時間に対して容量が小さすぎる動画は、解析に有効でないと判断し、あとで除外する。
# 例えば、1分の動画で100KB以下の動画は、解析に有効でないと判断する。
# また、動画時間が0秒の動画も、解析に有効でないと判断する。
# この関数は、動画のpathを引数にとり、その動画が解析に有効であるかどうかを返す。
def is_valid_video(video_path):
    video_size = os.path.getsize(video_path)
    video_length = get_video_length(video_path)
    if video_length is None:
        return False
    if video_length == 0:
        return False
    if video_size / video_length < MAX_FILE_SIZE_FACTOR:
        return False
    return True

# 解析に有効でなかったmp4動画を削除する関数
def remove_invalid_videos():
    user_dirs = [d for d in os.listdir(PROCESSED_DATA_DIR) if os.path.isdir(os.path.join(PROCESSED_DATA_DIR, d))]
    for user_dir in user_dirs:
        video_paths = os.listdir(os.path.join(PROCESSED_DATA_DIR, user_dir))
        for video_path in video_paths:
            video_path = os.path.join(PROCESSED_DATA_DIR, user_dir, video_path)
            if not is_valid_video(video_path):
                os.remove(video_path)
                print("Removed invalid video:", video_path)
    
    
if __name__ == "__main__":
    user_dirs = [d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))]
    
    # user_dirsのディレクトリ(ファイルは含めない)を、processed_dataディレクトリにコピーする。
    for user_dir in user_dirs:
        os.makedirs(os.path.join(PROCESSED_DATA_DIR, user_dir), exist_ok=True)
    
     # ユーザごとに、有効だった動画をmp4に変換し、その日付ごとに動画の総合計時間を計算し、出力する。
    for user_dir in user_dirs:
        video_paths = os.listdir(os.path.join(DATA_DIR, user_dir))
        valid_video_paths = []
        
        for video_path in video_paths:
            video_path = os.path.join(DATA_DIR, user_dir, video_path)
            if is_valid(video_path):
                if not is_converted(video_path):
                    convert_webm_to_mp4(video_path)
                valid_video_paths.append(video_path)
                
        date_video_paths = {}
        for video_path in valid_video_paths:
            date = get_date(video_path)
            if date not in date_video_paths:
                date_video_paths[date] = []
            # date_video_pathsのパス内"data"を"processed_data"に変更する
            video_path = video_path.replace(DATA_DIR, PROCESSED_DATA_DIR).replace(".webm", ".mp4")
            date_video_paths[date].append(video_path)
        
    # 動画に対して容量が小さすぎる動画は、解析に有効でないと判断し、除外する。
    remove_invalid_videos()
    
    # 日付ごとの動画の総合計時間を計算し、出力する。
    for user_dir in user_dirs:
        print("=====================================")
        print("User:", user_dir)
        date_video_paths = {}
        video_paths = os.listdir(os.path.join(PROCESSED_DATA_DIR, user_dir))
        for video_path in video_paths:
            video_path = os.path.join(PROCESSED_DATA_DIR, user_dir, video_path)
            date = get_date(video_path)
            if date not in date_video_paths:
                date_video_paths[date] = []
            date_video_paths[date].append(video_path)
        
        for date in sorted(date_video_paths):
            total_length = 0
            for video_path in date_video_paths[date]:
                length = get_video_length(video_path)
                if length is None:
                    continue
                total_length += length
            print(date, "{:.1f}".format(total_length / 60) + "min")
