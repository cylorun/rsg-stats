import glob, os, json, time, tkinter, threading

def make_stats():
    enter_times = []
    bastion_times = []
    fort_times = []
    enters = 0
    bastions = 0
    forts = 0
    print(f'Tracking {records_path}')
    while True:
        records = glob.glob(f'{records_path}\\*.json')
        for record in records:
            with open(record, 'r') as file:
                data = json.load(file)

            timelines = data.get("timelines", [])
            for timeline in timelines:
                print('broom')
                if timeline.get("name") == 'enter_nether':
                    enters += 1
                    enter_times.append(timeline.get("igt", 0) / 1000)
                if timeline.get("name") == 'enter_bastion':
                    bastions += 1
                    bastion_times.append(timeline.get("igt", 0) / 1000)
                if timeline.get("name") == 'enter_fortress':
                    forts += 1
                    fort_times.append(timeline.get("igt", 0) / 1000)
                os.remove(record)
                
        with open(f'{os.getcwd()}\\stats.txt', 'w+') as stat_file:
            stats = ''
            for key, value in settings.items():
                if value:
                    match key:
                        case 'nph': stats+= f'NPH: {round(enters / ((time.time() - start_time)/3600),1)}\n'
                        case 'enter-avg': stats+= f'AVG ENTER: {avg_time(enter_times)}\n'
                        case 'enter-count': stats+= f'ENTERS: {enters}\n'
                        case 'bastion-count': stats+= f'BASTIONS: {bastions}\n'
                        case 'bastion-time': stats+= f'BATSION ENTER: {avg_time(bastion_times)}\n'
                        case 'fort-count': stats+= f'FORTS: {forts}\n'
                        case 'fort-time': stats+= f'FORT ENTER: {avg_time(fort_times)}\n'
            stat_file.write(stats)
        time.sleep(10)

def avg_time(times):
    min, sec = divmod(int(sum(times) // len(times) if times else 0), 60)
    return f'{min}:{sec:02}'
    
def load_settings():
    try:
        with open('config.json', "r") as json_file:
            data = json.load(json_file)
            for key in settings:
                if key in data:
                    settings[key] = data[key]
    except FileNotFoundError:
        pass

def save_settings():
    for key, value in boxes.items():
        settings[key] = value.get()
    with open('config.json', "w") as json_file:
        json.dump(settings, json_file)

def make_box(i, setting):
    var = tkinter.BooleanVar(root, value=settings[setting])
    checkbox = tkinter.Checkbutton(root, text=setting, variable=var)
    checkbox.grid(row=i, column=0)
    boxes[setting] = var


records_path = f'{os.environ['USERPROFILE']}\\speedrunigt\\records'
start_time = time.time()
root = tkinter.Tk()
boxes = {}
settings = {
    "nph":True,
    "enter-avg":True,
    "enter-time":True,
    "enter-count":True,
    "bastion-time":True,
    "bastion-count":True,
    "fort-time":True,
    "fort-count":True
}

load_settings()
for i,key in enumerate(settings):
    make_box(i,key)

tkinter.Button(root, text="Save", command=save_settings).grid(row=8,column=0)
threading.Thread(target=make_stats).start()
root.resizable(False,False)
root.geometry('150x230')
root.mainloop()