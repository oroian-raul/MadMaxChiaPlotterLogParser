from collections import namedtuple


class DataExporter:
    Settings = namedtuple("Settings",
                          ["host_name", "user_name", "parser_name",
                           "plotter_hash", "plotter_build", "threads", "p1_buckets", "p2_buckets"])

    PhaseInfo = namedtuple("PhaseInfo", ["host_name", "user_name", "parser_name",
                                         "phase", "duration"])

    TableInfo = namedtuple("TableInfo", ["host_name", "user_name", "parser_name",
                                         "phase", "table", "table_action", "duration"])

    PlotCreationInfo = namedtuple("TableInfo", ["host_name", "user_name", "parser_name",
                                                "plot_name", "duration"])

    PlotCopyInfo = namedtuple("TableInfo", ["host_name", "user_name", "parser_name",
                                            "plot_name", "duration"])

    def __init__(self, database_address: str, bucket: str, org: str, token: str):
        raise NotImplementedError('Not implemented')

    def export_settings(self, data: Settings):
        raise NotImplementedError('Not implemented')

    def export_table_info(self, data: TableInfo):
        raise NotImplementedError('Not implemented')

    def export_phase_info(self, data: PhaseInfo):
        raise NotImplementedError('Not implemented')

    def export_plot_creation_info(self, data: PlotCreationInfo):
        raise NotImplementedError('Not implemented')

    def export_plot_copy_info(self, data: PlotCopyInfo):
        raise NotImplementedError('Not implemented')
