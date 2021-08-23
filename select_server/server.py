import socket, select, sys, queue, hashlib

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(('0.0.0.0', 8080))
    server.setblocking(0)
    server.listen(5)
    inp = [server]
    outp = []
    message_queue = {}

    while inp:
        readable, writable, exceptional = select.select(inp, outp, inp)
        for s in readable:
            if s is server:
                conn, addr = s.accept()
                conn.setblocking(0)
                inp.append(conn)
                message_queue [conn] = queue.Queue()
            else:
                data = s.recv(1024)
                if data:
                    soobscheniya = open (f'{addr[0]}.txt', 'a')
                    data_to_file = str(data) 
                    soobscheniya.write(data_to_file + '\n')
                    soobscheniya.close
                    message_queue[s].put(data)
                    if s not in outp:
                        outp.append(s)
                else:
                    if s in outp:
                        outp.remove(s)
                    inp.remove(s)
                    s.close()
                    del message_queue[s]
                    
        for s in writable:
            try:
                last_message = message_queue[s].get_nowait()
            except queue.Empty:
                outp.remove(s)
            else:
                s.send(last_message)

        for s in exceptional:
            inp.remove(s)
            if s in outp:
                outp.remove(s)
            s.close()
            del message_queue[s]
            


