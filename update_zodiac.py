import re, random
from datetime import datetime, timezone, timedelta

tz = timezone(timedelta(hours=8))
today = datetime.now(tz)
date_str = today.strftime('%Y年%m月%d日')
weekdays = ['星期一','星期二','星期三','星期四','星期五','星期六','星期日']
weekday = weekdays[today.weekday()]
base_seed = today.year * 10000 + today.month * 100 + today.day

levels = ['good','normal','weak']
zodiacs = [
    ('白羊座','3月21日 - 4月19日','♈'),('金牛座','4月20日 - 5月20日','♉'),
    ('双子座','5月21日 - 6月21日','♊'),('巨蟹座','6月22日 - 7月22日','♋'),
    ('狮子座','7月23日 - 8月22日','♌'),('处女座','8月23日 - 9月22日','♍'),
    ('天秤座','9月23日 - 10月23日','♎'),('天蝎座','10月24日 - 11月22日','♏'),
    ('射手座','11月23日 - 12月21日','♐'),('摩羯座','12月22日 - 1月19日','♑'),
    ('水瓶座','1月20日 - 2月18日','♒'),('双鱼座','2月19日 - 3月20日','♓')
]

# 详细的运势描述模板
overall_templates = {
    'good': [
        "今日运势良好，各方面都比较顺利，可以大胆尝试新事物。",
        "运势不错，今天做事容易成功，适合处理重要事务。",
        "整体运势良好，心情愉悦，适合社交和团队合作。"
    ],
    'normal': [
        "今日运势一般，工作、生活上习惯稳妥行事，不想给自己制造压力感。",
        "运势平稳，按部就班即可，不宜做重大决策。",
        "整体运势一般，保持平常心，做好分内事就好。"
    ],
    'weak': [
        "今日运势较弱，做事容易遇到阻碍，需要多加耐心。",
        "运势不佳，建议保守行事，避免冒险和冲动决定。",
        "整体运势较弱，注意调整心态，避免与人发生冲突。"
    ]
}

love_templates = {
    'good': [
        "感情方面运势良好，双方相处融洽，沟通顺畅。",
        "感情运势不错，适合约会或表达心意。",
        "感情方面良好，关系稳定，彼此信任。"
    ],
    'normal': [
        "感情方面运势普通，双方相处有些话不好意思说可能会有误会产生，也不利于互相增进了解。",
        "感情运势一般，需要多花时间经营关系。",
        "感情方面普通，保持现状即可，避免敏感话题。"
    ],
    'weak': [
        "感情方面运势较弱，容易产生误会，需要多沟通。",
        "感情运势不佳，注意控制情绪，避免争吵。",
        "感情方面较弱，需要给彼此一些空间和时间。"
    ]
}

career_templates = {
    'good': [
        "事业方面运势良好，工作进展顺利，容易获得认可。",
        "事业运势不错，适合开展新项目或提出建议。",
        "事业方面良好，团队合作愉快，工作效率高。"
    ],
    'normal': [
        "事业方面运势一般，工作上有些事做起来没什么挑战但风险确实少，如果你担心拿不下业绩选择这种方式做任务无可厚非。",
        "事业运势平稳，按计划完成工作即可。",
        "事业方面一般，保持现状，不宜跳槽或转行。"
    ],
    'weak': [
        "事业方面运势较弱，可能遇到挑战，需要谨慎处理。",
        "事业运势不佳，工作压力大，注意劳逸结合。",
        "事业方面较弱，避免与同事发生冲突，保持低调。"
    ]
}

wealth_templates = {
    'good': [
        "财运方面运势良好，投资理财机会不错，适合规划财务。",
        "财运不错，可能有意外收入，但需理性消费。",
        "财运方面良好，收支平衡，储蓄稳定增长。"
    ],
    'normal': [
        "财运方面运势平平，日常生活开销正常，没有特别大的支出也没有特别大的收入。",
        "财运一般，保持现有理财方式即可。",
        "财运方面平稳，不宜进行高风险投资。"
    ],
    'weak': [
        "财运方面运势较弱，需要控制开支，避免冲动消费。",
        "财运不佳，投资需谨慎，避免损失。",
        "财运方面较弱，注意节约，做好预算规划。"
    ]
}

health_templates = {
    'good': [
        "健康方面运势良好，身体状况不错，精力充沛。",
        "健康运势良好，适合运动锻炼，保持良好作息。",
        "健康方面良好，心情愉快，抵抗力强。"
    ],
    'normal': [
        "健康方面运势一般，注意劳逸结合，避免过度劳累。",
        "健康运势平稳，保持现有生活习惯即可。",
        "健康方面一般，注意饮食均衡，适当运动。"
    ],
    'weak': [
        "健康方面运势较弱，需要关注身体，及时休息。",
        "健康运势不佳，注意预防疾病，避免熬夜。",
        "健康方面较弱，注意保暖，避免受凉。"
    ]
}

def get_random_template(templates, level):
    return random.choice(templates[level])

with open('index.html','r',encoding='utf-8') as f:
    html = f.read()

# 更新日期
html = re.sub(
    r'id="currentDate">[^<]*</div>',
    f'id="currentDate">{date_str} {weekday}</div>',
    html
)

# 更新星座数据 - 替换整个 zodiacData 对象
new_data = 'const zodiacData = {\n'
for i,(name,dates,icon) in enumerate(zodiacs):
    random.seed(base_seed + hash(name) % 100000)
    ol,ll,cl,wl,hl = [random.choice(levels) for _ in range(5)]
    
    new_data += f'            "{name}": {{\n'
    new_data += f'                icon: "{icon}",\n'
    new_data += f'                dates: "{dates}",\n'
    new_data += f'                overall: "{get_random_template(overall_templates, ol)}",\n'
    new_data += f'                overallLevel: "{ol}",\n'
    new_data += f'                love: "{get_random_template(love_templates, ll)}",\n'
    new_data += f'                loveLevel: "{ll}",\n'
    new_data += f'                career: "{get_random_template(career_templates, cl)}",\n'
    new_data += f'                careerLevel: "{cl}",\n'
    new_data += f'                wealth: "{get_random_template(wealth_templates, wl)}",\n'
    new_data += f'                wealthLevel: "{wl}",\n'
    new_data += f'                health: "{get_random_template(health_templates, hl)}",\n'
    new_data += f'                healthLevel: "{hl}"\n'
    new_data += '            }' + (',' if i < 11 else '') + '\n'
new_data += '        };'

html = re.sub(r'const zodiacData = \{[\s\S]*?\};', new_data, html)

with open('index.html','w',encoding='utf-8') as f:
    f.write(html)

print(f'Updated for {date_str} {weekday}')