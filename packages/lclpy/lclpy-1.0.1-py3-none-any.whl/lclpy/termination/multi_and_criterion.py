from lclpy.termination.multi_criterion import MultiCriterion


class MultiAndCriterion(MultiCriterion):
    """Class to use multiple terminationcriteria at once.

    Parameters
    ----------
    criteria : list or tuple of AbstractTerminationCriterion
        An iterable object containing the intialised termination criterions one
        wishes to use.

    Attributes
    ----------
    criteria : list or tuple of AbstractTerminationCriterion
        An iterable object containing the intialised termination criterions one
        wishes to use.

    Examples
    --------
    3 termination criteria are used, three tests are done to ensure that all
    three criterions are capable of stopping the iterating correctly.

    MaxSecondsTerminationCriterion stops the iterating:

     .. doctest::

        >>> import time
        >>> from lclpy.termination.max_seconds_termination_criterion \\
        ...     import MaxSecondsTerminationCriterion
        >>> from lclpy.termination.max_iterations_termination_criterion \\
        ...     import MaxIterationsTerminationCriterion
        >>> from lclpy.termination.no_improvement_termination_criterion \\
        ...     import NoImprovementTerminationCriterion
        >>> from lclpy.termination.multi_and_criterion import MultiAndCriterion
        ... # init list
        >>> criteria = []
        >>> criteria.append(MaxSecondsTerminationCriterion(0))
        >>> criteria.append(MaxIterationsTerminationCriterion(0))
        >>> criteria.append(NoImprovementTerminationCriterion(3))
        ... # init MultiCriterion
        >>> multi_criterion = MultiAndCriterion(criteria)
        ... # test
        >>> start = time.time()
        >>> multi_criterion.start_timing()
        >>> while multi_criterion.keep_running():
        ...     multi_criterion.iteration_done()
        >>> stop = time.time()
        >>> time_passed = stop - start
        >>> time_passed < 4
        True


    MaxIterationsTerminationCriterion stops the iterating:

    .. doctest::

        >>> from lclpy.termination.max_seconds_termination_criterion \\
        ...     import MaxSecondsTerminationCriterion
        >>> from lclpy.termination.max_iterations_termination_criterion \\
        ...     import MaxIterationsTerminationCriterion
        >>> from lclpy.termination.no_improvement_termination_criterion \\
        ...     import NoImprovementTerminationCriterion
        >>> from lclpy.termination.multi_and_criterion import MultiAndCriterion
        ... # init list
        >>> criteria = []
        >>> criteria.append(MaxSecondsTerminationCriterion(0))
        >>> criteria.append(MaxIterationsTerminationCriterion(10))
        >>> criteria.append(NoImprovementTerminationCriterion(3))
        ... # init MultiCriterion
        >>> multi_criterion = MultiAndCriterion(criteria)
        ... # test
        >>> iterations = 0
        >>> values = [20, 19, 18, 20, 20, 20, 20, 13, 12, 11, 10, 9]
        >>> multi_criterion.start_timing()
        >>> while multi_criterion.keep_running():
        ...     multi_criterion.check_new_value(values[iterations])
        ...     iterations += 1
        ...     multi_criterion.iteration_done()
        >>> iterations
        10

    NoImprovementTerminationCriterion stops the iterating:

    .. doctest::

        >>> from lclpy.termination.max_seconds_termination_criterion \\
        ...     import MaxSecondsTerminationCriterion
        >>> from lclpy.termination.max_iterations_termination_criterion \\
        ...     import MaxIterationsTerminationCriterion
        >>> from lclpy.termination.no_improvement_termination_criterion \\
        ...     import NoImprovementTerminationCriterion
        >>> from lclpy.termination.multi_and_criterion import MultiAndCriterion
        ... # init list
        >>> criteria = []
        >>> criteria.append(MaxSecondsTerminationCriterion(0))
        >>> criteria.append(MaxIterationsTerminationCriterion(2))
        >>> criteria.append(NoImprovementTerminationCriterion(3))
        ... # init MultiCriterion
        >>> multi_criterion = MultiAndCriterion(criteria)
        ... # test 1
        >>> iterations = 0
        >>> values = [9, 8, 7, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        >>> multi_criterion.start_timing()
        >>> while multi_criterion.keep_running():
        ...     multi_criterion.check_new_value(values[iterations])
        ...     iterations += 1
        ...     multi_criterion.iteration_done()
        >>> iterations
        6

        """

    def keep_running(self):
        """function to determine if the algorithm needs to continue running.

        Returns
        -------
        bool
            The function returns true if the algorithm has to continue
            running, if the function returns false the algorithm needs to
            stop running. If all the composing termination criterions return
            False if their keep_running method is called, this method will
            return False. Else the method will return True.

        """

        for criterion in self.criteria:
            if criterion.keep_running() is True:
                return True
        return False
