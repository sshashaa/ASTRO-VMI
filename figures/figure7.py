import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, execute, Aer
import warnings 
warnings.filterwarnings('ignore') 

def append_zz_term(qc, q1, q2, gamma, cost):
    qc.cx(q1, q2)
    qc.rz(2 * cost * gamma, q2)
    qc.cx(q1, q2)

def get_cost_operator_circuit(G, gamma, costs):
    N = G.number_of_nodes()
    qc = QuantumCircuit(N, N)
    k = 0 
    for i, j in G.edges():
        cost = costs[k]
        k += 1
        append_zz_term(qc, i, j, gamma, cost)
    return qc

def append_x_term(qc, q1, beta):
            qc.rx(2 * beta, q1)

def get_mixer_operator_circuit(G, beta):
    N = G.number_of_nodes()
    qc = QuantumCircuit(N, N)
    for n in G.nodes():
        append_x_term(qc, n, beta)
    return qc

def get_qaoa_circuit(G, beta, gamma, costs):
    assert (len(beta) == len(gamma))
    p = len(beta)
    N = G.number_of_nodes()
    qc = QuantumCircuit(N, N)
    qc.h(range(N))
    for i in range(p):
        qc = qc.compose(get_cost_operator_circuit(G, gamma[i], costs))
        qc = qc.compose(get_mixer_operator_circuit(G, beta[i]))

    # measure the result
    qc.barrier(range(N))
    qc.measure(range(N), range(N))
    return qc

def maxcut_obj(x, G, costs):
    cut = 0
    k = 0
    for i, j in G.edges():
        if x[i] != x[j]:
            cut -= (costs[k] + 1)/2
        k += 1
    return cut

def compute_maxcut_energy(counts, G, costs):
    energy = 0
    total_counts = 0
    for meas, meas_count in counts.items():
        obj_for_meas = maxcut_obj(meas, G, costs)
        energy += obj_for_meas * meas_count
        total_counts += meas_count
    return energy / total_counts

def compute_variance(counts, G, energy, costs):
    squared_energy = 0
    total_counts = 0
    for meas, meas_count in counts.items():
        obj_for_meas = maxcut_obj(meas, G, costs)
        squared_energy += obj_for_meas**2 * meas_count
        total_counts += meas_count

    squared_energy_average = squared_energy / total_counts
    return  squared_energy_average - energy**2


def invert_counts(counts):
    return {k[::-1]:v for k, v in counts.items()}

p = 1
betas = np.linspace(0.0, 3.141592, num=20)
gammas = np.linspace(0.0, 3.141592, num=20)

edges = [[[0,1],[0,2],[0,3],[0,4]],
         [[0,3],[0,4],[1,3],[1,4],[1,2],[0,2]]]

costs_list = [[1,1,1,1],
            [1,1,1,1,1,1]]
for z in range(len(edges)):
    G = nx.Graph()
    costs = costs_list[z]
    G.add_edges_from(edges[z])

    backend = Aer.get_backend('qasm_simulator')

    energies = np.zeros((len(betas), len(gammas)))
    variance = np.zeros((len(betas), len(gammas)))
    sum_1 = np.zeros((len(betas), len(gammas)))
    sum_2 = np.zeros((len(betas), len(gammas)))
    sum_3 = np.zeros((len(betas), len(gammas)))

    for i, beta in enumerate(betas):
        for j, gamma in enumerate(gammas):
            theta = [beta, gamma]
            beta_ = theta[:p]
            gamma_ = theta[p:]
            qc = get_qaoa_circuit(G, beta_, gamma_, costs)
            counts = execute(qc, backend, seed_simulator=5, shots=200).result().get_counts()
            
            # return the energy
            energy = compute_maxcut_energy(counts, G, costs)
            variance_ind = compute_variance(counts, G, energy, costs)
            energies[i, j] = energy
            variance[i, j] = variance_ind
            sum_1[i,j] = energy + 0.1*variance_ind
            sum_2[i,j] = energy + 0.3*variance_ind
            sum_3[i,j] = energy + 0.5*variance_ind


    fig, axs = plt.subplots(1, 2, figsize=(16, 6))

    contour1 = axs[0].contourf(betas, gammas, energies, levels=50, cmap='viridis')
    fig.colorbar(contour1, ax=axs[0])
    axs[0].set_xlabel('Beta')
    axs[0].set_ylabel('Gamma')
    axs[0].set_title('Max-Cut Energy Landscape')

    contour2 = axs[1].contourf(betas, gammas, variance, levels=50, cmap='viridis')
    fig.colorbar(contour2, ax=axs[1])
    axs[1].set_xlabel('Beta')
    axs[1].set_ylabel('Gamma')
    axs[1].set_title('Variance Landscape')

    # Show the combined figure
    plt.tight_layout()

    # Save the figure as a PDF
    plt.savefig(f'experiments/plots/Figure7_{edges[z]}.pdf', format='pdf')
