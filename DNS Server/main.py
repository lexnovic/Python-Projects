from dnsserver import DNSServer

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    dns = DNSServer("localhost", 2053)
    dns.run()


if __name__ == "__main__":
    main()