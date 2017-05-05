class A:
    def method(self):
        def get():
            print('Get!')
        return get
    def use(self):
        fun = self.method()
        fun()
        p1()

def p1():
    print(1)

if __name__ == '__main__':
    a = A()
    a.use()
