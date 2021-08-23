import socket, select, sys

def sending(s,data,outputs):
    s.send(data)
    outputs.remove(s)
    return outputs

def getting (s, server, exceptional, outputs, inputs):
    if s is server:
        conn, addr = s.accept()
        print('пришло подключение от;', addr[0])
        conn.setblocking(0)
        inputs.append(conn)
    else:
        try:
            data = s.recv(1024)
        except socket.error as ex:
            print('Входящее подключение использует протокол, отличный от TCP, то есть:', ex)
            str_ex = str(ex)
            pr = bytes(str_ex, 'utf-8')
            exceptional.append(s)
        else:
            if data:
                soobscheniya = open (f"{addr[0]}.txt","a")
                data_to_file = str(data)
                soobscheniya.write(data_to_file + '\n')
                soobscheniya.close()
                if s not in outputs:
                    outputs.append(s)
            else:
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
    return s, server, exceptional, outputs, inputs, data

    def expetpions (inputs, outputs):
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        return inputs, outputs