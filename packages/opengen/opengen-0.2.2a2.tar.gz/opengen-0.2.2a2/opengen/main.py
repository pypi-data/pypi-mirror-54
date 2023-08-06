import casadi.casadi as cs
import opengen as og
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean
import logging as lg

# Example: Ball and Plate
# ======================================


# System dynamics
# --------------------------------------

car_length = 0.5
sampling_time = 0.1
nx = 3
nu = 2

# state: x = (x, y, psi)
# input u = (v, delta)
def dynamics_ct(x, u):
    v = u[0]
    delta = u[1]
    psi = x[2]
    dx1 = v * cs.cos(psi)
    dx2 = v * cs.sin(psi)
    dx3 = (v / car_length) * cs.tan(delta)
    return [dx1, dx2, dx3]


def dynamics_dt(x, u):
    dx = dynamics_ct(x, u)
    return [x[i] + sampling_time * dx[i] for i in range(nx)]


def stage_cost(x, u):
    cost = u[0]**2 + u[1]**2 \
           + 10*x[0]**2 + 10*x[1]**2 + 0.1*x[2]**2
    return cost


def terminal_cost(x):
    cost = 200 * x[0]**2 + 200 * x[1]**2 + 2 * x[2]**2
    return cost


#
# --------------------------------------
N = 20
u_seq = cs.SX.sym("u", nu*N)  # sequence of all u's
x0 = cs.SX.sym("x0", nx)   # initial state


x_t = x0
total_cost = 0
for t in range(0, N):
    u_t = u_seq[nu*t:nu*t+2]
    total_cost += stage_cost(x_t, u_t)  # update cost
    x_t = dynamics_dt(x_t, u_t)         # update state

total_cost += terminal_cost(x_t)  # terminal cost
F1 = x_t[0]

delta_bound = 1.5
velocity_min = -2
velocity_max = 10

u_seq_min = [-delta_bound, velocity_min]*N
u_seq_max = [delta_bound, velocity_max]*N

U = og.constraints.Rectangle(u_seq_min, u_seq_max)

problem = og.builder.Problem(u_seq, x0, total_cost)\
    .with_constraints(U)\
    .with_aug_lagrangian_constraints(F1, og.constraints.Zero())

build_config = og.config.BuildConfiguration()\
    .with_build_directory("python_build")\
    .with_build_mode("debug")\
    .with_tcp_interface_config()\
    .with_build_c_bindings()

meta = og.config.OptimizerMeta().with_optimizer_name("nils")

solver_config = og.config.SolverConfiguration()\
    .with_tolerance(1e-4)\
    .with_initial_tolerance(1e-4)\
    .with_max_inner_iterations(5000)

builder = og.builder.OpEnOptimizerBuilder(problem, meta,
                                          build_config, solver_config)\
    .with_verbosity_level(lg.INFO)
builder.build()

# -------------------------------------------------------------------------
# Simulations
# -------------------------------------------------------------------------
mng = og.tcp.OptimizerTcpManager("python_build/nils")
mng.start()

x_state_0 = [-2, 1, -0.1]

state_sequence = x_state_0
input_sequence = []
solver_time = []

simulation_steps = 1000

x = x_state_0
for k in range(simulation_steps):
    solver_status = mng.call(x)

    print(solver_status["exit_status"], " ::", solver_status["solve_time_ms"])

    us = solver_status['solution']
    u = us[0:nu+1]

    x_next = dynamics_dt(x, u)
    state_sequence += x_next
    input_sequence += u
    solver_time += [solver_status['solve_time_ms']]
    x = x_next

mng.kill()


#
# mng.kill()
#
time = np.arange(0, sampling_time*simulation_steps, sampling_time)

# plt.rcParams["font.size"] = "12"
# plt.plot(time, state_sequence[0:nx*simulation_steps:nx], '-', label="x")
# plt.plot(time, state_sequence[1:nx*simulation_steps:nx], '-', label="y")
# plt.grid()
# plt.ylabel('Position')
# plt.xlabel('Time')
# plt.legend(bbox_to_anchor=(0.7, 0.85), loc='upper left', borderaxespad=0.)
# plt.show()


plt.plot(input_sequence[1:nu*simulation_steps:nu], '-')
plt.xlabel('Time')
plt.ylabel('Steering (delta)')
plt.grid()
plt.show()
