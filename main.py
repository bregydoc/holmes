import elperuano

source = elperuano.Source()

source.load_info_person("martín vizcarra")

for d in source.raw_dataset:
    print(d)
