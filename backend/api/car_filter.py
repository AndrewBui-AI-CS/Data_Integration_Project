from backend import mongodb


class CarFilter():
    def __init__(self):
        self.car_db = mongodb['car']
    
    # def find(self, fields):
    #     for field in fields:
            