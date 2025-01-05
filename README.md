# DEA2H2
DEA2H2: Differential Evolution Architecture based Adaptive Hyper-Heuristic Algorithm for Continuous Optimization

## Abstract
This paper proposes a novel differential evolution (DE) architecture based hyper-heuristic algorithm (DEA$^2$H$^2$) for solving continuous optimization tasks. A representative hyper-heuristic algorithm consists of two main components: low-level and high-level components. In the low-level component, DEA$^2$H$^2$ leverages ten DE-derived search operators as low-level heuristics (LLHs). In the high-level component, we incorporate a success-history-based mechanism inspired by the success-history-based parameter adaptation in success-history adaptive DE (SHADE). Specifically, if a parent individual successfully evolves an offspring individual using a specific search operator, that corresponding operator is preserved for subsequent iterations. On the contrary, if the evolution is unsuccessful, the search operator is replaced by random initialization. To validate the effectiveness of DEA$^2$H$^2$, we conduct comprehensive numerical experiments on both CEC2020 and CEC2022 benchmark functions, as well as eight engineering problems. We compare the performance of DEA$^2$H$^2$ against fifteen well-known metaheuristic algorithms (MA). Additionally, ablation experiments are performed to investigate the effectiveness of the success-history-based high-level component independently. The experimental results and statistical analyses affirm the superiority and robustness of DEA$^2$H$^2$ across diverse optimization tasks, highlighting its potential as an effective tool for continuous optimization problems. The source code of this research can be downloaded from https://github.com/RuiZhong961230/DEA2H2.

## Citation
@article{Zhong:24,  
  title={DEA2H2: Differential Evolution Architecture based Adaptive Hyper-Heuristic Algorithm for Continuous Optimization},  
  author={Rui Zhong and Jun Yu},  
  journal={Cluster Computing},  
  volume={27},  
  pages={12239-12266},  
  year={2024},  
  publisher={Springer},  
  doi = {https://doi.org/10.1007/s10586-024-04587-0 },  
}

## Datasets and Libraries
CEC benchmarks are provided by the opfunu library and engineering problems are provided by the enoppy library.
