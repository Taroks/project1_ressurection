import socket, select, sys 

with socket.socket (socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(('0.0.0.0', 8080))
    server.setblocking(0)
    server.listen(5)
    inputs = [server]
    outputs =[]

    while server:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        for s in readable:
            if s is server:
                conn, addr = s.accept()
                print('пришло подключение от;', addr)
                conn.setblocking(0)
                inputs.append(conn)
            else:
                try:
                    data = s.recv(1024)
                except socket.error as ex:
                    print('Ваше подключение использует протокол, отличный от TCP, то есть:', ex)
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

        for s in writable:
            s.send(data)
            outputs.remove(s)
            

        for s in exceptional:
            # s.sendall(pr)
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            
