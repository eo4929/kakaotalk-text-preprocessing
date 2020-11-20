## 단일 카카오톡 대화 txt를 json 형태로 변환

```
$ python convert_txt_to_json.py {fileName}
```

## 단일 카카오톡 대화 txt에서 feature 추출

```
$ python get_features.py {fileName} {userName}
```

## 여러 카카오톡 대화들에서 한번에 feature 추출 및 csv로 저장

```
$ python make_csv.py
```

* input.json 작성 필요
* output.csv 에 결과 저장

```
{
    "args":[
        {
            "fileName": "./data/input_1.txt",
            "userName": "A"
        },
        {
            "fileName": "./data/input_2.txt",
            "userName": "B"
        },
        ...
    ]
}
```

## Using

* Python 3

