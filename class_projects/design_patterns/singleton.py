limit_strategy_ref = None

class LimitStartegy:
    def __init__(self):
        global limit_strategy_ref
        if limit_strategy_ref is not None:
            raise Exception("should not use this again")
        
        limit_strategy_ref = self

class CreateSingleton:
    def __init__(self):
        self.singleton_dict = []

        def create(self, object_type):
            if object_type not in self.singleton_dict:
                self.singleton_dict[object_type] = LimitStartegy()
            return self.singleton_dict[object_type]

cs = CreateSingleton()
a = cs.create("limit")
b = cs.create("limit")

if a==b: print("ciao")