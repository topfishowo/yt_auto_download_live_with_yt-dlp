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

## 注意事項
確定都有安裝好後<br>
yt-dlp config.txt 中請勿使用 ```--embed-thumbnail``` 有機率無法擷取直播封面造成錯誤<br>
推薦設定多線程下載提升性能 ```-N 8``` <br>
直播結束後請勿馬上關閉應用，要等到ffmpeg合併好直播後在關閉※需要一小段時間，處理完成時會跳出綠色的"影片處理完成"<br>
CMD 視窗可用 Ctrl+C 進行關閉<br>

### 效果展示
在指定的資料夾處自動生成日期時間<br>
![image](https://user-images.githubusercontent.com/78526289/235908490-7646254c-b39b-4159-b09d-a80a2fc855ea.png)<br>
API 配額消耗計數，讓你掌握消耗了多少配額，並於台灣下午3點重置<br>
![image](https://user-images.githubusercontent.com/78526289/235909118-04378dba-4934-4487-be66-2cbde9e9cdf5.png)<br>
影片成功擷取到直播時<br>
![image](https://user-images.githubusercontent.com/78526289/235911283-b7004ee0-53eb-48cc-968d-ce9901545153.png)<br>
