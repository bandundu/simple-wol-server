# Python 3 wol server example

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os
import requests

# instead of os command https://pypi.org/project/wakeonlan/ can be used to send WOL Package
# from wakeonlan import send_magic_packet

hostName = <YourWOLServerHostname> # e.g. "192.168.0.135"
serverPort = <YourWOLServerPort> # e.g. 8565
macAdress = <YourTargetServerMacAdress> # e.g. "xx:xx:xx:xx:xx:xx"
domain <YoutTargetDomain> # e.g. "http://mycool.domain.com"
timeout = 120 # nr of seconds to wait untill resource is considered as timed out
timewait = 1 # seconds to wait between resource checks

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):

        # send WOL package
        os.system(f'wakeonlan {macAdress}')
        # instead of os command https://pypi.org/project/wakeonlan/ can be used to send WOL Package
        # send_magic_packet(macAdress)

        # wait for the resource to be available
        self.waitForResourceAvailable(domain,timeout,timewait)

        # redirect to desired domain
        self.send_response(301)
        self.send_header('Location', domain)

        # making sure that the browser does not serve from cache
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")

        self.end_headers()

    def waitForResourceAvailable(self, domain, timeout, timewait):
        timer = 0
        # check every "timewait" seconds wether domain is available
        while requests.get(domain).status_code == 502:
            print("Resource not available")
            time.sleep(timewait)
            timer += timewait
            if timer > timeout:
                print("Resource timeout")
                break
            if requests.get(domain).status_code == 200:
                print("Resource available")
                break


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started http://{hostName}:{serverPort}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
