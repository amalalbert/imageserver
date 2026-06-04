print("=== LOADING CUSTOM RUNSERVER COMMAND ===")

print("Loading custom runserver command!")

from django.core.management.commands.runserver import Command as RunserverCommand

from gallery.broadcast import launch_local_application, send_startup_broadcast


class Command(RunserverCommand):
    def inner_run(self, *args, **options):
        print("Custom inner_run called!")
        result = super().inner_run(*args, **options)
        print("Server startup complete, launching application...")
        # Get the server details
        host = self.addr or self.default_addr
        port = self.port
        send_startup_broadcast(host, port)
        print(f"Server started at http://{host}:{port}")
        launch_local_application(host, port)
        return result