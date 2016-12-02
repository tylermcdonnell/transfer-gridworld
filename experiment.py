__author__ = "Tyler McDonnell"
from rlpy.Domains import GridWorld
from rlpy.Agents import Q_Learning
from rlpy.Representations import Tabular
from rlpy.Policies import eGreedy
from rlpy.Experiments import Experiment
import matplotlib.pyplot as plt
import os
import argparse


def make_experiment(batch_id, exp_id, grid, max_steps=10000, weight_vec=None):
    """
    Each file specifying an experimental setup should contain a
    make_experiment function which returns an instance of the Experiment
    class with everything set up.

    @param id: number used to seed the random number generators
    @param path: output directory where logs and results are stored
    """
    path = ('./Results/Experiment%d' % batch_id)
    opt = {}
    opt["exp_id"] = exp_id
    opt["path"] = path

    # Domain:
    domain = GridWorld(grid, noise=0.3)
    opt["domain"] = domain

    # Representation
    representation = Tabular(domain, discretization=20)

    # Policy
    policy = eGreedy(representation, epsilon=0.2)

    # Agent
    opt["agent"] = Q_Learning(representation=representation, policy=policy,
                              discount_factor=domain.discount_factor,
                              initial_learn_rate=0.1,
                              learn_rate_decay_mode="boyan", boyan_N0=100,
                              lambda_=0)
    opt["checks_per_policy"] = 10
    opt["max_steps"] = max_steps
    opt["num_policy_checks"] = 1
    experiment = Experiment(**opt)

    # Insert weight vector as start point if provided.
    if weight_vec != None:
        representation.weight_vec = weight_vec
    return experiment

def transfer_experiment(batch_id, gridA, gridB, max_steps):
    '''
    Creates a grid world transfer learning experiment.
    
    :param gridA: Path to grid world file to serve as source domain.
    :param gridB: Path to grid world file to serve as target domain.
    :param max_steps: Max number of steps to learn in either domain.
    '''
    # Train on source domain.
    source = make_experiment(batch_id, 1, gridA, max_steps=max_steps)
    source.run(visualize_steps=True,
               visualize_learning=True,
               visualize_performance=1)
    source.plot(save=False)
    plt.close("all")

    # Extract weight vector learned from source domain.
    learned = source.agent.representation.weight_vec

    # Train on target domain without learned weight vector.
    target_notransfer = make_experiment(batch_id,
                                        2,
                                        gridB,
                                        max_steps=max_steps)
    target_notransfer.run(visualize_steps=True,
                          visualize_learning=True,
                          visualize_performance=1)
    target_notransfer.plot(save=False)
    plt.close("all")
    

    # Train on target domain with transfer.
    target_transfer   = make_experiment(batch_id,
                                        3,
                                        gridB,
                                        max_steps=max_steps,
                                        weight_vec=learned)
    target_transfer.run(visualize_steps=True,
                        visualize_learning=True,
                        visualize_performance=1)
    target_transfer.plot(save=False)
    plt.close("all")
    
    return source, target_notransfer, target_transfer

def batch_transfer_experiment(batch_id, source_task, directory, max_steps):
    count = 0
    ratios = []
    for f in os.listdir(directory):
        if f.endswith('.txt'):
            source, target_notransfer, target = transfer_experiment(batch_id, source_task, os.path.join(directory, f), 2000)
            # Compute transfer ratio.
            tr = target.evaluate(1, 1) / target_notransfer.evaluate(1,1)
            ratios.append(tr)
            print "Transfer Ratio: %f" % tr
    for r in ratios:
        print 
                                                                    

    

if __name__ == '__main__':
    '''
    experiment = make_experiment(1)
    experiment.run(visualize_steps=False,  # should each learning step be shown?
                   visualize_learning=True,  # show policy / value function?
                   visualize_performance=1)  # show performance runs?
    experiment.plot()
    experiment.save()
    '''

    # Transfer learning experiments for grid worlds of varying size.
    #source, target_notransfer, target = transfer_experiment(0, 'worlds/3x3/grid1.txt', 'worlds/3x3/grid1.txt', 10000)
    #source, target_notransfer, target = transfer_experiment(1, 'worlds/4x4/grid0.txt',  'worlds/4x4/grid1.txt', 10000)
    #source, target_notransfer, target = transfer_experiment(2, 'worlds/5x5/grid0.txt',  'worlds/5x5/grid1.txt', 5000)
    #source, target_notransfer, target = transfer_experiment(3, 'worlds/6x6/grid0.txt',  'worlds/6x6/grid1.txt', 5000)
    #source, target_notransfer, target = transfer_experiment(4, 'worlds/7x7/grid0.txt',  'worlds/7x7/grid1.txt', 5000)
    #source, target_notransfer, target = transfer_experiment(5, 'worlds/8x8/grid0.txt',  'worlds/8x8/grid1.txt', 10000)
    #source, target_notransfer, target = transfer_experiment(6, 'worlds/9x9/grid0.txt',  'worlds/9x9/grid1.txt', 30000)
    #source, target_notransfer, target = transfer_experiment(7, 'worlds/10x10/grid0.txt', 'worlds/10x10/grid1.txt', 10000)

    batch_transfer_experiment(10, 'worlds/4x4vary/grid0.txt', 'worlds/4x4vary/', 1000)
