# Youtube自動下載 Ver 1.1
使用 YouTube Data API v3<br>
會自動擷取正在直播中的網址使用並 yt-dlp 進行下載<br>
API 配額計數器避免超過當天的配額限制 免費配額為 10,000 次，台灣下午3點重置<br>
預設每次執行消耗 6 次 API 配額 剛啟動時會多消耗 1 次<br>
可自訂頻道與下載路徑並自動按日期時間區分資料夾<br>

## 安裝
安裝 Python https://www.microsoft.com/store/productId/9PJPW5LDXLZ5<br>
Python 函式庫安裝 ```pip install google-api-python-client```<br>
安裝 yt-dlp https://github.com/yt-dlp/yt-dlp<br>
安裝 ffmpeg https://www.gyan.dev/ffmpeg/builds/#libraries <br>
yt-dlp與ffmpeg安裝方式，網路上有許多教學<br>
申請憑證 API 金鑰 https://console.cloud.google.com/ 並選擇 YouTube Data API v3 程式庫<br>
如果沒有編輯器推薦安裝 Notepad++ https://notepad-plus-plus.org/downloads/

### 效果展示
在指定的資料夾處自動生成日期時間
![image](https://user-images.githubusercontent.com/78526289/235908490-7646254c-b39b-4159-b09d-a80a2fc855ea.png)
