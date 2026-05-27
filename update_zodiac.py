import re, random
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
today = datetime.now(tz)
date_str = today.strftime('%Y年%m月%d日')
weekdays = ['星期一','星期二','星期三','星期四','星期五','星期六','星期日']
weekday = weekdays[today.weekday()]
seed = today.year * 10000 + today.month * 100 + today.day
levels = ['good','normal','weak']

zodiacs = [
    ('白羊座','3月21日-4月19日'),('金牛座','4月20日-5月20日'),
    ('双子座','5月21日-6月21日'),('巨蟹座','6月22日-7月22日'),
    ('狮子座','7月23日-8月22日'),('处女座','8月23日-9月22日'),
    ('天秤座','9月23日-10月23日'),('天蝎座','10月24日-11月22日'),
    ('射手座','11月23日-12月21日'),('摩羯座','12月22日-1月19日'),
    ('水瓶座','1月20日-2月18日'),('双鱼座','2月19日-3月20日')
]

with open('index.html','r',encoding='utf-8') as f:
    html = f.read()

new_data = 'const twelveZodiacsData = {\n'
for i,(name,dates) in enumerate(zodiacs):
    random.seed(seed + hash(name))
    ol,ll,cl,wl,hl = [random.choice(levels) for _ in range(5)]
    ot = {'good':'良好','normal':'一般','weak':'较弱'}[ol]
    lt = {'good':'良好','normal':'一般','weak':'较弱'}[ll]
    ct = {'good':'良好','normal':'一般','weak':'较弱'}[cl]
    wt = {'good':'良好','normal':'一般','weak':'较弱'}[wl]
    ht = {'good':'良好','normal':'一般','weak':'较弱'}[hl]
    new_data += f'            "{name}": {{\n'
    new_data += f'                icon: "{chr(9792+i) if i<12 else chr(9800+i-12)}",\n'
    new_data += f'                dates: "{dates}",\n'
    new_data += f'                overall: "今日运势{ot}。",\n'
    new_data += f'                overallLevel: "{ol}",\n'
    new_data += f'                love: "感情方面运势{lt}。",\n'
    new_data += f'                loveLevel: "{ll}",\n'
    new_data += f'                career: "事业方面运势{ct}。",\n'
    new_data += f'                careerLevel: "{cl}",\n'
    new_data += f'                wealth: "财运方面运势{wt}。",\n'
    new_data += f'                wealthLevel: "{wl}",\n'
    new_data += f'                health: "健康方面运势{ht}。",\n'
    new_data += f'                healthLevel: "{hl}"\n'
    new_data += '            }' + (',' if i < 11 else '') + '\n'
new_data += '        };'

html = re.sub(r'const twelveZodiacsData = \{[\s\S]*?\};', new_data, html)
html = re.sub(r"id='currentDate'>[^<]*运势</div>", f"id='currentDate'>{date_str} {weekday} 运势</div>", html)

with open('index.html','w',encoding='utf-8') as f:
    f.write(html)
print(f'Updated for {date_str} {weekday}')
