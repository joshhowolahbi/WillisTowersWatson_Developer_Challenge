# Function to get the .txt data file and striping it of whitespaces
def get_data(data):
    """
    A function to read data while stripping it of whitespaces
    :param data: (string) name of .txt file to be read by the function
    :return: (list) every line in data
    """
    entry = []

    # reading file with the file name
    with open(data, 'r') as f:
        next(f)
        for line in f:
            entry.append(line.strip())
    f.close()

    # returns a list of each line in the file
    return entry


def clean_data(data):
    """
    A function to clean the data and splitting each string into
    type of product,origin year, development year, and the payment made
    :param data: (string) to be parsed into get_data function
    :return: (set) of product types from the whole data
             (set) of years from the whole data
             (list) products from each line
    """
    # Get striped data
    products = get_data(data)

    # initialize variables to hold a set of types of products
    # set of range of years both in origin and development years
    # list of entries from data including payments
    prod_type = set()
    year_range = set()
    prod = []

    # looping through each line of stripped data
    # splitting elements in each line separated by comma
    # adding elements in a list and appending to prod list above
    for line in products:
        product = line.split(",")[0]
        origin_year = int(line.split(",")[1])
        dev_year = int(line.split(",")[2])
        payment = float(line.split(",")[3])

        prod_type.add(product)
        year_range.add(origin_year)
        year_range.add(dev_year)
        prod.append([product, origin_year, dev_year, payment])

    # sorting year range
    years = sorted(year_range)

    # return cleaned and sorted data
    return prod_type, years, prod


def matrix(data):
    """
    A function to create a square matrix of the size required
    based on the data given
    :param data: (string) to be parsed into clean_data function
    :return: (int) the start year from the data,
             (int) the required matrix size
             (dict) A dictionary holding the matrices for each product type
    """
    # getting the returned data from clean_data()
    product_types, years, products = clean_data(data)

    # getting the start year and end year to compute matrix size
    start_yr = years[0]
    end_yr = years[-1]

    # deducing matrix size from year values
    mat_size = end_yr-start_yr+1

    # initializing a dictionary to hold matrix for each product type, having product type as key
    overall_mat = {}

    # initializing matrix values to zero for each product type and populating the above dictionary
    for product_type in product_types:
        triangle_matrix = [[0 for x in range(mat_size)] for y in range(mat_size)]
        overall_mat[product_type]= triangle_matrix

    # populating the values for each matrix point from the data provided
    for product in products:

        # getting which matrix to be populated
        product_matrix = overall_mat[product[0]]

        # getting the x and y points on the matrix, using the origin year and the development year
        x = product[1] - start_yr
        y = product[2] - product[1]

        # imputing the payment value in the x,y point of the matrix
        product_matrix[x][y]=product[3]

        # populating the compiled matrices for each product type to the dictionary
        overall_mat[product[0]]=product_matrix

    # returning the start year and matrix size and the overall matrices for each product for our output
    return start_yr, mat_size, overall_mat


def output_value(data):
    """
    A function to populate the output result
    :param data: (string) to be parsed into matrix function
    :return: (String) the output result
    """
    # getting the above returned data from the matrix function
    start_year, mat_size, matrices = matrix(data)

    # getting the desired output result
    out_result = f"{start_year}, {mat_size}\n"

    # looping through each matrix for each product and to get the cumulative value for rows in matrix
    for k, v in matrices.items():
        # appending the product type
        out = f"{k}"
        # determining the number of development years of cumulative values to add to out string
        for i in range(0, mat_size):
            # initialized cumulative value
            var = 0
            # to get the stopping point for each row in matrix corresponding to the development years
            for j in range(0, mat_size-i):
                # appending cumulative value to out string
                var += v[i][j]
                out += f", {var}"
        # appending out string to output result
        out_result += out + "\n"

    return out_result


def out_file(data, output):
    """
    A function to write the output result into a text file
    :param data: (string) to be parsed into output_value function
    :param output: (string) name of the output file
    :return: A .txt file having the output result
    """
    # getting output result
    result_file = output_value(data)

    with open(f"{output}.txt", 'w') as text_file:
        text_file.write(result_file)


if __name__ == '__main__':
    # to view output result in console
    print(output_value("Input_Data.txt"))

    # to write output result into a text file, uncomment below line
    # out_file("Input_Data.txt", "Output_file")
