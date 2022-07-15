from datetime import datetime, timedelta
from pip import main
import pybgpstream


class BgpBlackVTFront():
    def __init__(self,
                 from_time=None,
                 until_time=None,
                 data_interface=None,
                 project=None,
                 projects=None,
                 collector=None,
                 collectors=None,
                 record_type=None,
                 record_types=None,
                 filter=None
    ):
        self.from_time = from_time
        self.until_time = until_time
        self.data_interface = data_interface
        self.project = project
        self.projects = projects
        self.collector = collector
        self.collectors = collectors
        self.record_type = record_type
        self.record_types = record_types
        self.filter = f"{filter} community 20473:18 3356:100 29632:65446 20473:4000 3356:3 3356:2011 3356:901 3356:575 3356:22 3356:123"

    def display(self):

        # Set threshold time
        threshold = {
            "day": 0,
            "hour": 0,
            "minute": 0,
            "second": 0
        }

        # BGPStream Object
        stream = pybgpstream.BGPStream(
            from_time=self.from_time,
            until_time=self.until_time,
            data_interface=self.data_interface,
            project=self.project,
            projects=self.projects,
            collector=self.collector,
            collectors=self.collectors,
            record_type=self.record_type,
            record_types=self.record_types,
            filter=self.filter
        )

        # Extracting BGPStream data
        for index, element in enumerate(stream):
            data = str(element).split("|")

            date_time = datetime.fromtimestamp(float(data[2])).strftime("%Y-%m-%d %H:%M:%S")

            record = {
                "aaa": data[0],
                "bbb": data[1],
                "timestamp": datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S"),
                "ddd": data[3],
                "eee": data[4],
                "collector": data[5],
                "ggg": data[6],
                "hhh": data[7],
                "iii": data[8],
                "nlri": data[9],
                "kkk": data[10],
                "lll": data[11],
                "mmm": data[12],
                "nnn": data[13],
                "ooo": data[14]
            }

            if index == 0:
                start_time = record["timestamp"]
                end_time = start_time + timedelta(days=threshold["day"],hours=threshold["hour"], minutes=threshold["minute"], seconds=threshold["second"])

            if record["timestamp"] < start_time:
                continue

            if record["timestamp"] >= start_time and record["timestamp"] <= end_time:
                # First Graph
                data_dict["first_graph"].append(record)

                # Second Graph
                if record["nlri"][-3:] == "/12":
                    data_dict["second_graph"]["12"].append(record)

                elif record["nlri"][-3:] == "/24":
                    data_dict["second_graph"]["24"].append(record)

                # Second and Fourth Graph
                elif record["nlri"][-3:] == "/32":
                    data_dict["second_graph"]["32"].append(record)
                    data_dict["fourth_graph"].append(record)

                # Third Graph
                elif record["nlri"][-3:] == "/36":
                    data_dict["third_graph"]["36"].append(record)

                elif record["nlri"][-3:] == "/40":
                    data_dict["third_graph"]["40"].append(record)

                elif record["nlri"][-3:] == "/48":
                    data_dict["third_graph"]["48"].append(record)

                table_data = record.copy()
                table_data["timestamp"] = table_data["timestamp"].strftime('%Y/%m/%d %H:%M:%S')

                data_dict["table_data"].append(table_data)
            
            else:
                response = dict()
                response["date_range"] = f"{start_time.strftime('%Y/%m/%d %H:%M:%S')}-{end_time.strftime('%Y/%m/%d %H:%M:%S')}"

                response["data"] = {
                    "first_graph": {
                        "total": len(data_dict["first_graph"]),
                        "distinct": len(set(tuple(d.items()) for d in data_dict["first_graph"]))
                    },
                    "second_graph": [
                        {
                            "x": "12",
                            "y": len(data_dict["second_graph"]["12"])
                        },
                        {
                            "x": "24",
                            "y": len(data_dict["second_graph"]["24"])
                        },
                        {
                            "x": "32",
                            "y": len(data_dict["second_graph"]["32"])
                        }
                    ],
                    "third_graph": [
                        {
                            "x": "36",
                            "y": len(data_dict["third_graph"]["36"])
                        },
                        {
                            "x": "40",
                            "y": len(data_dict["third_graph"]["40"])
                        },
                        {
                            "x": "48",
                            "y": len(data_dict["third_graph"]["48"])
                        }
                    ],
                    "fourth_graph": {
                        "total": len(data_dict["fourth_graph"]),
                        "distinct": len(set(tuple(d.items()) for d in data_dict["fourth_graph"]))
                    },
                    "table_data": data_dict["table_data"]
                }
                
                print("**************************************************")
                print(response)
                print("**************************************************")
                
                data_dict = {
                    "first_graph": list(),
                    "second_graph": {
                        "12": list(),
                        "24": list(),
                        "32": list()
                    },
                    "third_graph":{
                        "36": list(),
                        "40": list(),
                        "48": list()
                    },
                    "fourth_graph": list(),
                    "table_data": list()
                }
