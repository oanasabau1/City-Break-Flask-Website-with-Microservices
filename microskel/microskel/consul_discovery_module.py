import threading
import time
from injector import Module, Binder, singleton
import consul
import random
from decouple import config
from microskel.service_discovery import ServiceDiscovery, HostAndPort
from microskel.log_call_module import log_call


class ConsulDiscovery(ServiceDiscovery):
    def __init__(self, app):
        self.app = app
        self.services = {}  # key = service_name; value = list of healthy endpoints
        self.consul_client = consul.Consul(host=config('CONSUL_HOST'), verify=False,
                                           port=config('CONSUL_PORT', cast=int))
        self.lock = threading.Lock()
        self.refresh_interval = config('REFRESH_INTERVAL', default=60, cast=int)  # seconds
        self.refresh_thread = threading.Thread(target=self._refresh_services, daemon=True)
        self.refresh_thread.start()

    @log_call
    def discover(self, service_name: str) -> HostAndPort:
        with self.lock:
            registrations = self.services.get(service_name)
        return random.choice(registrations) if registrations else self.do_discover(service_name)

    @log_call
    def do_discover(self, service_name: str) -> HostAndPort:
        with self.lock:
            self.services = self.consul_client.catalog.services()[1]
            if service_name not in self.services:
                self.app.logger.error(f'No registrations for {service_name}')
                return None
            healthy_services = self.consul_client.health.service(service=service_name, passing=True)
            registrations = [HostAndPort(entry['Service']['Address'], entry['Service']['Port'])
                             for entry in healthy_services[1]]
            self.services[service_name] = registrations
            return self.discover(service_name) if registrations else None

    def _refresh_services(self):
        while True:
            time.sleep(self.refresh_interval)
            with self.lock:
                for service_name in self.services.keys():
                    self.do_discover(service_name)


class ConsulDiscoveryModule(Module):
    def __init__(self, app):
        self.app = app

    def configure(self, binder: Binder) -> None:
        discovery = ConsulDiscovery(self.app)
        binder.bind(ServiceDiscovery, to=discovery, scope=singleton)


def configure_views(app):
    @app.route('/consul_catalog/<service_name>')
    def consul_catalog(service_name: str, service_discovery: ServiceDiscovery):
        registration: HostAndPort = service_discovery.discover(service_name)
        return registration.__dict__ if registration else f'No registration for {service_name}'