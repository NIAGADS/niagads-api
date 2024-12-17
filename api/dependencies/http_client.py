from aiohttp import ClientSession
from aiohttp.connector import TCPConnector

class HttpClientSessionManager():
    """ Create Http connection pool and request a session """
    
    def __init__(self, baseUrl):
        self.__baseUrl = baseUrl
        self.__connector: TCPConnector = TCPConnector(limit=50)   
        self.__session: ClientSession = ClientSession(self.__baseUrl, connector=self.__connector, raise_for_status=True)
        
    async def close(self):
        if self.__session is not None:
            self.__session.close()
        if self.__connector is not None:
            self.__connector.close()
            
    async def __call__(self) -> ClientSession:
        if self.__session is None:
            raise Exception(f"HTTP client session manager for {self.__baseUrl} not initialized")
        return self.__session