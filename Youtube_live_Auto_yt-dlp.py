from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import time
import subprocess
import datetime
import os

#============================YouTube Data API v3 設定&其他參數============================#
# 設定要取得的頻道 ID
CHANNEL_ID = 'YT_CHANNEL_ID'
# 森森鈴蘭  UC3ZTQ8VZVCpwLHjFKSFe5Uw
# 瑪格麗特  UCbh7KHPMgYGgpISdbF6l0Kw
# 柴崎楓音  UCqGLWrvVOqtrpxFdoTY5tYg  柴柴日常  UCo6kgNRCyQPObsfJNMEIwFQ

# 設定 YouTube Data API 金鑰
API_KEY = 'YOUR_API_KEY'

# 設定頻道播放清單讀取上限 消耗對應數量 API 配額
channel_list_maxResults = 5
# 設定等待秒數，以 24 小時為例，每個 API 消耗需要 9 秒冷卻 ※迴圈每次消耗 1 開始執行消耗 1
wait_time = 60
# 推薦設置 上限5 秒數60

# 設定下載資料夾的路徑
download_folder = "C:/Users/User/Desktop"
#=========================================================================================#

# 建立 YouTube Data API 的客戶端
youtube = build('youtube', 'v3', developerKey=API_KEY)

print('\033[32m' + "//////YouTube Data API v3設置完成 開始執行//////" + '\033[0m')
print(f'目前設置間隔時間 {wait_time} 秒')
print(f'播放清單範圍上限 {channel_list_maxResults} 個')
print(f'偵測目標頻道 ID {CHANNEL_ID}')
print(f'下載路徑 {download_folder}\n')

# 取得目前 Python 檔案所在目錄的絕對路徑
dir_path = os.path.dirname(os.path.abspath(__file__))

# 設定儲存計數器和日期的檔案路徑
count_file = os.path.join(dir_path, 'count.txt')

# 如果檔案不存在，就建立一個新的，預設次數為 0，日期為今天
if not os.path.exists(count_file):
    with open(count_file, 'w') as f:
        f.write('0\n' + str(datetime.date.today()))
        print('\033[32m' + "計數器資料建立完成\n" + '\033[0m')
        
# 如果下載資料夾不存在，就建立一個
if not os.path.exists(download_folder):
    os.makedirs(download_folder)
    print('\033[32m' + "下載資料夾建立完成\n" + '\033[0m')

# 讀取檔案中的次數和日期
with open(count_file, 'r') as f:
    data = f.read().split('\n')
    if len(data) == 2:
        count, saved_date = data
    else:
        count, saved_date = 0, str(datetime.date.today())

# 將次數轉換為整數
count = int(count)

# 先取得頻道的 uploads 播放清單 ID
channel_response = youtube.channels().list(
    part='contentDetails',
    id=CHANNEL_ID
).execute()
count += 1
with open(count_file, 'w') as f:
    f.write(f"{count}\n{saved_date}")

playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
# 持續監測並計算次數
while True:
    # 取得當前時間
    current_time = time.strftime("%H:%M:%S", time.localtime())
    
        # 如果進入新的一天且時間 >= 下午3點，就重置計數器
    if datetime.date.today() != datetime.date.fromisoformat(saved_date) and current_time >= "15:00:00":
        saved_date = str(datetime.date.today())
        count = 0
        print('\033[32m' + f"成功重置 API 配額計數               \n" + '\033[0m')
        
    try:
        # 取得 uploads 播放清單指定數量個影片資訊
        playlist_response = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=channel_list_maxResults
        ).execute()
        count += 1
        
        # 將影片資訊放入列表中
        video_list = playlist_response['items']

        # 將列表中的影片資訊依照時間排序，最新的排在最前面
        video_list = sorted(video_list, key=lambda x: x['snippet']['publishedAt'], reverse=True)

        for video in video_list:
            video_id = video['snippet']['resourceId']['videoId']

            # 取得影片詳細資訊，判斷是否正在直播中
            video_response = youtube.videos().list(
                part='liveStreamingDetails',
                id=video_id
            ).execute()
            
            # 增加計數器並將次數和日期存儲到檔案中
            count += 1
            with open(count_file, 'w') as f:
                f.write(f"{count}\n{saved_date}")

            if 'liveStreamingDetails' in video_response['items'][0] and 'activeLiveChatId' in video_response['items'][0]['liveStreamingDetails']:
                # 直播正在進行中，取得直播網址
                live_streaming_details = video_response['items'][0]['liveStreamingDetails']
                if 'actualStartTime' in live_streaming_details:
                    actual_start_time = datetime.datetime.fromisoformat(live_streaming_details['actualStartTime'][:-1])
                    if actual_start_time <= datetime.datetime.now(actual_start_time.tzinfo):
                        live_chat_id = live_streaming_details['activeLiveChatId']
                        live_url = f'https://www.youtube.com/live_chat?v={video_id}&is_popout=1&live_chat_id={live_chat_id}'

                        print('\033[36m' + f"成功找到直播串流 開始下載 API餘額 {10000-count} 次..." + '\033[0m')

                        # 取得當前日期與時間
                        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
                        # 構造目錄路徑
                        folder_path = os.path.join(download_folder, current_time)
                        # 建立目錄
                        os.makedirs(folder_path, exist_ok=True)
                        # 建立完整下載路徑
                        download_folder_path = os.path.join(folder_path, '%(title)s.%(ext)s')

                        # 使用 yt-dlp 指令下載直播影片
                        subprocess.run(['yt-dlp', '-f bv+ba', '--live-from-start', '--no-part', '--output', download_folder_path, live_url])
                        
                        print('\033[32m' + "\n影片處理完成\n" + '\033[0m')
                        
            else:
                # 直播未開始並顯示計數器次數
                print(f'未找到直播串流 API餘額 {10000-count} 次...', end="\r")

    # 除錯用
    except HttpError as e:
        print('\033[31m' + '發生了一個 HTTP 錯誤： %s' % e + '\033[0m')#紅
    except Exception as error:
        print(f'發生錯誤：{error}')
        
    # 等待wait_time秒
    time.sleep(wait_time)