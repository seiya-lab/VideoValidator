import os
import cv2
import datetime
# �擾���ꂽ���悪��͂ɗL���ł��邩�ǂ������`�F�b�N���A�W�v����B�܂��A�L���ȓ����webm�`������mp4�`���ɕϊ�����B

DATA_DIR = "../data"
PROCESSED_DATA_DIR = "../processed_data"
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
        print("Error occurred while getting video length:", str(e))
        return None

# �L���ȓ���Ƃ́A
#   (����̃t�@�C���T�C�Y)/(����̒���)��10KB�ł��邱�ƁA
#   ����̉𑜓x��1280x720�ł��邱�ƁA
#   ����̃t�@�C���T�C�Y��1MB�ȏ�ł��邱�ƁA
#   �t�@�C������(����)�������Ă��Ȃ�����
# ���w���B 
def is_valid(video_path):
    video_size = os.path.getsize(video_path)
    video_length = get_video_length(video_path)
    video = cv2.VideoCapture(video_path)
    width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    video.release()
    filename = os.path.basename(video_path)
    if "(" in filename or ")" in filename:
        return False
    if video_size < MIN_FILE_SIZE:
        return False
    if video_length == 0:
        return False
    if width != RESOLUTION_WIDTH or height != RESOLUTION_HEIGHT:
        return False
    if video_size > video_length * MAX_FILE_SIZE_FACTOR:
        return False
    return True

# webm�����mp4����ɕϊ�����֐�
# �������path�́A../data/���[�UID/����ID.webm�Ƃ����
# �ϊ���̓����path�́A../processed_data/���[�UID/����ID.mp4�ƂȂ�B
def convert_webm_to_mp4(video_path):
    try:
        video_dir = os.path.dirname(video_path)
        video_id = os.path.basename(video_path).split(".")[:-1]
        output_dir = video_dir.replace(DATA_DIR, PROCESSED_DATA_DIR)
        mp4_video_path = os.path.join(output_dir, video_id + ".mp4")
        os.system("ffmpeg -i " + video_path + " -vcodec h264 -c:v copy" + mp4_video_path)
        return True
    except Exception as e:
        print("Error occurred while converting webm to mp4:", str(e))
        return False

# ���ł�mp4����ɕϊ�����Ă��邩�ǂ������`�F�b�N����֐�
def is_converted(video_path):
    video_dir = os.path.dirname(video_path)
    video_id = os.path.basename(video_path).split(".")[:-1]
    output_dir = video_dir.replace(DATA_DIR, PROCESSED_DATA_DIR)
    mp4_video_path = os.path.join(output_dir, video_id + ".mp4")
    if os.path.exists(mp4_video_path):
        return True
    else:
        return False

# video_path������t���擾����֐�
def get_date(video_path):
    # ����t�@�C�����̒��ɁA�W�����̎��Ԃ��܂܂�Ă���̂ŁA���{���Ԃɕϊ����擾����B
    # �Ⴆ��rec__s__8d8621b1-c250-4c13-8647-7cfcdf5f09b2__2023-04-14T05_26_23.644Z.webm��04/14
    filename = os.path.basename(video_path)
    utc_time = filename.split("__")[-1].split(".")[0].replace("T", " ").replace("_", ":")
    jst_date = datetime.datetime.strptime(utc_time, "%Y-%m-%d %H:%M:%S.%f").astimezone(datetime.timezone(datetime.timedelta(hours=9))).strftime("%m/%d")
    return jst_date
    
    
if __name__ == "__main__":
    user_dirs = os.listdir(DATA_DIR)
    print(user_dirs)
    
     # ���[�U���ƂɁA�L�������������mp4�ɕϊ����A���̓��t���Ƃɓ���̑����v���Ԃ��v�Z���A�o�͂���B
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
            date_video_paths[date].append(video_path)
            
        for date in date_video_paths:
            total_time = 0
            for video_path in date_video_paths[date]:
                total_time += get_video_length(video_path)
            print(user_dir, date, total_time)
