import socket
import pandas

as_port = 53533
as_ip = "0.0.0.0"
as_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
as_socket.bind((as_ip, as_port))

csv_path = "./AS/dns_data.csv"
try:
    dns_data = pandas.read_csv(csv_path)
except:
    dns_data = pandas.DataFrame(columns={"TYPE", "NAME", "VALUE", "TTL"})

while True:
    message, client_add = as_socket.recvfrom(2048)
    message = message.decode()
    message = message.split('\n')
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
            d = pandas.DataFrame([[type, name, value, ttl]],columns=["TYPE", "NAME", "VALUE", "TTL"])
            dns_data = pandas.concat([dns_data, d], ignore_index=True).drop_duplicates(subset=['NAME'], keep='last')
            dns_data.to_csv(csv_path)

            as_socket.sendto("Success".encode(), client_add)
        except:
            as_socket.sendto("Failed".encode(), client_add)

    elif len(message) == 2:
        for data in message:
            data = data.split('=')
            if data[0] == "TYPE":
                type = data[1]
            elif data[0] == "NAME":
                name = data[1]
        value = dns_data.loc[dns_data["NAME"]==name, "VALUE"].array[0]
        ttl = dns_data.loc[dns_data["NAME"]==name, "TTL"].array[0]
        response = "TYPE={}\nNAME={}\nVALUE={}\nTTL={}".format(type, name, value, ttl)

        as_socket.sendto(response.encode(), client_add)


