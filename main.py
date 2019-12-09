import elperuano
import json
import datetime

source = elperuano.Source()

source.load_info_person("susana villarán", deep=True)


def default(o):
    if type(o) is datetime.date or type(o) is datetime.datetime:
        return o.isoformat()


with open("susanavillaran.json", "w+") as f:
    data = json.dumps(source.raw_dataset, default=default)
    f.write(data)
