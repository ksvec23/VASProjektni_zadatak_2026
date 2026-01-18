import spade
import asyncio
import random
from spade.message import Message
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from config import WORLD_SIZE, INFECTION_PROBABILITY, INCUBATION_DAYS, RECOVERY_DAYS, MORTALITY_RATE

class HealthState:
    susceptible = "Podložan"
    exposed = "Izložen"
    infected = "Zaražen"
    recovered = "Ozdravio"
    dead = "Preminuo"

class agentPerson(spade.agent.Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.state = HealthState.susceptible
        self.days = 0
        self.x = random.randint(0, WORLD_SIZE - 1)
        self.y = random.randint(0, WORLD_SIZE - 1)
        self.can_move = True
        self.quarantined = False

    async def setup(self):
        print(f"{self.jid},{self.x},{self.y},{self.state}")
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(self.LifeBehaviour(), template)

    class LifeBehaviour(CyclicBehaviour):
        async def run(self):
            agent = self.agent

            # šalji stanje vizualizaciji
            msg_viz = Message(to="visual@127.0.0.1")
            msg_viz.body = f"{agent.jid},{agent.x},{agent.y},{agent.state}"
            msg_viz.set_metadata("performative", "inform")
            await self.send(msg_viz)

            # šalji stanje okolini
            msg_env = Message(to="env@127.0.0.1")
            msg_env.body = f"POS,{agent.jid},{agent.x},{agent.y},{agent.state}"
            msg_env.set_metadata("performative", "inform")
            await self.send(msg_env)

            # primi poruke
            msg = await self.receive(timeout=0.1)
            if msg:
                await self.handle_message(msg)

            
            if agent.state not in [HealthState.dead, HealthState.recovered]:
                self.progress_disease()
                self.move()

            await asyncio.sleep(1)  

        async def handle_message(self, msg):
            agent = self.agent
            if msg.body == "INFECT" and agent.state == HealthState.susceptible:
                if random.random() < INFECTION_PROBABILITY:
                    agent.state = HealthState.exposed
                    agent.days = 0
                    print(f"[INFO] {agent.jid} postao ZARAŽEN!!")

            elif msg.body == "LOCKDOWN":
                agent.can_move = False
                print(f"[INFO] {agent.jid} LOCKDOWN")

            elif msg.body == "VACCINATE" and agent.state == HealthState.susceptible:
                agent.state = HealthState.recovered
                print(f"[INFO] {agent.jid} CIJEPLJEN")

        def progress_disease(self):
            agent = self.agent
            if agent.state in [HealthState.exposed, HealthState.infected]:
                agent.days += 1

            
            if agent.state == HealthState.exposed and agent.days >= INCUBATION_DAYS:
                agent.state = HealthState.infected
                agent.days = 0
                print(f"[INFO] {agent.jid} IMA SIMPTOME")

            
            elif agent.state == HealthState.infected and agent.days >= RECOVERY_DAYS:
                if random.random() < MORTALITY_RATE:
                    agent.state = HealthState.dead
                else:
                    agent.state = HealthState.recovered
                print(f"[INFO] {agent.jid} OPORAVIO SE / PREMINUO")

        def move(self):
            agent = self.agent
            if agent.can_move and not agent.quarantined and agent.state not in [HealthState.dead, HealthState.recovered]:
                agent.x = max(0, min(WORLD_SIZE - 1, agent.x + random.randint(-2, 2)))
                agent.y = max(0, min(WORLD_SIZE - 1, agent.y + random.randint(-2, 2)))
