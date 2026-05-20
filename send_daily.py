import json
import os
import datetime
import urllib.request

# ===== 설정 =====
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")
START_DAY_INDEX = int(os.environ.get("START_DAY_INDEX", "0"))  # 몇 번째 날부터 시작할지
# ================

with open("words_data.json", encoding="utf-8") as f:
    all_days = json.load(f)

# 오늘이 시작일로부터 몇 번째 날인지 계산
start_date = datetime.date(2025, 1, 20)  # 첫 번째 단어 날짜
today = datetime.date.today()
day_index = (today - start_date).days

if day_index < 0 or day_index >= len(all_days):
    print(f"오늘({today})은 단어 범위 밖입니다. (0~{len(all_days)-1}일)")
    exit(0)

words = all_days[day_index]

# Discord embed 메시지 구성
fields = []
for w in words:
    # word_line 파싱: "漢字(reading) : 뜻" 형태
    fields.append({
        "name": w["word_line"],
        "value": f"_{w['sentence_jp']}_\n{w['romanization']}\n{w['sentence_kr']}",
        "inline": False
    })

embed = {
    "title": f"🍪 오늘의 일본어 단어 — {today.strftime('%m/%d')} ({day_index+1}일차)",
    "color": 0xFFA500,
    "fields": fields,
    "footer": {"text": f"총 {len(all_days)}일 중 {day_index+1}일째"}
}

payload = json.dumps({"embeds": [embed]}).encode("utf-8")

req = urllib.request.Request(
    WEBHOOK_URL,
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST"
)

try:
    with urllib.request.urlopen(req) as res:
        print(f"✅ 전송 완료! 상태코드: {res.status}")
except Exception as e:
    print(f"❌ 전송 실패: {e}")
