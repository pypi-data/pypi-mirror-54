import sciunit

#==============================================================================

class SomaReceivesStepCurrent(sciunit.Capability):
    """ Enables step current stimulus to soma """
    def inject_soma_square_current(self, current):
        """
        Input current is specified in the form of a dict with keys:
            'delay'     : (value in ms),
            'duration'  : (value in ms),
            'amplitude' : (value in nA)
        """
        raise NotImplementedError()

class SomaProducesMembranePotential(sciunit.Capability):
    """ Enables recording membrane potential from soma """
    def get_soma_membrane_potential(self, tstop):
        """
        Run simulation for time 'tstop' specified in ms,
        and must return a dict of the form:
            [ list1, list2 ]
            where,
                list1 = time series (in ms)
                list2 = membrane potential series (in mV)
        """
        raise NotImplementedError()

    def get_soma_membrane_potential_eFEL_format(self, tstop, start, stop):
        traces = self.get_soma_membrane_potential(tstop)
        efel_trace = {'T' : traces[0],
                      'V' : traces[1],
                      'stim_start' : [start],
                      'stim_end'   : [stop]}
        return efel_trace
