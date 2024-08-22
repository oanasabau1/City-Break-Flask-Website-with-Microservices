from typing import List, Optional
import random

from decouple import config

from microskel.service_discovery import HostAndPort


class LoadBalancerStrategy:
    def select(self, services: List[HostAndPort]) -> Optional[HostAndPort]:
        raise NotImplementedError


class RoundRobin(LoadBalancerStrategy):
    def __init__(self):
        self.current_index = 0

    def select(self, services: List[HostAndPort]) -> Optional[HostAndPort]:
        if not services:
            return None
        service = services[self.current_index]
        self.current_index = (self.current_index + 1) % len(services)
        return service


class LeastConnections(LoadBalancerStrategy):
    def __init__(self):
        self.connections = {}

    def select(self, services: List[HostAndPort]) -> Optional[HostAndPort]:
        if not services:
            return None
        for service in services:
            if service not in self.connections:
                self.connections[service] = 0
        least_connected = min(services, key=lambda svc: self.connections.get(svc, 0))
        self.connections[least_connected] += 1
        return least_connected

    def release_connection(self, service: HostAndPort):
        if service in self.connections and self.connections[service] > 0:
            self.connections[service] -= 1


def get_load_balancer_strategy():
    strategy_name = config('LOAD_BALANCER_STRATEGY', default='round_robin')

    if strategy_name == 'least_connections':
        return LeastConnections()
    else:
        return RoundRobin()
