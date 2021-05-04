from Inspect_Server.log_setting import logger
from socketserver import TCPServer, ThreadingMixIn, BaseRequestHandler

from Inspect_Server.settings import BUFSIZ
from Inspect_Server.inspect_test import getparsedate, checkbarcode, savetestdata


class Server(ThreadingMixIn, TCPServer):
    pass


class Handler(BaseRequestHandler):
    def handle(self):
        try:
            while True:
                data = self.request.recv(BUFSIZ)
                print("{} send:".format(self.client_address), data)
                logger.info(data)
                if not data:
                    print("connection lost:{}".format(self.client_address))
                    logger.info("connection lost：{}".format(self.client_address))
                    break
                parsedate = getparsedate(data)
                if isinstance(parsedate, Exception):
                    rtnstr = '请传入正确的JSON字符串'
                    logger.error(rtnstr)
                    self.request.sendall(rtnstr.encode('GBK'))
                    continue

                rtnstr = checkbarcode(parsedate)
                if rtnstr == 'OK':
                    rtnstr = savetestdata(parsedate)

                self.request.sendall(rtnstr.encode('GBK'))

        except Exception as e:
            logger.error(e)
            print(self.client_address, "连接断开")
        finally:
            self.request.close()

    def setup(self):
        print("before handle,连接建立：", self.client_address)
        logger.info("before handle,连接建立：{}".format(self.client_address))

    def finish(self):
        print("finish run  after handle")
        logger.info("finish run  after handle")
