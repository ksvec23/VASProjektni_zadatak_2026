import pygame
import spade
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
from config import WORLD_SIZE
import asyncio

class agentVisualization(spade.agent.Agent):
    def __init__(self, jid, password):
        super().__init__(jid, password)
        pygame.init()
        self.cell_size = 20
        self.screen_width = WORLD_SIZE * self.cell_size
        self.screen_height = WORLD_SIZE * self.cell_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Simulacija epidemije")
        self.clock = pygame.time.Clock()
        self.agents = {}
        self.running = True

    async def setup(self):
        print("[VISUALIZATION] Agent započeo.")
        template = Template(metadata={"performative": "inform"})
        self.add_behaviour(self.ReceiveDrawBehaviour(), template)

    async def stop(self):
        self.running = False
        pygame.quit()
        await super().stop()

    class ReceiveDrawBehaviour(CyclicBehaviour):
        async def run(self):
            agent = self.agent
            msg = await self.receive(timeout=0.05)
            if msg:
                try:
                    parts = msg.body.split(",")
                    jid = parts[0]
                    x, y = int(parts[1]), int(parts[2])
                    state = parts[3]
                    agent.agents[jid] = (x, y, state)
                except:
                    pass

            agent.screen.fill((20, 20, 40))
            for jid, (x, y, state) in agent.agents.items():
                color = (100, 200, 255)  # susceptible
                if state == "Zaražen": color = (255, 50, 50)
                elif state == "Izložen": color = (255, 165, 0)
                elif state == "Ozdravio": color = (50, 255, 50)
                elif state == "Preminuo": color = (100, 100, 100)
                px = x * agent.cell_size + agent.cell_size // 2
                py = y * agent.cell_size + agent.cell_size // 2
                pygame.draw.circle(agent.screen, color, (px, py), agent.cell_size // 3)

            for i in range(0, agent.screen_width, agent.cell_size):
                pygame.draw.line(agent.screen, (50, 50, 50), (i, 0), (i, agent.screen_height))
            for i in range(0, agent.screen_height, agent.cell_size):
                pygame.draw.line(agent.screen, (50, 50, 50), (0, i), (agent.screen_width, i))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    agent.running = False
                    await agent.stop()

            pygame.display.flip()
            await asyncio.sleep(0.1)
