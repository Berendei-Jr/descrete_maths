def to_another_system(num, base):
    chastnoe = 1
    ostatki = []
    while chastnoe != 0:
        chastnoe = int(num/base)
        ostatki.append(num % base)
        num = chastnoe
    ans = []
    for i in range(len(ostatki)-1, -1, -1):
        ans.append(ostatki[i])
    return ans

def mult_stolbik(array1, array2, z):
    result_array_size = len(array1)+len(array2)-1
    strings = []
    for second_index in range(len(array2)-1, -1, -1):
        string = [0 for i in range(len(array1))]
        for first_index in range(len(array1)-1, -1, -1):
            string[first_index] = (array1[first_index] * array2[second_index]) % z
        for i in range(second_index):
            string.insert(0, 0)
        for i in range(result_array_size - len(string)):
            string.append(0)
        strings.append(string)
    new_array = []
    for i in range(result_array_size):
        v = 0
        for string in strings:
            v = (v + string[i]) % z
        new_array.append(v)
    return new_array


class Alpha:
    def __init__(self, degree, array) -> None:
        self.degree = degree
        self.array = array

    def __str__(self) -> str:
        return f'a^{self.degree} = {self.array}'

    def __call__(self):
        return self.array

    def is_one(self):
        tmp_alpha = self.array.copy()
        tmp_alpha[-1] -= 1
        for i in tmp_alpha:
            if i != 0:
                return False
        return True

    def get_value(self):
        return self.array

    def set_array_value(self, i, value):
        self.array[-(i+1)] = value

class Field:
    def __init__(self, z_value, generator, generator_degree, size) -> None:
        self.z_value = z_value
        self.generator = generator
        self.generator_degree = generator_degree
        self.size = size
        self.field = []

    def _get_degree(self, array: list):
        for el in self.field:
            if el.array == array:
                return el.degree
        else:
            raise ValueError(f'Unknown element {array}')

    def build(self):
        field_built = False

        svobodniy_chlen = 0
        alpha = Alpha(1, [0 for i in range(self.generator_degree + 1)])
        alpha.set_array_value(1, 1)
        while not field_built:
            self.field.clear()
            alpha.get_value()[-1] = svobodniy_chlen
            self.field.append(alpha)
            svobodniy_chlen += 1
            previous_degree_alpha = alpha

            for degree in range(2, self.size):
                new_alpha = Alpha(degree, mult_stolbik(alpha(), previous_degree_alpha(), self.z_value))
                while len(new_alpha()) != len(alpha()):
                    new_alpha().pop(0)

                while new_alpha.get_value()[0] != 0:
                    new_alpha = Alpha(degree, self.sub(new_alpha(), self.generator))
                self.field.append(new_alpha)
                if new_alpha.is_one():
                    if degree == self.size - 1:
                        field_built = True
                    break
                elif degree == self.size - 1:
                    raise ValueError('Unable to create field')

                previous_degree_alpha = new_alpha
        for el in self.field:
            print(el)

    def add(self, alpha1: Alpha, alpha2: Alpha):
        new_alpha = []
        for index in range(self.generator_degree + 1):
            new_alpha[index] = (alpha1.get_value()[index] + alpha2.get_value()[index]) % self.z_value

        for alpha in self.field:
            if alpha.get_value() == new_alpha:
                return alpha
        raise ValueError(f'Unknown element {new_alpha}')

    #def mult(self, alpha1: Alpha, alpha2: Alpha):
    #    values = []
    #    for second_index in range(self.generator_degree, -1, -1):
    #        string = []
    #        for first_index in range(self.generator_degree, -1, -1):
    #            string[first_index] = (alpha1[first_index] * alpha2[second_index]) % self.z_value
    #        values.append(string)

    def sub(self, alpha1: list, alpha2: list):
        answer = []
        for i in range(len(alpha1)):
            value = alpha1[i] - alpha2[i]
            if value < 0:
                value  = self.z_value + value
            answer.append(value)
        return answer

    def decodeRS(self, word: list, length: int):
        symbol_length = int(len(word)/length)
        word_alphas = []
        for symbol in range(length):
            alpha = [0]
            for i in range(symbol_length):
                alpha.append(word[symbol_length*symbol + i])
            word_alphas.append(Alpha(self._get_degree(alpha), alpha))
        for i in word_alphas:
            print(alpha)

    #def divide_mnogochlen(self, array1, array2):
    #    answer = [0]
    #    max_number_in_z_system = []
    #    for i in range(self.generator_degree):
    #        max_number_in_z_system.append(self.z_value - 1)
    #
    #    i = 0
    #    while mult_stolbik(answer, array2, self.z_value) != array1:
    #        i += 1
    #        answer = to_another_system(i, self.z_value)
    #    return answer

f = Field(3, [1, 1, 2], 2, 9)
f.build()
f.decodeRS([1, 2, 1, 1, 2, 2, 0, 0, 2, 2, 1, 0, 2, 0, 2, 1], 8)
