import socket
import subprocess
import threading
import webbrowser
from django.conf import settings


def send_startup_broadcast(host: str, port: int) -> None:
    """Send a startup broadcast notification.

    If BROADCAST_WEBHOOK_URL is configured, this sends a POST to that webhook.
    Otherwise it sends a UDP broadcast packet on BROADCAST_PORT.
    """
    message = f"imageserver started at http://{host}:{port}"
    webhook_url = getattr(settings, "BROADCAST_WEBHOOK_URL", None)

    if webhook_url:
        try:
            import json
            from urllib import request

            payload = json.dumps({"message": message}).encode("utf-8")
            req = request.Request(
                webhook_url,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with request.urlopen(req, timeout=5) as response:
                response.read()
            print(f"Startup broadcast sent to webhook: {webhook_url}")
        except Exception as exc:
            print(f"Failed to send startup webhook broadcast: {exc}")
    else:
        broadcast_port = getattr(settings, "BROADCAST_PORT", 9999)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.sendto(message.encode("utf-8"), ("255.255.255.255", broadcast_port))
            print(f"Startup broadcast sent via UDP to 255.255.255.255:{broadcast_port}")
        except Exception as exc:
            print(f"Failed to send startup UDP broadcast: {exc}")


def launch_local_application(host: str, port: int) -> None:
    """Open a local app URL or run a local launch command when the server starts."""
    url = getattr(settings, "STARTUP_LAUNCH_URL", None)
    if url is None:
        url = f"http://{host}:{port}/"

    command = getattr(settings, "STARTUP_LAUNCH_COMMAND", None)

    print(f"Launch config: URL={url}, COMMAND={command}")

    def _launch() -> None:
        print("Launching application...")
        if url:
            try:
                import webbrowser
                result = webbrowser.open(url, new=2)
                print(f"Opened startup URL: {url} (result: {result})")
            except Exception as exc:
                print(f"Failed to open startup URL {url}: {exc}")

        if command:
            try:
                subprocess.Popen(command, shell=isinstance(command, str))
                print(f"Launched local startup command: {command}")
            except Exception as exc:
                print(f"Failed to launch startup command {command}: {exc}")

    # For debugging, launch synchronously first
    _launch()
    # threading.Timer(0.5, _launch).start()
