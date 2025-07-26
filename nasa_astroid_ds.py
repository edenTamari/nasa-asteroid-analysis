import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

YEAR = '2000'

def load_data(file_name):
    """
    The function converts an Excel table into an array
    @param:
        file_mane (str): The name of the file to be opened
    @Returns:
        data (array): An array containing the data
    """
    try:
        data = np.genfromtxt(file_name, delimiter=',', dtype=str, encoding='utf-8')
        return data
    except Exception as err:
        print('Something went wrong:', err)

def scoping_data(data, names):
    """
    The function deletes from the DATA array the columns appearing in the NAMES list
    @param:
        data (array): An array containing the data
        names (list): A list of column names
    @Returns:
        updated_data (array): An array containing the data
    """
    try:
        if data.size == 0 or not names:
            return data

        header = data[0]
        # Find indices of columns to be removed
        indices_to_remove = [i for i, col_name in enumerate(header) if col_name in names]
        # Create a new data array without the specified columns
        updated_data = np.delete(data, indices_to_remove, axis=1)

        return updated_data
    except Exception as err:
        print('Something went wrong:', err)
        return data

def mask_data(data):
    """
    The function updates the DATA array so that only the asteroids whose
    approach date to the Earth is from the year 2000 appear
    @param:
        data (array): An array containing the data
    @Returns:
        masked_data (array): An array containing the data
    """
    try:
        if data is None or data.size == 0:
            return data

        # Find the index of the 'Close Approach Date' column
        header = data[0]
        close_approach_index = np.where(header == 'Close Approach Date')[0][0]

        # Create a boolean mask for dates from 2000 onwards
        mask = np.array([date >= '2000-01-01' for date in data[1:, close_approach_index]], dtype=bool)

        # Apply the mask to the data array (including the header)
        masked_data = np.vstack((header, data[1:][mask]))

        return masked_data
    except Exception as err:
        print('Something went wrong:', err)
        return data


def data_details(data):
    """
    The function will delete the following columns from the array: Neo Reference ID, Orbiting Body, Equinox
    @param:
        data (array): An array containing the data
    @Returns:
        void
    """

    names = ["Neo Reference ID", "Orbiting Body", "Equinox"]
    data = scoping_data(data, names)
    print(data[0])
    print("Number of Rows: ", data.shape[0], "\nNumber of Columns: ", data.shape[1])

def max_absolute_magnitude(data):
    """
    The function will check which asteroid has the maximum Absolute Magnitude
    @param:
        data (array): An array containing the data
    @Returns:
        tpl (tuple) : name, Absolute Magnitude
    """
    try:
        header = data[0]
        name_index = np.where(header == 'Name')[0][0]
        absolute_magnitude_index = np.where(header == 'Absolute Magnitude')[0][0]

        string_data = data[1:, absolute_magnitude_index]
        int_data = string_data.astype(float)
        max_absolute_magnitude = max(int_data)

        row_of_the_asteroid = np.where(data[1:, absolute_magnitude_index] == str(max_absolute_magnitude))
        name = str(data[row_of_the_asteroid[0] +1, name_index])
        new_name = get_name(name)
        tpl = tuple([new_name, max_absolute_magnitude])
        return tpl

    except Exception as err:
        print('Something went wrong:', err)


def closest_to_earth(data):
    """
    The function will check which asteroid is closest to Earth
    @param:
        data (array): An array containing the data
    @Returns:
        new_name (str) : astroid name
    """
    try:
        header = data[0]
        name_index = np.where(header == 'Name')[0][0]
        miss_dist_index = np.where(header == 'Miss Dist.(kilometers)')[0][0]

        string_data = data[1:, miss_dist_index]
        int_data = string_data.astype(float)
        nim_miss_dist = min(int_data)

        row_of_the_asteroid = np.where(data[1:, miss_dist_index] == str(nim_miss_dist))
        name = str(data[row_of_the_asteroid[0] + 1, name_index])
        new_name = get_name(name)
        return new_name

    except Exception as err:
        print('Something went wrong:', err)


def get_name(name):
    """
    The function Cleans the asteroid name from unnecessary characters
    @param:
        name (str): asteroid name
    @Returns:
        clean_name (str) : astroid name
    """
    clean_name = ""
    for letter in name:
        if letter.isdigit():
            clean_name += letter
    return clean_name


def common_orbit(data):
    """
    The function checks how many asteroids there are in each orbit
    @param:
        data (array): An array containing the data
    @Returns:
        dict_id (dict) : key: ID Orbit , value: The amount of asteroids
    """
    try:
        dict_id = dict()
        header = data[0]
        id_index = np.where(header == 'Orbit ID')[0][0]
        list_of_id = data[1:, id_index]

        for id in list_of_id:
            if id in dict_id:
                dict_id[id] += 1
            else:
                dict_id[id] = 1
        return dict_id

    except Exception as err:
        print('Something went wrong:', err)


def min_max_diameter(data):
    """
    The function calculates the average of Est Dia in KM(max) and the average of Est Dia in KM(min)
    @param:
        data (array): An array containing the data
    @Returns:
        tpl_diameter (tuple) : averages of Est Dia in KM(max) and KM(min)
    """
    try:
        int_min, int_max = get_diameter_col(data)

        avr_min = int_min.mean()
        avr_max = int_max.mean()

        tpl_diameter = tuple([avr_min, avr_max])
        return tpl_diameter

    except Exception as err:
        print('Something went wrong:', err)

def plt_hits_diameter(data):
    """
    Function creates a histogram graph showing the amount of asteroids according to their diameter
    @param:
        data (array): An array containing the data
    @Returns:
        viod
    """
    try:
        int_min, int_max = get_diameter_col(data)
        avg_np = np.zeros(len(int_min), dtype=float)
        for i in range(len(avg_np)):
            avg_np[i] = (int_min[i] + int_max[i])/2

        tpl_diameter = min_max_diameter(data)
        bins = np.linspace(tpl_diameter[0], tpl_diameter[1], 11)

        plt.hist(avg_np, bins=bins, color='steelblue', edgecolor='black')
        plt.title("Asteroid diameter histogram:")
        plt.xlabel('Average Diameter (km)')
        plt.ylabel('Number of Asteroids')
        plt.show()

    except Exception as err:
        print('Something went wrong:', err)

def get_diameter_col(data):
    """
    A function that creates a histogram graph showing the amount of asteroids according to their orbit
    @param:
        data (array): An array containing the data
    @Returns:
        viod
    """
    try:
        header = data[0]
        est_min = np.where(header == 'Est Dia in KM(min)')[0][0]
        est_max = np.where(header == 'Est Dia in KM(max)')[0][0]

        arr_min = data[1:, est_min]
        arr_max = data[1:, est_max]

        int_min = arr_min.astype(float)
        int_max = arr_max.astype(float)

        return int_min, int_max
    except Exception as err:
        print('Something went wrong:', err)

def plt_hist_common_orbit(data):
    """
    Function creates a pie graph showing the percentage of hazardous and non-hazardous asteroids
    @param:
        data (array): An array containing the data
    @Returns:
        viod
    """
    try:
        header = data[0]
        min_orbit_col = np.where(header == 'Orbit ID')[0][0]
        min_orbit = data[1:, min_orbit_col].astype(float)

        nim_val = min(min_orbit)
        max_val = max(min_orbit)

        bins = np.linspace(nim_val, max_val, 7)
        plt.hist(min_orbit, bins=bins, range=(nim_val,max_val), color='steelblue', edgecolor='black')
        plt.title("Histogram of Asteroids by Minimum Orbit Intersection")
        plt.xlabel('Minimum Orbit Intersection')
        plt.ylabel('Number of Asteroids')
        plt.show()

    except Exception as err:
        print('Something went wrong:', err)
    return

def plt_pie_hazard(data):
    """
    Function creates a pie graph showing the percentage of hazardous and non-hazardous asteroids
    @param:
        data (array): An array containing the data
    @Returns:
        viod
    """
    try:
        header = data[0]
        hazardous_col = np.where(header == 'Hazardous')[0][0]
        arr_hazardous = data[1:, hazardous_col]
        true_count, false_count = 0, 0
        for bool in arr_hazardous:
            if bool == 'True':
                true_count += 1
            else:
                false_count += 1

        sizes = [true_count, false_count]
        colors = ['red', 'green']
        labels = ['Dangerous asteroids', 'Harmless asteroids']

        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
        plt.title('Pie Chart of dangerous and not dangerous asteroids:')
        plt.show()
    except Exception as err:
        print('Something went wrong:', err)

def plt_liner_motion_magnitude(data):
    """
    This function accepts a data array, checks whether there is a linear relationship
    between the maximum proximity Absolute Magnitude of each asteroid and its speed
    of movement (Miles per hour), and displays a simple linear regression graph.
    Additionally, it explains the correlation between these two variables.

    Note:
    The correlation between Absolute Magnitude and Speed of movement (mph) indicates
    the strength and direction of a linear relationship between these two variables:

    - A positive correlation means that as the Absolute Magnitude of an asteroid increases,
      its speed tends to increase as well.
    - A negative correlation means that as the Absolute Magnitude increases, the speed tends to decrease.
    - A correlation coefficient (r) close to 1 or -1 indicates a strong linear relationship,
      while an r close to 0 indicates a weak or no linear relationship.
    - The R-squared value indicates the proportion of variance in the speed that is predictable
      from the Absolute Magnitude. An R-squared value close to 1 means a high proportion of
      variance is explained by the model, whereas a value close to 0 means little variance is explained.
    @param:
        data (array): An array containing the data
    @Returns:
        viod
    """
    try:
        header = data[0]
        abm_index = np.where(header == 'Absolute Magnitude')[0][0]
        mph_index = np.where(header == 'Miles per hour')[0][0]

        arr_x_abm = data[1:, abm_index].astype(float)
        mph_y_abm = data[1:, mph_index].astype(float)

        a, b, r_value, p_value, std_err = stats.linregress(arr_x_abm, mph_y_abm)
        if p_value < 0.05:
            plt.scatter(arr_x_abm, mph_y_abm)
            plt.plot(arr_x_abm, a * arr_x_abm + b, color='black')
            plt.title('linear regression between Absolute Magnitude and Miles per hour')
            plt.legend(['Data points', 'Fitted line'])
            plt.xlabel('Absolute Magnitude')
            plt.ylabel('Miles per hour')
            plt.show()
        else:
            print('NO linear regression')

    except Exception as err:
        print('Something went wrong:', err)


def main():
    data = load_data('nasa.csv')

    plt_hits_diameter(data)
    plt_hist_common_orbit(data)
    plt_pie_hazard(data)
    plt_liner_motion_magnitude(data)


if __name__ == "__main__":
    main()
