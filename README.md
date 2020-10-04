# AI Learns to Sail
Code for the blog post ["AI Learns to Sail upwind" on ML&Neuro Blog](https://ppierzc.github.io/ai-learns-to-sail-upwind).

A Q-learning implementation using average reward of the sailing upwind task.
Tackles two tasks: open sea and sailing in the channel.
The open sea just requires to select the appropriate angle to sail along.
The channel task requires the agent to learn how to gybe.

## Installation
Clone the project locally.

    git clone https://github.com/PPierzc/ai-learns-to-sail.git

## Open Sea
<img alt="open sea results" src="./imgs/open_sea.png" width="300px" />

    Running: Random agent on open sea task: 100%|██████████| 100/100 [00:00<00:00, 275.73it/s]
    Running: Train agent on open sea task: 100%|██████████| 500/500 [00:07<00:00, 67.93it/s]
    Results from last 100 episodes
    | ===== agent ===== | ===== mean ===== | ===== std ===== |
    | Random            | 52.52            | 35.16           |
    | Trained           | 107.89           | 10.36           |
    
## Channel
<img alt="channel results" src="./imgs/channel.png" width="300px" />

    Running: Random agent on channel sea task: 100%|██████████| 100/100 [00:00<00:00, 602.28it/s]
    Running: Train agent on channel sea task: 100%|██████████| 1000/1000 [00:11<00:00, 86.73it/s]
    Results from last 100 episodes
    | ===== agent ===== | ===== mean ===== | ===== std ===== |
    | Random            | 19.86            | 11.88           |
    | Trained           | 63.94            | 19.47           |