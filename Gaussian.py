import math
# import matplotlib.pyplot as plt


class Gaussian():
    """ Gaussian distribution class for calculating and 
    visualizing a Gaussian distribution.

    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats extracted from the data file

    """

    def __init__(self, mu=0, sigma=1):

        self.mean = mu
        self.stdev = sigma

    def read_data_file(self, file_name, sample=True):
        with open(file_name) as file:
            data_list = []
            my_read = file.readlines()
            for item in my_read:
                data_list.append(int(item))
        return data_list

    def calculate_mean(self, data):
        self.mean = 1.0 * sum(data) / len(data)
        return self.mean

    def calculate_stdev(self, data, sample=True):
        n = len(data) - 1 if sample else len(data)
        mean = self.mean
        sigma = sum([((d - mean)**2) for d in data])
        sigma = math.sqrt(sigma / n)
        self.stdev = sigma

        return self.stdev

    def stat_pdf(self, data, mean, stdev, n_spaces=50):
        min_range = min(data)
        max_range = max(data)
        # calculates the interval between x values
        interval = 1.0 * (max_range - min_range) / n_spaces
        x = []
        y = []

        # calculate the x values to visualize
        for i in range(n_spaces):
            tmp = min_range + interval*i
            tmp_pdf = (1.0 / (stdev * math.sqrt(2*math.pi))) * \
                math.exp(-0.5*((tmp - mean) / stdev) ** 2)
            x.append(tmp)
            y.append(tmp_pdf)

        return x, y

    # def normal_dist(self, x, y):
    #     plt.plot(x, y)
    #     plt.title(
    #         'Normal Distribution for \n Sample Mean and Sample Standard Deviation')
    #     # x-axis label
    #     plt.xlabel('distance')
    #     plt.ylabel('Density')
    #     plt.show()

    # def histogram(self, data):
    #     plt.hist(data)
    #     plt.title('Histogram of Data')
    #     plt.xlabel('data')
    #     plt.ylabel('count')
    #     plt.show()

    def __add__(self, other):
        result = Gaussian()
        result.mean = self.mean + other.mean
        result.stdev = math.sqrt(self.stdev ** 2 + other.stdev ** 2)

        return result

    def __repr__(self):
        return f"mean {self.mean}, standard deviation {self.stdev}"