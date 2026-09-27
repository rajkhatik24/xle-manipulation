from isaacsim import SimulationApp

simulation_app = SimulationApp({
    "headless": False
})

print("\n================================")
print("XLE PROJECT: ISAAC SIM WORKS!")
print("================================\n")

# Keep Isaac alive for a short test
for _ in range(300):
    simulation_app.update()

simulation_app.close()
