from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import ASYNCHRONOUS
from data_exporter import DataExporter


class InfluxExporter(DataExporter):
    def __init__(self, database_address: str, bucket: str, org: str, token: str):
        self.db_client = InfluxDBClient(url=database_address, token=token, retries=0)
        self.write_api = self.db_client.write_api(write_options=ASYNCHRONOUS)
        self.bucket = bucket
        self.org = org

    def write(self, point):
        try:
            self.write_api.write(self.bucket, self.org, point)
        except Exception as e:
            print(str(e))

    def export_settings(self, data: DataExporter.Settings):
        point = Point("settings") \
            .tag("host_name", data.host_name) \
            .tag("user_name", data.user_name) \
            .tag("parser_name", data.parser_name) \
            .tag("plotter_hash", data.plotter_hash) \
            .tag("plotter_build", data.plotter_build) \
            .field("threads", data.threads) \
            .field("p1_buckets", data.p1_buckets) \
            .field("p2_buckets", data.p2_buckets) \
            .time(datetime.utcnow(), WritePrecision.NS)

        self.write(point)

    def export_table_info(self, data: DataExporter.TableInfo):
        point = Point("table_info") \
            .tag("host_name", data.host_name) \
            .tag("user_name", data.user_name) \
            .tag("parser_name", data.parser_name) \
            .tag("phase", data.phase) \
            .tag("table", data.table) \
            .tag("table_action", data.table_action) \
            .field("duration", data.duration) \
            .time(datetime.utcnow(), WritePrecision.NS)

        self.write(point)

    def export_phase_info(self, data: DataExporter.PhaseInfo):
        point = Point("phase_info") \
            .tag("host_name", data.host_name) \
            .tag("user_name", data.user_name) \
            .tag("parser_name", data.parser_name) \
            .tag("phase", data.phase) \
            .field("duration", data.duration) \
            .time(datetime.utcnow(), WritePrecision.NS)

        self.write(point)

    def export_plot_creation_info(self, data: DataExporter.PlotCreationInfo):
        point = Point("plot_info") \
            .tag("host_name", data.host_name) \
            .tag("user_name", data.user_name) \
            .tag("parser_name", data.parser_name) \
            .field("plot_name", data.plot_name) \
            .field("duration", data.duration) \
            .time(datetime.utcnow(), WritePrecision.NS)

        self.write(point)

    def export_plot_copy_info(self, data: DataExporter.PlotCopyInfo):
        point = Point("plot_copy_info") \
            .tag("host_name", data.host_name) \
            .tag("user_name", data.user_name) \
            .tag("parser_name", data.parser_name) \
            .tag("copy_success", data.copy_success) \
            .field("plot_name", data.plot_name) \
            .field("duration", data.duration) \
            .time(datetime.utcnow(), WritePrecision.NS)

        self.write(point)
