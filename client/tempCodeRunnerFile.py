data_length_in_bytes = recv_all(BYTES)
    data_length_int = int.from_bytes(data_length_in_bytes, 'big')

    data = recv_all(data_length_int)