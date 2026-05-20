import json
import os
import datetime
import urllib.request

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")
START_DATE = datetime.date(2026, 5, 20)  # 오늘부터 시작

with open("words_data.json", encoding="utf-8") as f:
    all_days = json.load(f)

today = datetime.date.today()
day_index = (today - START_DATE).days % len(all_days)
words = all_days[day_index]

fields = []
for w in words:
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

with urllib.request.urlopen(req) as res:
    print(f"✅ 전송 완료! 상태코드: {res.status}")
