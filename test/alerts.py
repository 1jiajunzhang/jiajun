from vpython import *
import numpy as np

# Constants
N = 4  # Grid size
k = 1
m = 1
spacing = 1
atom_radius = 0.3 * spacing
dt = 0.04 * (2 * np.pi * np.sqrt(m / k))

# Set up the scene
scene = canvas()
scene.center = vector(0.5 * (N - 1), 0.5 * (N - 1), 0.5 * (N - 1))
scene.caption = """A model of a solid represented as atoms connected by interatomic bonds.

To rotate "camera", drag with right button or Ctrl-drag.
To zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.
On a two-button mouse, middle is left + right.
To pan left/right and up/down, Shift-drag.
Touch screen: pinch/extend to zoom, swipe or two-finger rotate."""

class Crystal:
    def __init__(self, N, atom_radius, spacing, momentumRange):
        self.atoms = []
        self.springs = []
        
        # Create atoms
        for z in range(-1, N + 1):
            for y in range(-1, N + 1):
                for x in range(-1, N + 1):
                    atom = sphere(
                        pos=vector(x, y, z) * spacing, 
                        radius=atom_radius, 
                        color=vector(0, 0.58, 0.69)
                    )
                    if 0 <= x < N and 0 <= y < N and 0 <= z < N:
                        atom.momentum = momentumRange * vector(np.random.uniform(-1,1), np.random.uniform(-1,1), np.random.uniform(-1,1))
                    else:
                        atom.visible = False
                        atom.momentum = vector(0, 0, 0)
                    self.atoms.append(atom)

        # Create springs
        for atom in self.atoms:
            if atom.visible:
                neighbors = [
                    (vector(1, 0, 0), True),
                    (vector(0, 1, 0), True),
                    (vector(0, 0, 1), True),
                    (vector(-1, 0, 0), False),
                    (vector(0, -1, 0), False),
                    (vector(0, 0, -1), False)
                ]
                for direction, visible in neighbors:
                    neighbor_pos = atom.pos + direction * spacing
                    neighbor = next((a for a in self.atoms if a.pos == neighbor_pos and a.visible), None)
                    if neighbor:
                        self.make_spring(atom, neighbor, visible)

    def make_spring(self, start, end, visible):
        spring = helix(
            pos=start.pos,
            axis=end.pos - start.pos,
            radius=0.2 * spacing,
            thickness=0.05,
            color=color.orange,
            visible=visible
        )
        spring.start = start
        spring.end = end
        self.springs.append(spring)

# Create the crystal lattice
c = Crystal(N, atom_radius, spacing, 0.1 * spacing * np.sqrt(k / m))

# Simulation loop
while True:
    rate(60)
    for atom in c.atoms:
        if atom.visible:
            atom.pos += (atom.momentum / m) * dt
    for spring in c.springs:
        spring.axis = spring.end.pos - spring.start.pos
        L = mag(spring.axis)
        if L > 0:
            Fdt = spring.axis.norm() * (k * dt * (1 - spacing / L))
            if spring.start.visible:
                spring.start.momentum += Fdt
            if spring.end.visible:
                spring.end.momentum -= Fdt
