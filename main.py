import asyncio
import spade
from agentOsoba import agentPerson, HealthState
from agentOkolina import agentEnvironment
from agentSimulacija import agentVisualization
from agentPravila import agentPolicy
from config import POPULATION_SIZE, SIMULATION_TIME

async def main():
    print("\n=== POČETAK SIMULACIJE EPIDEMIJE ===\n")
    # agentOkolina
    environment = agentEnvironment("env@127.0.0.1", "password")
    await environment.start(auto_register=True)
    
    # agentSimulacija
    viz = agentVisualization("visual@127.0.0.1", "password")
    await viz.start(auto_register=True)
    
    # agentPravila
    policy = agentPolicy("policy@127.0.0.1", "password")
    await policy.start(auto_register=True)
    
    # agentOsoba
    person_agents = []
    for i in range(POPULATION_SIZE):
        agent = agentPerson(f"agent{i}@127.0.0.1", "password")
        await agent.start(auto_register=True)
        person_agents.append(agent)
    print(f"{POPULATION_SIZE} agenata aktivirano, simulacija uskoro započinje...")
    await asyncio.sleep(1)

    # postavljanje nultog pacijenta
    patient_zero = person_agents[0]
    patient_zero.state = HealthState.infected
    print(f" {patient_zero.jid} = PATIENT ZERO (EPIDEMIJA KREĆE!)\n")
    try:
        for day in range(1, SIMULATION_TIME + 1):
            infected = sum(1 for ag in person_agents if ag.state == HealthState.infected)
            exposed = sum(1 for ag in person_agents if ag.state == HealthState.exposed)
            print(f"[DAN {day}] Zaraženih: {infected}, Izloženih: {exposed}")

            if infected == 0 and exposed == 0:
                print("EPIDEMIJA ZAKLJUČENA!")
                break
            await asyncio.sleep(1)  

    except KeyboardInterrupt:
        print("\nSimulaciju prekinuo korisnik!")
    finally:
        print("\nZaustavljanje svih agenata!!")
        all_agents = person_agents + [viz, environment, policy]
        for agent in all_agents:
            try:
                await agent.stop()
            except Exception:
                pass
        print("\n=== SIMULACIJA ZAVRŠENA ===")

if __name__ == "__main__":
    spade.run(main())
