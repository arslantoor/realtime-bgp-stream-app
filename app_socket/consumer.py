import json
from datetime import datetime, timedelta
import pybgpstream
import asyncio
import random
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class BgpBlackVTFront(AsyncJsonWebsocketConsumer):
    async def connect(self, *args):
        self.project = "routeviews-stream"
        self.filter = "2914:420 2914:2000 16552:9100 16552:40014 2914:3000 2914:1011 16552:10500"
        self.room_name = self.scope["url_route"]["kwargs"]["user_id"]
        self.room_group_name = "user_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


    async def receive(self, text_data):
        text_data = json.loads(text_data)
        print("Recieved Message from Third Party Server --> ", text_data, type(text_data))

        # Set threshold time
        threshold = {
            "day": 0,
            "hour": 0,
            "minute": 0,
            "second": 0
        }

        # Data Dictionary
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

        # BGPStream Object
        stream = pybgpstream.BGPStream(
            # accessing routeview-stream
            project=text_data["project"],
            # filter to show only stream from amsix bmp stream
            filter=f"{text_data['filter']} community 20473:18 3356:100 29632:65446 20473:4000 3356:3 3356:2011 3356:901 3356:575 3356:22 3356:123",
        )
        
        print('*******************************')
        print('Object Created')
        print('*******************************')

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

            # print('***********************')
            # print("record --> ", record)
            # print('***********************')

            if index == 0:
                print("************************************** Loop Started **************************************")
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

                start_time = record["timestamp"]
                end_time = start_time + timedelta(days=threshold["day"],hours=threshold["hour"], minutes=threshold["minute"], seconds=threshold["second"])
                await self.send(json.dumps(response))
                await asyncio.sleep(random.random() * 2 + 1)


    async def send_parameter(self, event):
        print("Recieved method \t\t:", event)

        await self.send(text_data=json.dumps({
            "event": event,
        }))


    async def send_notification(self, event):
        user_id = event["user_id"]
        notification = event["notification"]
        notification_id = event["notification_id"]
        campaign_status = event["campaign_status"]
        campaign_id = event["campaign_id"]
        keyword_status = event["keyword_status"]
        keyword_id = event["keyword_id"]
        keyword_name = event["keyword_name"]
        campaign_name = event["campaign_name"]

        print("send_notification method call", campaign_name)
        print("campaign_status", campaign_status)
        new_data = {
            "notification": notification,
            "notification_id": notification_id,
            "user_id": user_id,
            "campaign_id": campaign_id,
            "campaign_status": campaign_status,
            "campaign_name": campaign_name,
        }
        # send message to webSocket
        await self.send(text_data=json.dumps({
            "notification": notification,
            "notification_id": notification_id,
            "user_id": user_id,
            "campaign_id": campaign_id,
            "campaign_status": campaign_status,
            "keyword_id": keyword_id,
            "keyword_status": keyword_status,
            "keyword_name": keyword_name,
            "campaign_name": campaign_name,
        }))
