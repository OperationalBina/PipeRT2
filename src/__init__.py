

dict = {
    "tomer": {
        "f": True,
        "t" : False
    }
}

dict.setdefault("tomer", {"f": False})
dict["tomer"].update({"f": False})

print(dict)
