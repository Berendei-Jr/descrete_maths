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

    def is_null(self):
        return sum(self.array) == 0

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
        self.syndroms = []

    def _get_degree(self, array: list):
        if Alpha(0, array).is_null():
            return None
        for el in self.field:
            if el.array == array:
                return el.degree
        else:
            raise ValueError(f'Unknown element {array}')

    def build(self):
        field_built = False

        svobodniy_chlen = 0
        one = Alpha(0, [0 for i in range(self.generator_degree + 1)])
        one.set_array_value(0, 1)
        alpha = Alpha(1, [0 for i in range(self.generator_degree + 1)])
        alpha.set_array_value(1, 1)
        while not field_built:
            self.field.clear()
            alpha.get_value()[-1] = svobodniy_chlen
            self.field.append(one)
            self.field.append(alpha)
            svobodniy_chlen += 1
            previous_degree_alpha = alpha

            for degree in range(2, self.size):
                new_alpha = Alpha(degree, mult_stolbik(alpha(), previous_degree_alpha(), self.z_value))
                while len(new_alpha()) != len(alpha()):
                    new_alpha().pop(0)

                while new_alpha.get_value()[0] != 0:
                    new_alpha = Alpha(degree, self.sub(new_alpha, Alpha(None, self.generator)))
                self.field.append(new_alpha)
                if new_alpha.is_one():
                    if degree == self.size - 1:
                        field_built = True
                    else:
                        break
                elif degree == self.size - 1:
                    raise ValueError('Unable to create field')

                previous_degree_alpha = new_alpha
        print('Поле:')
        for el in self.field:
            print(el)

    def ord(self):
        svobodniy_chlen = 0
        one = Alpha(0, [0 for i in range(self.generator_degree + 1)])
        one.set_array_value(0, 1)
        alpha = Alpha(1, [0 for i in range(self.generator_degree + 1)])
        alpha.set_array_value(1, 1)
        self.field.clear()
        alpha.get_value()[-1] = svobodniy_chlen
        self.field.append(one)
        self.field.append(alpha)
        svobodniy_chlen += 1
        previous_degree_alpha = alpha

        for degree in range(2, self.size):
            new_alpha = Alpha(degree, mult_stolbik(alpha(), previous_degree_alpha(), self.z_value))
            while len(new_alpha()) != len(alpha()):
                new_alpha().pop(0)

            while new_alpha.get_value()[0] != 0:
                new_alpha = Alpha(degree, self.sub(new_alpha, Alpha(None, self.generator)))
            self.field.append(new_alpha)
            if new_alpha.is_one():
                    break

            previous_degree_alpha = new_alpha
        print('Поле:')
        for el in self.field:
            print(el)
        print(f'Ord = {degree}')

    def get_alpha(self, degree) -> Alpha:
        for a in self.field:
            if a.degree == degree:
                return a
        return Alpha(None, [])
    
    def get_alpha_by_array(self, array: list) -> Alpha:
        for a in self.field:
            if a.array == array:
                return a
        return Alpha(None, [])

    def add(self, alpha1: Alpha, alpha2: Alpha):
        if alpha1.is_null():
            return alpha2
        elif alpha2.is_null():
            return alpha1

        new_alpha = []
        for index in range(self.generator_degree + 1):
            new_alpha.append((alpha1.get_value()[index] + alpha2.get_value()[index]) % self.z_value)

        for alpha in self.field:
            if alpha.get_value() == new_alpha:
                return alpha
        if sum(new_alpha) == 0:
            return Alpha(None, [])
        raise ValueError(f'Unknown element {new_alpha}')

    def mult(self, alpha1: Alpha, alpha2: Alpha):
        if alpha1.degree is None or alpha2.degree is None:
            return Alpha(None, [])
        power = (alpha1.degree + alpha2.degree) % (self.size - 1)
        if power == 0:
            return self.get_alpha(0)
        return self.get_alpha(power)

    def power(self, alpha: Alpha, power: int):
        power = alpha.degree*power % (self.size - 1)
        if power == 0:
            return self.get_alpha(0)
        return self.get_alpha(power)

    def sub(self, alpha1: Alpha, alpha2: Alpha):
        a1 = alpha1().copy()
        a2 = alpha2().copy()
        answer = []
        for i in range(len(a1)):
            value = a1[i] - a2[i]
            if value < 0:
                value  = self.z_value + value
            answer.append(value)
        return answer

    def _syndroms_matrix_det(self, m = 3):
        if m == 3:
            a1 = self.mult(self.mult(self.syndroms[0], self.syndroms[2]), self.syndroms[4])
            a2 = self.mult(self.mult(self.syndroms[1], self.syndroms[2]), self.syndroms[3])
            b1 = self.mult(self.mult(self.syndroms[2], self.syndroms[2]), self.syndroms[2])
            b2 = self.mult(self.mult(self.syndroms[1], self.syndroms[1]), self.syndroms[4])
            b3 = self.mult(self.mult(self.syndroms[0], self.syndroms[3]), self.syndroms[3])
            det = self.add(a1, a2)
            det = self.add(det, a2)
            det = self.get_alpha_by_array(self.sub(det, b1))
            det = self.get_alpha_by_array(self.sub(det, b2))
            det = self.get_alpha_by_array(self.sub(det, b3))
            return det
        elif m == 2:
            a1 = self.mult(self.syndroms[0], self.syndroms[2])
            a2 = self.mult(self.syndroms[1], self.syndroms[1])
            return self.get_alpha_by_array(self.sub(a1, a2))

    #def _to_stupenchatiy_vid(self, )

    def find_roots(self, mnogochlen_stepeney):
        roots = []
        for a in self.field:
            if not a.is_null():
                summa = self.get_alpha(mnogochlen_stepeney[len(mnogochlen_stepeney)-1])
                for deg in range(len(mnogochlen_stepeney)-2, -1, -1):
                    alpha = self.get_alpha(mnogochlen_stepeney[deg])
                    slogaemoe = self.mult(alpha, self.power(a, len(mnogochlen_stepeney) - deg - 1))
                    #try:
                    summa = self.add(summa, slogaemoe)
                    #except:
                    #    continue
                if summa.is_null():
                    roots.append(a)
        print(f'Roots:')
        for r in roots:
            print(r)

    def decodeRS(self, word: list, length: int):
        symbol_length = int(len(word)/length)
        word_alphas = []
        for symbol in range(length):
            alpha = [0]
            for i in range(symbol_length):
                alpha.append(word[symbol_length*symbol + i])
            word_alphas.append(Alpha(self._get_degree(alpha), alpha))
        print('***************************************************\ny(x) = ', end = '')
        for i in range(length):
            if word_alphas[i].degree != None:
                print(f'a^{word_alphas[i].degree}*x^{length-1-i} + ', end = '')
        print('\n***************************************************')
        for i in range(6):
            tmp_arr = []
            for j in range(len(word_alphas)):
                s = self.power(self.get_alpha(i+1), length - 1 - j)
                s2 = word_alphas[j]
                if j != length - 1:
                    m = self.mult(s2, s)
                else:
                    m = s2
                tmp_arr.append(m)

            synd = tmp_arr[0]
            print(f'Синдром {i+1}: a^{synd.degree}', end = '')
            for s_i in range(1, len(tmp_arr)):
                print(f' + a^{tmp_arr[s_i].degree} ', end = '')
                synd = self.add(synd, tmp_arr[s_i])
            self.syndroms.append(synd)
            print(f'= a^{synd.degree}')
        print('***************************************************\nНайдем ранг матрицы синдромов')
        detM = self._syndroms_matrix_det()
        r = 0
        print(f'Определитель M: {detM}')
        if detM.degree != None:
            r = 3
        else:
            detM = self._syndroms_matrix_det(m = 2)
            print(f'Определитель M2: {detM}')
            if detM.degree != None:
                r = 2
            else:
                raise ValueError
        print(f'r = {r}')

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

#f = Field(2, [1, 0, 0, 1, 1], 4, 16)
#f = Field(3, [1, 1, 2], 2, 9)
#f.build()
#f.decodeRS([0, 2, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 1, 0, 2, 2], 8)
#f.decodeRS([1, 2, 1, 1, 2, 2, 0, 0, 2, 2, 1, 0, 2, 0, 2, 1], 8)
#f.decodeRS([1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1], 13)

#f.find_roots([0, 6, 6, 4])

#print(mult_stolbik(, [1, 1] ,2))

f = Field(2, [1, 0, 0, 0, 1, 1, 0, 1, 1], 8, 2**8)
#f.build()
f.ord()

#f.find_roots([1, 0, 0, 0, 1, 1, 0, 1, 1])
#for num in range(2, 2**20):
#    b = list(map(int, list(str(bin(num))[2:])))
#    m = mult_stolbik(b, [1, 0, 0, 0, 1, 1, 0, 1, 1], 2)
#   print(len(b))
#    if m[0] == 1 and m[-1] == 1:
#        new_m = m[1:-1]
#        if sum(new_m) == 0:
#            print(b, m, len(m)-1)
#            break
