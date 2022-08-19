class ProxyManager:

    def parse_proxy_string(proxy_string):
        split_string = proxy_string.strip('\n').split(':')

        ip = split_string[0]
        port = split_string[1]
        proxy_string = f'{ip}:{port}'

        authenticated = len(split_string) == 4
        if authenticated:
            username = split_string[2]
            password = split_string[3]
            proxy_string = f'{username}:{password}@{proxy_string}'
        
        return proxy_string

    def load_queue(queue, proxy_file_path):
        with open(proxy_file_path) as proxy_file:
            for proxy_string in proxy_file.readlines():
                queue.put_nowait(proxy_string.strip('\n'))