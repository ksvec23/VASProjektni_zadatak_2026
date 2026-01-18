import spade
import asyncio
import math
import random
from spade.message import Message
from spade.behaviour import CyclicBehaviour
from spade.template import Template
from config import INFECTION_RADIUS, INFECTION_PROBABILITY
from agentOsoba import HealthState

class agentEnvironment(spade.agent.Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.agent_positions = {}       
        self.last_infected = {}         
        self.simulation_day = 0         

    async def setup(self):
        print("[ENVIRONMENT] Agent započeo.")
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(self.EnvironmentBehaviour(), template)

    class EnvironmentBehaviour(CyclicBehaviour):
        async def run(self):
            agent = self.agent

            # pozicije svih agenata
            msg = await self.receive(timeout=0.1)
            if msg and msg.body.startswith("POS,"):
                parts = msg.body.split(",")
                jid = parts[1]
                x, y, state = int(parts[2]), int(parts[3]), parts[4]
                agent.agent_positions[jid] = (x, y, state)

            agent.simulation_day = int(asyncio.get_event_loop().time() // 1)
            self.check_infections()
            await asyncio.sleep(0.05)

        def check_infections(self):
            agent = self.agent
            positions = agent.agent_positions
            current_day = agent.simulation_day

            for infector_id, (ix, iy, istate) in positions.items():
                if istate != HealthState.infected:
                    continue

                for target_id, (tx, ty, tstate) in positions.items():
                    if target_id == infector_id:
                        continue

                    if tstate != HealthState.susceptible:
                        continue

                    last_day = agent.last_infected.get((infector_id, target_id), -1)
                    if last_day == current_day:
                        continue

                    distance = math.sqrt((ix - tx) ** 2 + (iy - ty) ** 2)
                    if distance <= INFECTION_RADIUS and random.random() < INFECTION_PROBABILITY:
                        msg = Message(to=target_id)
                        msg.body = "INFECT"
                        msg.set_metadata("performative", "inform")
                        asyncio.create_task(self.send(msg))
                        agent.last_infected[(infector_id, target_id)] = current_day
                        print(f"[ENV] {infector_id} je potencijalno ZARAZIO {target_id} (udaljenost={distance:.1f})")
