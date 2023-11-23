import Lectura
import Decodificador
import mapeoCamara

file_archive = "archivoPatron.xlsx"  # File name must be known
pattern, error = Lectura.leerPatron(file_archive)  # Pattern is the desire/final pattern for this method

# The current set comes from the "mapeo" function
# current_set = [
#    [100, None, 200, 300, 100],
#    [200, None, 100, 200, None],
#    [300, None, None, None, None],
#    [100, 100, 300, None, 100],
#    [None, None, 100, None, 300]
# ]
trash, current_set = mapeoCamara.mapeo()

# Now the entries for this method are the desire pattern and the actual pattern

# The ideas behind this method are:
# Step 1: Compare the patterns and find the objects that are correctly placed (to avoid them)
# Step 2: The other objects in "descarga" will be taken to "suministro" in the places should be in according
# to the pattern. This with the idea of placing everything in "suministro" and later take it to "descarga"
# This step is relevant, because this avoids overlaps that could happen in the reorganize of the objects
# Step 3: Take the objects to "descarga", and thanks to the previous step, the movements will be just lateral,
# because the currect row of each object is accurate.

class Reorganize:
    def __init__(self, pattern, currect_set):
        self.des_pattern = pattern  # Given pattern
        self.cur_pattern = currect_set  # Current distribution
        self.right_places = {}  # Cells that are correctly placed
        self.pattern_places = {}  # Positions of each object in pattern
        self.actual_places = {}  # Positions of each object in current distribution
        self.cells_to_move = {}  # Positions of object to be moved
        self.potential_to_supply = {}  # Positions that will be placed in supply before correcting them
        self.supply_positions = {}  # Positions corrected for supply matrix

    # This method looks for the places for each kind of object and if it's correctly placed
    def places(self):
        objects = [100, 200, 300]  # Possible objects for patterns
        positions_pattern = {obj: [] for obj in objects}
        positions_pattern[None] = []  # This is extra for None positions
        positions_actual = {obj: [] for obj in objects}
        positions_actual[None] = []  # This is extra for None positions
        correct_places = {obj: [] for obj in objects}

        for i in range(5):
            for j in range(5):
                cell_pattern = self.des_pattern[i][j]
                cell_actual = self.cur_pattern[i][j]
                # This part looks for correct placed object
                if cell_actual == cell_pattern and cell_actual is not None and cell_pattern is not None:
                    correct_places[cell_pattern].append((i, j))
                # This if/else looks for the positions of the current positions in "descarga"
                if cell_actual is not None:
                    positions_actual[cell_actual].append((i, j))
                else:
                    positions_actual[None].append((i, j))
                # This if/else looks for the positions in the given pattern
                if cell_pattern is not None:
                    positions_pattern[cell_pattern].append((i, j))
                else:
                    positions_pattern[None].append((i, j))

        self.right_places = correct_places
        self.actual_places = positions_actual
        self.pattern_places = positions_pattern


    # This function find the objects that have to be moved
    def to_move(self):
        objects = [100, 200, 300]  # Possible objects for patterns
        move_cells = {obj: [] for obj in objects}
        pattern_cells = {obj: [] for obj in objects}
        for obj_type in objects:
            for object_position in self.actual_places[obj_type]:
                if object_position not in self.right_places[obj_type]:
                    move_cells[obj_type].append(object_position)
        for obj_type in objects:
            for object_position in self.pattern_places[obj_type]:
                if object_position not in self.right_places[obj_type]:
                    pattern_cells[obj_type].append(object_position)

        self.cells_to_move = move_cells
        self.potential_to_supply = pattern_cells

    # This function calculates the places towards "suministro"
    def towards_supply(self):
        objects = [100, 200, 300]  # Possible objects for patterns
        supply_cells = {obj: [] for obj in objects}
        for obj_type in objects:
            for obj in self.potential_to_supply[obj_type]:
                new_x = obj[0] + 0
                new_y = obj[1] + 5
                supply_cells[obj_type].append((new_x, new_y))

        self.supply_positions = supply_cells

    # This function works for codifying the tuples nto numbers
    # This works for a vector of tuples, not for ditionaries. (Easier testing)
    def codify_to_numbers(self, vector_object):
        reference_matrix = [
            [6, 7, 8, 9, 10, 1, 2, 3, 4, 5],
            [16, 17, 18, 19, 20, 11, 12, 13, 14, 15],
            [26, 27, 28, 29, 30, 21, 22, 23, 24, 25],
            [36, 37, 38, 39, 40, 31, 32, 33, 34, 35],
            [46, 47, 48, 49, 50, 41, 42, 43, 44, 45]
        ]
        codified_numbers = []

        for tuple_obj in vector_object:
            row, column = tuple_obj
            if 0 <= row < 5 and 0 <= column < 10:
                number = reference_matrix[row][column]
                codified_numbers.append(number)

        return codified_numbers

    # This function combines the vectors of current_places, supply_positions and potential_to_supply (Final positions)
    # for each object, and puts the type of data in each case. This for testing and reviewing.

    def combine_vectors(self, vector1, vector2, type_of_data):

        if type_of_data not in [100, 200, 300]:
            raise ValueError("The type_of_data must be: 100, 200 or 300")

        global_vector = []
        for val1, val2 in zip(vector1, vector2):
            #  global_vector.append(type_of_data)
            # global_vector.append(val1)
            # global_vector.append(val2)
            completed_value = (val1, val2)
            global_vector.append(completed_value)

        return global_vector

    # This function combines all the 6 vectors for this method

    def final_vector(self, last_vector):
        final_vector_codified = []
        for vector in last_vector:
            final_vector_codified.extend(vector)

        return final_vector_codified

    # This last function unifies all the functions

    def reorganized_data(self):

        # Global calculations
        self.places()
        self.to_move()
        self.towards_supply()

        # This function combines the vectors of current_places, supply_positions and potential_to_supply (Final positions)

        # Work for object A (100)
        Aux_A_current = self.codify_to_numbers(self.cells_to_move[100])
        Aux_A_supply = self.codify_to_numbers(self.supply_positions[100])
        Aux_A_final = self.codify_to_numbers(self.potential_to_supply[100])
        A_part_1 = self.combine_vectors(Aux_A_current, Aux_A_supply, 100)
        A_part_2 = self.combine_vectors(Aux_A_supply, Aux_A_final, 100)

        # Work for object B (200)
        Aux_B_current = self.codify_to_numbers(self.cells_to_move[200])
        Aux_B_supply = self.codify_to_numbers(self.supply_positions[200])
        Aux_B_final = self.codify_to_numbers(self.potential_to_supply[200])
        B_part_1 = self.combine_vectors(Aux_B_current, Aux_B_supply, 200)
        B_part_2 = self.combine_vectors(Aux_B_supply, Aux_B_final, 200)

        # Work for object C (300)
        Aux_C_current = self.codify_to_numbers(self.cells_to_move[300])
        Aux_C_supply = self.codify_to_numbers(self.supply_positions[300])
        Aux_C_final = self.codify_to_numbers(self.potential_to_supply[300])
        C_part_1 = self.combine_vectors(Aux_C_current, Aux_C_supply, 300)
        C_part_2 = self.combine_vectors(Aux_C_supply, Aux_C_final, 300)

        # Final combination

        vector_mix = [A_part_1, B_part_1, C_part_1, A_part_2, B_part_2, C_part_2]

        final_vector_codified = self.final_vector(vector_mix)
        print(final_vector_codified)


        return final_vector_codified

# This function call_reorganize Class
def call_reorganize(pattern, file_archive):
    reorganize_data = Reorganize(pattern, file_archive)
    final_vector_return = reorganize_data.reorganized_data()
    print("patron")
    print(pattern)
    print("actual")
    print(file_archive)
    print("1000000000000000000000000")
    print(final_vector_return)
    final_vector_for_returning = Decodificador.traducirPosicionesPasos(final_vector_return)

    return final_vector_for_returning

# This function works for an external call, coming from other python archive
def external_call_reorganized_method():
    final_vector_transmit = call_reorganize(pattern, current_set)
    return final_vector_transmit

final_vector_transmit = call_reorganize(pattern, current_set)
print("The final vector to transmit is: ")
print(final_vector_transmit)

# final = external_call_reorganized_method()
# print(final)