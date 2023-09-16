import shelve

class SomeData():
    def __init__(self):
        self.goo = "gooey"
        self.poo = "poopy"
        self.how_many = 5
        self.doubles = 2.3343

    def to_string(self):
        print("Here are the data:\n",
            self.goo,"\n",
            self.poo,"\n",
            self.how_many,"\n",
            self.doubles,"\n",
            "Thanks!")
    def default(self, o):
        pass

def main():
    d = SomeData()
    d.to_string()
    print(d)
    with shelve.open("test2") as f:
        f['data'] = d
    
    with shelve.open("test2") as f:
        e = f['data']
    
    e.doubles = 2.222
    print(d)
    e.to_string()
    print(e)

if __name__ == "__main__":
    main()