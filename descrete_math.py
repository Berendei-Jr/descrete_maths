def convert_to_another_system(num: int, base: int) -> int:
    """
    Convert a number to another numeral system.

    Args:
        num (int): The number to be converted.
        base (int): The base of the numeral system to convert to.

    Returns:
        int: The number in the new numeral system.
    """
    chastnoe = 1
    ostatki = []
    while chastnoe != 0:
        chastnoe = int(num / base)
        ostatki.append(num % base)
        num = chastnoe
    ans = []
    for i in range(len(ostatki) - 1, -1, -1):
        ans.append(ostatki[i])
    return int(''.join(map(str, ans)))


def multiply_stolbik(array1: list, array2: list, z: int):
    """
    Multiply two arrays using the 'stolbik' (column-by-column) method with modulo z.

    Args:
    array1 (list): The first array to be multiplied.
    array2 (list): The second array to be multiplied.
    z (int): The modulo value.

    Returns:
    list: The result of multiplying the two arrays using the 'stolbik' method with modulo z.
    """
    result_array_size = len(array1) + len(array2) - 1
    strings = []
    for second_index in range(len(array2) - 1, -1, -1):
        string = [0 for i in range(len(array1))]
        for first_index in range(len(array1) - 1, -1, -1):
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
    """
    Class for representing element in field.
    """

    def __init__(self, degree, array) -> None:
        self.degree = degree
        self.array = array

    def __str__(self) -> str:
        return f'a^{self.degree} =\t{self.array[1:]}'

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
        self.array[-(i + 1)] = value


class Field:
    """
    Class for representing a field.
    """

    def __init__(self, z_value, generator) -> None:
        self.z_value = z_value
        self.generator = generator
        self.generator_degree = len(generator) - 1
        self.size = z_value ** self.generator_degree
        self.field = []

    def _get_degree(self, array: list):
        if Alpha(0, array).is_null():
            return None
        for el in self.field:
            if el.array == array:
                return el.degree
        else:
            raise ValueError(f'Unknown element {array}')

    def build(self):
        """
        This function builds the field based on the generator degree and size,
        appending new Alphas to the field until the field is fully built. It
        raises a ValueError if the field cannot be created.
        """
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
                new_alpha = Alpha(degree, multiply_stolbik(alpha(), previous_degree_alpha(), self.z_value))
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
        print('Field:')
        for el in self.field:
            print(el)

    def calculate_order(self):
        """
        Calculate the order of the field, populating the field list with Alpha objects.
        """
        constant_term = 0
        one = Alpha(0, [0] * (self.generator_degree + 1))
        one.set_array_value(0, 1)
        alpha = Alpha(1, [0] * (self.generator_degree + 1))
        alpha.set_array_value(1, 1)
        self.field.clear()
        alpha.get_value()[-1] = constant_term
        self.field.extend([one, alpha])
        constant_term += 1
        previous_alpha_degree = alpha

        for degree in range(2, self.size):
            new_alpha = Alpha(degree, multiply_stolbik(alpha(), previous_alpha_degree(), self.z_value))
            while len(new_alpha()) != len(alpha()):
                new_alpha().pop(0)

            while new_alpha.get_value()[0] != 0:
                new_alpha = Alpha(degree, self.sub(new_alpha, Alpha(None, self.generator)))
            self.field.append(new_alpha)
            if new_alpha.is_one():
                break

            previous_alpha_degree = new_alpha

        print('Field:')
        for el in self.field:
            print(el)

        print(f'Order = {degree}')

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
        """
        Adds two Alpha objects and returns the result.

        Args:
            alpha1 (Alpha): The first Alpha object to be added.
            alpha2 (Alpha): The second Alpha object to be added.

        Returns:
            Alpha: The result of adding alpha1 and alpha2.
        Raises:
            ValueError: If the result is not found in the field.
        """
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
        """
        Calculate the product of two Alpha objects.

        Args:
            alpha1 (Alpha): The first Alpha object.
            alpha2 (Alpha): The second Alpha object.

        Returns:
            Alpha: The product of the two Alpha objects.
        """
        if alpha1.degree is None or alpha2.degree is None:
            return Alpha(None, [])
        power = (alpha1.degree + alpha2.degree) % (self.size - 1)
        if power == 0:
            return self.get_alpha(0)
        return self.get_alpha(power)

    def power(self, alpha: Alpha, power: int):
        """
        Calculate the power of the given alpha to the specified exponent.

        Args:
            alpha (Alpha): The alpha value to be raised to a power.
            power (int): The exponent to raise the alpha to.

        Returns:
            Alpha: The result of raising the alpha to the specified power.
        """
        power = alpha.degree * power % (self.size - 1)
        if power == 0:
            return self.get_alpha(0)
        return self.get_alpha(power)

    def sub(self, alpha1: Alpha, alpha2: Alpha):
        """
        Subtracts the elements of two Alpha objects and returns the resulting list.

        Args:
            alpha1: An instance of the Alpha class.
            alpha2: An instance of the Alpha class.

        Returns:
            list: A list of the differences between the elements of alpha1 and alpha2.
        """
        a1 = alpha1().copy()
        a2 = alpha2().copy()
        answer = []
        for i in range(len(a1)):
            value = a1[i] - a2[i]
            if value < 0:
                value = self.z_value + value
            answer.append(value)
        return answer

    def find_roots(self, polynomial_degrees):
        """
        Find the roots of the polynomial given its degrees in the field.

        Parameters:
            polynomial_degrees (list): A list of polynomial degrees.

        Returns:
            None
        """
        roots = []
        constant_term = self.get_alpha(polynomial_degrees[-1])
        for element in self.field:
            if not element.is_null():
                total = constant_term
                for index in range(len(polynomial_degrees) - 2, -1, -1):
                    alpha = self.get_alpha(polynomial_degrees[index])
                    term = self.mult(alpha, self.power(element, len(polynomial_degrees) - index - 1))
                    total = self.add(total, term)
                if total.is_null():
                    roots.append(element)
        print('Roots:')
        for root in roots:
            print(root)
