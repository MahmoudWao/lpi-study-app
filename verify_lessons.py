import json,sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
with open(r'C:\Users\miikharo\lpi-study-app\structured_data.json','r',encoding='utf-8') as f:
    data=json.load(f)
for sec_id in ['3.1','4.4','5.3']:
    lesson=data[sec_id]['full_lesson']
    print(f"=== {sec_id} ===")
    print(lesson[:400])
    print("...\n")
