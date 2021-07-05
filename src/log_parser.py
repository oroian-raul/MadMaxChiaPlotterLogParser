import socket
import time

from data_exporter import DataExporter


class LogParser:

    def __init__(self, file_path: str, parser_name: str, parser_user: str, data_exporter: DataExporter):
        self.data_exporter = data_exporter
        self.file = open(file_path, 'r')
        self.parser_name = parser_name
        self.host_name = socket.gethostname()
        self.parser_user = parser_user
        self.start()

    def get_next_line(self):
        line = self.file.readline()[:-1]
        while len(line) == 0 or line is None:
            time.sleep(1)
            line = self.file.readline()[:-1]

        return line

    def export_settings(self):
        line = self.get_next_line()
        plotter_hash = line[line.rfind("-") + 2:-1]

        line = self.get_next_line()
        plotter_build = line[line.find("Build") + 6: line.find("for Windows") - 1]

        line = self.get_next_line()
        while "Number of Threads" not in line:
            line = self.get_next_line()

        threads = int(line[line.find(":") + 2:])

        line = self.get_next_line()
        p1_buckets = int(line[line.find("(") + 1:-2])

        line = self.get_next_line()
        p2_buckets = int(line[line.find("(") + 1:-2])

        self.data_exporter.export_settings(DataExporter.Settings(host_name=self.host_name,
                                                                 user_name=self.parser_user,
                                                                 parser_name=self.parser_name,
                                                                 plotter_hash=plotter_hash,
                                                                 plotter_build=plotter_build,
                                                                 threads=threads,
                                                                 p1_buckets=p1_buckets,
                                                                 p2_buckets=p2_buckets))

    def get_plot_name(self):
        line = self.get_next_line()
        while "Plot Name" not in line:
            line = self.get_next_line()

        return line[line.find(":") + 2:-1]

    def export_plot_stats(self):
        plot_name = self.get_plot_name()
        print(plot_name)

        line = self.get_next_line()
        while "Started copy" not in line:
            print(line)
            if line[0] == "[" and "max_table_size" not in line:
                phase = int(line[2])
                if phase != 4:
                    table_index_start = line.find("Table") + 6
                    table_index_end = line.find(" ", table_index_start)
                    table = int(line[table_index_start: table_index_end])

                    table_action = None
                    if phase == 2:
                        table_action = line[table_index_end + 1: line.find(" ", table_index_end + 1)]
                    elif phase == 3:
                        table_action = line[4]

                    duration_index_start = line.find("took", table_index_end) + 5
                    duration_index_end = line.find("sec") - 1
                    duration = float(line[duration_index_start: duration_index_end])
                    self.data_exporter.export_table_info(DataExporter.TableInfo(host_name=self.host_name,
                                                                                user_name=self.parser_user,
                                                                                parser_name=self.parser_name,
                                                                                phase=phase,
                                                                                table=table,
                                                                                table_action=table_action,
                                                                                duration=duration
                                                                                ))

            elif "Phase" in line:
                duration = float(line[line.find("took") + 5: line.find("sec")])
                self.data_exporter.export_phase_info(DataExporter.PhaseInfo(host_name=self.host_name,
                                                                            user_name=self.parser_user,
                                                                            parser_name=self.parser_name,
                                                                            phase=phase,
                                                                            duration=duration,

                                                                            ))
            elif "Total" in line:
                duration = float(line[line.find("was") + 4: line.find("sec")])
                self.data_exporter.export_plot_info(DataExporter.PlotInfo(host_name=self.host_name,
                                                                          user_name=self.parser_user,
                                                                          parser_name=self.parser_name,
                                                                          plot_name=plot_name,
                                                                          duration=duration
                                                                          ))
            line = self.get_next_line()

    def start(self):
        self.export_settings()

        while True:
            self.export_plot_stats()
