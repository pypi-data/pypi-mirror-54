import random
import sys
import typing
from multiprocessing import Event, Process

import uvicorn
from starlette.testclient import TestClient

if typing.TYPE_CHECKING:  # pragma: no cover
    from .applications import App

try:
    import pytest
except ImportError:  # pragma: no cover
    pytest = None


def create_client(app: "App", **kwargs) -> TestClient:
    """Create a [Starlette Test Client][client] out of an application.

    [client]: https://www.starlette.io/testclient/

    # Parameters
    app: an #::bocadillo.applications#App instance.
    **kwargs (any): keyword arguments passed to the `TestClient` constructor.

    # Returns
    client (TestClient): a Starlette test client.
    """
    return TestClient(app, **kwargs)


class ServerURL(str):
    def __call__(self, path: str) -> str:
        return self + path


class LiveServer:
    """Context manager to spin up a live uvicorn server in a separate process.

    The server process is terminated when exiting the context.

    # Parameters
    app: an #::bocadillo.applications#App instance.
    ready_timeout (float):
        The maximum time to wait for the live server to be ready to handle
        connections, in seconds.
        Defaults to 5.
    stop_timeout (float):
        The maximum time to wait for the live server to terminate, in seconds.
        Defaults to 5.
    **kwargs (any):
        keyword arguments passed to `uvicorn.run()`.
        `host` defaults to `"127.0.0.1."` (i.e. `localhost`).
        `port` defaults to a random integer between 3000 and 9999.
    
    # Attributes
    url (str):
        the full URL where the server lives.
        Build a full URL by calling this attribute,
        e.g. `server.url("/path/foo")`.
    """

    def __init__(
        self,
        app: "App",
        ready_timeout: float = 5,
        stop_timeout: float = 5,
        **kwargs,
    ):
        kwargs.setdefault("host", "127.0.0.1")
        kwargs.setdefault("port", random.randint(3000, 9999))

        self.app = app
        self.kwargs = kwargs
        self.ready_timeout = ready_timeout
        self.stop_timeout = stop_timeout
        self._process: Process = None
        self._ready: Event = None

    @property
    def url(self) -> ServerURL:
        host = self.kwargs["host"]
        port = self.kwargs["port"]
        return ServerURL(f"http://{host}:{port}")

    async def callback_notify(self):
        # Run periodically by the Uvicorn server.
        self._ready.set()

    def __enter__(self):
        if pytest is not None and sys.version_info >= (3, 8):
            pytest.skip("LiveServer fails on 3.8")

        self._ready = Event()
        self._process = Process(
            target=uvicorn.run,
            args=(self.app,),
            kwargs={"callback_notify": self.callback_notify, **self.kwargs},
        )
        self._process.start()

        if not self._ready.wait(self.ready_timeout):  # pragma: no cover
            raise TimeoutError(
                f"Live server not ready after {self.ready_timeout} seconds"
            )

        return self

    def __exit__(self, *args):
        self._process.terminate()
        self._process.join(self.stop_timeout)
        if self._process.exitcode is None:  # pragma: no cover
            raise TimeoutError(
                f"Live server still running after {self.stop_timeout} seconds."
            )
