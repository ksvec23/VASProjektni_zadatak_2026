import spade
import asyncio
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
from config import POPULATION_SIZE, LOCKDOWN_THRESHOLD
from agentOsoba import HealthState

class agentPolicy(spade.agent.Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.day = 0

    async def setup(self):
        print("[POLICY] Agent započeo.")
        template = Template()
        template.set_metadata("performative", "inform")
        self.add_behaviour(self.PolicyBehaviour(), template)

    class PolicyBehaviour(CyclicBehaviour):
        async def run(self):
            agent = self.agent
            agent.day += 1

            for i in range(POPULATION_SIZE):
                target_jid = f"agent{i}@127.0.0.1"

                infected_count = await self.count_infected()
                if infected_count > LOCKDOWN_THRESHOLD:
                    msg = Message(to=target_jid)
                    msg.body = "LOCKDOWN"
                    msg.set_metadata("performative", "inform")
                    await self.send(msg)    

            await asyncio.sleep(1)  

        async def count_infected(self):
           
            return 0
