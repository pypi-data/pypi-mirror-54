import numpy as np
import matplotlib.pyplot as plt


class Trajectory:
    """
    Object that describes a trajectory. With functions for checking if the trajectory describes real diffusion,
    convenient plotting and calculations of diffusion coefficients.

    Parameters
    ----------
    pixel_width: float
        Defines the length one pixel corresponds to. This value will be used when calculating diffusion
        coefficients. Default is 1.

    Attributes
    ----------
    pixel_width
    particle_positions
    """

    def __init__(self, pixel_width=1):
        self._particle_positions = np.empty((0,), dtype=[('frame_index', np.int16), ('time', np.float32), ('integer_position', np.int16), ('refined_position', np.float32)])
        self._velocities = np.empty((0, 0), dtype=np.float32)
        self._time_steps = np.empty((0, 0), dtype=np.int16)
        self._position_steps = np.empty((0, 0), dtype=np.int16)
        self._pixel_width = pixel_width

    @property
    def pixel_width(self):
        """
        float:
            Defines the length one pixel corresponds to. This value will be used when calculating diffusion
            coefficients. Default is 1.
        """
        return self._pixel_width

    @pixel_width.setter
    def pixel_width(self, width):
        self._pixel_width = width

    @property
    def particle_positions(self):
        """
        np.array:
            Numpy array with all particle positions in the trajectory on the form `np.array((nParticles,), dtype=[('frame_index', np.int16),
            ('time', np.float32),('integer_position', np.int16), ('refined_position', np.float32)])`
        """
        return self._particle_positions

    def plot_trajectory(self, ax=None, **kwargs):
        """
        Plots the trajectory using the frame index and the refined particle position in pixels.

        ax: matplotlib axes instance
            The axes which you want the frames to plotted on. If none is provided a new instance will be created.
        **kwargs:
            Plot settings, any settings which can be used in matplotlib.pyplot.plot method.

        Returns
        -------
            matplotlib axes instance
                Returns the axes input argument or creates and returns a new instance of a matplotlib axes object.
        """
        if ax is None:
            ax = plt.axes()
        ax.plot(self._particle_positions['refined_position'], self._particle_positions['frame_index'], np.ones((1,)), **kwargs)
        return ax

    def plot_velocity_auto_correlation(self, ax=None, **kwargs):
        """
        Plots the particle velocity auto correlation function which can be used for examining if the trajectory
        describes free diffusion.

        ax: matplotlib axes instance
            The axes which you want the frames to plotted on. If none is provided a new instance will be created.
        **kwargs:
            Plot settings, any settings which can be used in matplotlib.pyplot.plot method.

        Returns
        -------
            matplotlib axes instance
                Returns the axes input argument or creates and returns a new instance of a matplotlib axes object.
        """
        if ax is None:
            ax = plt.axes()
        ax.acorr(self._velocities, **kwargs)
        return ax

    def calculate_mean_square_displacement_function(self):
        """
        Returns
        -------
            time: np.array
                The time corresponding to the mean squared displacements.

            msd: np.array
                The mean squared displacements of the trajectory.
        """

        mean_square_displacements = np.zeros((self.particle_positions['frame_index'][-1] - self.particle_positions['frame_index'][0] + 1,),
                                             dtype=[('msd', np.float32), ('nr_of_values', np.int16)])
        times = np.arange(0, self.particle_positions['frame_index'][-1] - self.particle_positions['frame_index'][0] + 1, dtype=np.float32) * self._calculate_time_step()


        for first_index, first_position in enumerate(self.particle_positions[:-1]):
            for second_index, second_position in enumerate(self.particle_positions[first_index + 1:]):
                index_difference = second_position['frame_index'] - first_position['frame_index']
                mean_square_displacements['msd'][index_difference] += ((second_position['refined_position'] - first_position['refined_position']) * self.pixel_width) ** 2
                mean_square_displacements['nr_of_values'][index_difference] += 1

        for index, msd in enumerate(mean_square_displacements):
            if mean_square_displacements['nr_of_values'][index] != 0:
                mean_square_displacements['msd'][index] = msd['msd'] / mean_square_displacements['nr_of_values'][index].astype(np.float32)

        non_zeros_indices = np.nonzero(mean_square_displacements['nr_of_values'])
        return times[non_zeros_indices], mean_square_displacements['msd'][non_zeros_indices]

    def _append_position(self, particle_position):
        self._particle_positions = np.append(self._particle_positions, particle_position)

    def _position_exists_in_trajectory(self, particle_position):
        for p in self._particle_positions:
            if np.array_equal(p, particle_position):
                return True

    def _calculate_particle_velocities(self):
        self._time_steps = np.diff(self._particle_positions['time'])
        self._position_steps = np.diff(self._particle_positions['refined_position'] * self.pixel_width)
        self._velocities = self._position_steps / self._time_steps

    @staticmethod
    def _remove_non_unique_values(array):
        return np.unique(array)

    @staticmethod
    def _sort_values_low_to_high(array):
        return np.sort(array)

    def _fit_straight_line_to_mean_square_displacement_function(self):
        times, mean_square_displacements = self.calculate_mean_square_displacement_function()
        polynomial_degree = 1
        polynomial_coefficients, covariance_matrix = np.polyfit(times, mean_square_displacements, polynomial_degree, cov=True)
        error_estimate = [np.sqrt(covariance_matrix[0, 0]), np.sqrt(covariance_matrix[1, 1])]
        return polynomial_coefficients, error_estimate

    def calculate_diffusion_coefficient_from_velocity(self):
        """
        TODO: remove
        """
        diffusion_coefficient_velocity = 0
        for index, velocity in enumerate(self._velocities):
            diffusion_coefficient_velocity += velocity ** 2 * self._time_steps[index] / 4
        return diffusion_coefficient_velocity / len(self._velocities)

    def calculate_diffusion_coefficient_from_mean_square_displacement_function(self):
        """
        Fits a straight line to the mean square displacement function and calculates the diffusion coefficient from the
        gradient of the line. The mean squared displacement of the particle position is proportional to :math:`2Dt`
        where :math:`D` is the diffusion coefficient and :math:`t` is the time.

        Returns
        -------
            diffusion_coefficient: float
                todo
            error: float
                todo
        """
        polynomial_coefficients, error_estimate = self._fit_straight_line_to_mean_square_displacement_function()
        return polynomial_coefficients[0] / 2, error_estimate[0] / 2

    def calculate_diffusion_coefficient_using_covariance_based_estimator(self):
        """
        Unbiased estimator of the diffusion coefficient. More info at `https://www.nature.com/articles/nmeth.2904`

        Returns
        -------
            diffusion_coefficient: float
        """
        displacements = []
        time_step = self._calculate_time_step()
        for index, first_position in enumerate(self._particle_positions[:-1]):
            for second_position in self._particle_positions[index + 1:]:
                if second_position['frame_index'] - first_position['frame_index'] == 1:
                    displacements.append((second_position['refined_position'] - first_position['refined_position']) * self.pixel_width)
        displacements = np.array(displacements, dtype=np.float32)
        mean_squared_displacements = np.mean(displacements ** 2)
        mean_first_order_correlation = np.mean(displacements[:-1] * displacements[1:])
        return mean_squared_displacements / (2 * time_step) + mean_first_order_correlation / time_step

    def _calculate_time_step(self):
        return (self.particle_positions['time'][1] - self.particle_positions['time'][0]) / (self.particle_positions['frame_index'][1] - self.particle_positions['frame_index'][0])

    def calculate_number_of_missing_data_points(self):
        """
        Calculates the number of frames which the particle is not found in.

        Returns
        -------
            number: int
        """
        return int((self._particle_positions['frame_index'][-1] - self._particle_positions['frame_index'][0]) - self._particle_positions['frame_index'].shape[0] + 1)

    def calculate_number_of_particle_positions_with_single_time_step_between(self):
        """
        Calculates how many times in the trajectory the particle position in found in consecutive frames..

        Returns
        -------
            number: int
        """
        return int(np.sum([diff == 1 for diff in np.diff(self._particle_positions['frame_index'])]))
