from descrete_math import *

f = Field(3, [1, 1, 2])
f.build()
f.calculate_order()

f.find_roots([0, 6, 6, 4])

print(convert_to_another_system(69, 8))
