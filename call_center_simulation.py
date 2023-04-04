import os
import random
import simpy
import numpy as np
from rich.console import Console


NUM_of_EMP = 10
AVG_SUPPORT = 5
CUSTOMER_INTERVAL = 2
SIMULATION_TIME = 120
console = Console()

customer_handled = 0


class CallCenter:

    def __init__(self, env, num_emp, avg_support):
        self.env = env
        self.staff = simpy.Resource(env, num_emp)
        self.avg_support = avg_support


    def support(self, customer):
        random_time = max(1, np.random.normal(self.avg_support, 4))
        yield self.env.timeout(random_time)
        console.log("Support finished for {} at {:.2f}".format(customer, self.env.now))


def customer(env, name, call_center):
    global customer_handled
    console.log("{} On waiting queue".format(name))
    with call_center.staff.request() as request:
        yield request
        console.log("Customer {} on call at {:.2f}".format(name, env.now))
        yield env.process(call_center.support(name))
        console.log("Customer {} left call at {:.2f}".format(name, env.now))
        customer_handled += 1


def setup(env, num_emp, avg_support, customer_interval):
    call_center = CallCenter(env, num_emp, avg_support)

    for i in range(1, 6):
        env.process(customer(env, i, call_center))

    while True:
        yield env.timeout(random.randint(customer_interval-1, customer_interval+1))
        i += 1
        env.process(customer(env, num_emp, call_center))


if __name__ == "__main__":
    console.log(os.system('figlet Call Simulation'))
    env = simpy.Environment()
    env.process(setup(env, NUM_of_EMP, AVG_SUPPORT, CUSTOMER_INTERVAL))
    env.run(until=SIMULATION_TIME)
    console.log("Cutomer handled : [bold blue]{}[/bold blue]".format(customer_handled))