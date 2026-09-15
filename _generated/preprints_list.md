### 2026

**Rothe's Method for Quantum Dynamics in Atoms and Molecules with Gaussian Wavepackets**

Simon Elias Schrader, Håkon Emil Kristiansen, Aleksander P. Wozniak, Ludwik Adamowicz, **Simen Kvaal**, and Thomas Bondo Pedersen (2026).\
[doi:10.48550/arXiv.2606.20947](https://doi.org/10.48550/arXiv.2606.20947)

:::{.content-visible when-format="html"}
<details>
<summary>Abstract</summary>
<p>Capable of capturing both bound and continuum quantum dynamics, Gaussian wavepackets are highly attractive basis functions for simulating laser-driven processes in atoms and molecules. Unfortunately, fully flexible Gaussian wavepackets are exceedingly challenging to propagate in a numerically stable manner within the framework of conventional time-dependent variational principles. In this chapter, we discuss the sources of the numerical issues and review an alternative approach, Rothe's method, that offers a route to improved numerical stability. Recent proof-of-concept simulations based on Rothe's method indicate that Gaussian wavepackets provide results on par with highly accurate grid-based methods for both electronic and rovibrational quantum dynamics, including ultrafast nonlinear processes that involve the continuum such as high-harmonic generation. Remarkably few Gaussian wavepackets are needed to achieve the high accuracy of grid-based approaches, indicating that further algorithmic developments and efficient implementations may enable efficient simulations of not only electronic and rovibrational phenomena but also fully coupled electronic-nuclear quantum dynamics with significantly reduced memory demands. We also point out remaining practical challenges, including matrix elements of the squared Hamiltonian and the treatment of Coulomb cusps.</p>
</details>
:::

---

**Reduced Density Matrix Functional Theory And A Reduced Formulation Of Density Functional Theory**

Håkon R. Fredheim and **Simen Kvaal** (2026).\
[doi:10.48550/arXiv.2510.12242](https://doi.org/10.48550/arXiv.2510.12242)

:::{.content-visible when-format="html"}
<details>
<summary>Abstract</summary>
<p>A mathematical framework for reduced density matrix functional theory (RDMFT) is proposed. The work is inspired by and generalizes the work by E.H. Lieb [E.H. Lieb, Int. J. Quant. Chem. 24(1983), pp.243–277] on density-functional theory (DFT). We introduce a Banach space for density matrices with finite kinetic energy. The dual space is a rich class of single-particle potentials, i.e., Hermitian forms. The ground state energy of an $N$-fermion system with external forces given by any such Hermitian form is expressed as the Legendre–Fenchel transform of a convex and lower semicontinuous “universal” reduced density matrix functional. The formalism is employed to provide a mathematical framework for density-functional theory (DFT). The main tool here is a rigorous definition of diagonals of reduced density matrices. The result is a refinement of Lieb's results on DFT applicable to a wide variety of models.</p>
</details>
:::

---

### 2022

**No need for a grid: Adaptive fully-flexible gaussians for the time-dependent Schrödinger equation**

**Simen Kvaal**, Caroline Lasser, Thomas Bondo Pedersen, and Ludwik Adamowicz (2022).\
[arXiv](http://arxiv.org/abs/2207.00271)

:::{.content-visible when-format="html"}
<details>
<summary>Abstract</summary>
<p>Linear combinations of complex gaussian functions, where the nonlinear parameters are allowed to vary, are shown to be an extremely flexible representation for the solution of the time-dependent Schrödinger equation in one spatial dimension. Propagation of such wavefunctions using the Dirac–Frenkel variational principle is notoriously hard, and we present instead a scheme based on the method of vertical lines, or Rothe's method. We apply the method to a simple test system mimicking an atom subject to an extreme laser pulse, producing complicated ionization dynamics. The scheme is shown to perform very well on this model. Since the propagation method can be formulated entirely in terms of gaussian integrals and expectation values, we eliminate the need for large grids using only a handful of gaussian functions but with the same accuracy. This paves the way for accurate and affordable solutions of the time-dependent Schrödinger equation for multi-atom molecules beyond the Born–Oppenheimer approximation.</p>
</details>
:::

---
