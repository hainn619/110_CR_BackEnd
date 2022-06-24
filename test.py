from wsgiref.util import request_uri


elements = ["a", "b", "c", "d", "e", ]

for i in elements:
    print(i)


def about():
    me = {
        "first": "hai",
        "last": "nguyen",
        "age": "100"
    }
    return "hai nguyen"



app.run(debug=True)
