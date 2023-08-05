from cicada.analysis.cicada_analysis import CicadaAnalysis


class CicadaConnectivityGraph(CicadaAnalysis):
    def __init__(self):
        """
        A list of
        :param data_to_analyse: list of data_structure
        :param family_id: family_id indicated to which family of analysis this class belongs. If None, then
        the analysis is a family in its own.
        :param data_format: indicate the type of data structure. for NWB, NIX
        """
        super().__init__(name="connectivity graph", family_id="Connectivity",
                         short_description="Build connectivity graph")

    def check_data(self):
        """
        Check the data given one initiating the class and return True if the data given allows the analysis
        implemented, False otherwise.
        :return: a boolean
        """
        super().check_data()

        self.invalid_data_help = "Not implemented yet"
        return False

        if self._data_format != "nwb":
            # non NWB format compatibility not yet implemented
            return False

        return True

    def get_params_for_gui(self):
        return [{'name': 'range (ms)', 'type': int, 'range': [100, 1500], 'doc': 'Range for connectivity', 'default': 0},
            {'name': 'with graph', 'type': bool, 'doc': 'only count the cells that spikes', 'default': True}]

    def update_original_data(self):
        """
        To be called if the data to analyse should be updated after the analysis has been run.
        :return: boolean: return True if the data has been modified
        """
        pass

    def run_analysis(self, **kwargs):
        """
        test
        :param kwargs:
        :return:
        """

        for data in self._data_to_analyse:
            print(f"Connectivity ----- {data.identifier}")
