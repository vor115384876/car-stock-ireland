class ConstantBaseModel:
    def __init__(self, csv_data):
        self._data = dict()
        for row in csv_data:
            self._data[int(row[0])] = row[1:]

    def get_constant(self, year:int, cat:int=None):
        # print(f'getting min in {self._data.keys()} and {year}')
        year_to_use =  max(min(self._data.keys()),year)
        if cat is None:
            return self._data[year_to_use]
        else:
            return self._data[year_to_use][cat-1]

    def update_year_constant(self, year:int, values:[int]):
        year_to_use =  max(min(self._data.keys()),year)
        self._data[year_to_use] = values

class BaseModel:
    def __init__(self, year, csv_data):
        self._year = year
        # print(year)
        self._data = [list(map(int, row)) for row in csv_data]


    def get_counts(self, age:int=None, cat:int=None):
        if age is not None:
            if cat is not None:
                return self._data[age][cat-1]
            else:
                return self._data[age]
        elif cat is not None:
            return [x[cat-1] for x in self._data]
        else:
            return self._data

    def get_car_year(self, age):
        return self._year-age

    def get_max_age(self):
        return len(self._data) - 1

    def get_cat_counts(self):
        # print("aagg")
        # print(len(self._data[0]))
        # [print(sum(int(row[i])) for row in self._data) for i in range(len(self._data[0]))]
        return [sum(int(row[i]) for row in self._data) for i in range(len(self._data[0]))]

    def apply_constant(self, model:ConstantBaseModel):
        new_model = []
        max_age = self.get_max_age()
        for age in range(max_age):
            year = self.get_car_year(age=age)
            new_row = [float(a)*float(b) for a,b in zip(self.get_counts(age=age),model.get_constant(year=year))]
            new_model.append(new_row)
        return new_model
