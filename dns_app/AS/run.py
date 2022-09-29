import socket
import pandas

as_port = 53533
as_ip = "3.4.5.6"
as_socket = socket(socket.AF_INET, socket.SOCK_DGRAM)
as_socket.bind((as_ip, as_port))

csv_path = "./dns_data.csv"
dns_data = pandas.DataFrame(columns={"TYPE", "NAME", "VALUE", "TTL"}).set_index(['TYPE', 'NAME'])
"""set index"""


while True:
    message, client_add = as_socket.recvfrom(2048)
    message = message.decode()
    message = message.split('/n')
    if len(message)==4:
        try:
            for data in message:
                data = data.split('=')
                if data[0] == "TYPE":
                    type = data[1]
                elif data[0] == "NAME":
                    name = data[1]
                elif data[0] == "VALUE":
                    value = data[1]
                elif data[0] == "TTL":
                    ttl = data[1]
            dns_data.append({"TYPE": type, "NAME": name, "VALUE": value, "TTL": ttl})
            """check if already exists"""
            dns_data.to_csv(csv_path)
            as_socket.sendto("Success", client_add)
        except:
            as_socket.sendto("Failed", client_add)

    elif len(message) == 2:
        for data in message:
            data = data.split('=')
            if data[0] == "TYPE":
                type = data[1]
            elif data[0] == "NAME":
                name = data[1]
            if [type, name] in dns_data.index:
                value = dns_data[[type, name]]["VALUE"]
                ttl = dns_data[[type, name]]["TTL"]
            response = "TYPE={}\nNAME={}\nVALUE={}\nTTL={}\n".format(type, name, value, ttl)
            as_socket.sendto(response, client_add)


