# Genetic-Algorithm

A genetic algorithm is an algorithm that imitates the process of natural selection. They help solve optimization and search problems. Genetic algorithms are part of the bigger class of evolutionary algorithms. Genetic algorithms imitate natural biological processes, such as inheritance, mutation, selection and crossover.

The concept of genetic algorithms is a search technique often used in computer science to find complex, non-obvious solutions to algorithmic optimisation and search problems. Genetic algorithms are global search heuristics.

## The pseudocode is:

   1) Initialization: A number of candidate solutions is generated; very often these have random values
      Evaluation: A fitness function allows to score each candidate; the score will be a number that tells how good this solution solves he      problem.
   2) The following steps are run until a stop criterion is met:
   3) Selection: Pick the solutions/individuals for the next iteration
   4) Recombination: Combine the solutions picked
   5) Mutation: Randomly change the newly generated solutions
   6) Evaluation: Apply the fitness function, see step 2.
   7) If the stop criterion is not met, re-start with the selection step.
