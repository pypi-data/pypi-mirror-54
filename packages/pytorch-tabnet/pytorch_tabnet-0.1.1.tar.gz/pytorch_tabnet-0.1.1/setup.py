# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pytorch_tabnet']

package_data = \
{'': ['*']}

install_requires = \
['numpy==1.17.2',
 'pandas==0.25.1',
 'scikit_learn==0.21.3',
 'torch==1.0.1',
 'tqdm==4.30.0']

setup_kwargs = {
    'name': 'pytorch-tabnet',
    'version': '0.1.1',
    'description': '',
    'long_description': '# README\n\n# TabNet : Attentive Interpretable Tabular Learning\n\nThis is a pyTorch implementation of Tabnet (Arik, S. O., & Pfister, T. (2019). TabNet: Attentive Interpretable Tabular Learning. arXiv preprint arXiv:1908.07442.) https://arxiv.org/pdf/1908.07442.pdf.\n\n# Installation\n\nYou can install using pip by running:\n`pip install pytorch-tabnet`\n\nIf you wan to use it locally within a docker container:\n\n`git clone git@github.com:dreamquark-ai/tabnet.git`\n\n`cd tabnet` to get inside the repository\n\n`make start` to build and get inside the container\n\n`poetry install` to install all the dependencies, including jupyter\n\n`make notebook` inside the same terminal\n\nYou can then follow the link to a jupyter notebook with tabnet installed.\n\n\n\nGPU version is available and should be working but is not supported yet.\n\n# How to use it?\n\nThe implementation makes it easy to try different architectures of TabNet.\nAll you need is to change the  network parameters and training parameters. All parameters are quickly describe bellow, to get a better understanding of what each parameters do please refer to the orginal paper.\n\nYou can also get comfortable with the code works by playing with the **notebooks tutorials** for adult census income dataset and forest cover type dataset.\n\n## Network parameters\n\n- input_dim : int\n\n    Number of initial features of the dataset\n\n- output_dim : int\n\n    Size of the desired output. Ex :\n    - 1 for regression task\n    - 2 for binary classification\n    -  N > 2 for multiclass classifcation\n\n- nd : int\n\n    Width of the decision prediction layer. Bigger values gives more capacity to the model with the risk of overfitting.\n    Values typically range from 8 to 64.\n\n- na : int\n\n    Width of the attention embedding for each mask.\n    According to the paper nd=na is usually a good choice.\n\n- n_steps : int\n    Number of steps in the architecture (usually between 3 and 10)\n\n- gamma : float\n    This is the coefficient for feature reusage in the masks.\n    A value close to 1 will make mask selection least correlated between layers.\n    Values range from 1.0 to 2.0\n- cat_idxs : list of int\n\n    List of categorical features indices.\n- cat_emb_dim : list of int\n\n    List of embeddings size for each categorical features.\n- n_independent : int\n\n    Number of independent Gated Linear Units layers at each step.\n    Usual values range from 1 to 5 (default=2)\n- n_shared : int\n\n    Number of shared Gated Linear Units at each step\n    Usual values range from 1 to 5 (default=2)\n- virtual_batch_size : int\n\n    Size of the mini batches used for Ghost Batch Normalization\n\n## Training parameters\n\n- max_epochs : int (default = 200)\n\n    Maximum number of epochs for trainng.\n- patience : int (default = 15)\n\n    Number of consecutive epochs without improvement before performing early stopping.\n- lr : float (default = 0.02)\n\n    Initial learning rate used for training. As mentionned in the original paper, a large initial learning of ```0.02 ```  with decay is a good option.\n- clip_value : float (default None)\n\n    If a float is given this will clip the gradient at clip_value.\n- lambda_sparse : float (default = 1e-3)\n\n    This is the extra sparsity loss coefficient as proposed in the original paper. The bigger this coefficient is, the sparser your model will be in terms of feature selection. Depending on the difficulty of your problem, reducing this value could help.\n- model_name : str (default = \'DQTabNet\')\n\n    Name of the model used for saving in disk, you can customize this to easily retrieve and reuse your trained models.\n- saving_path : str (default = \'./\')\n\n    Path defining where to save models.\n- scheduler_fn : torch.optim.lr_scheduler (default = None)\n\n    Pytorch Scheduler to change learning rates during training.\n- scheduler_params: dict\n\n    Parameters dictionnary for the scheduler_fn. Ex : {"gamma": 0.95,                    "step_size": 10}\n- verbose : int (default=-1)\n\n    Verbosity for notebooks plots, set to 1 to see every epoch.\n',
    'author': None,
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.8,<4.0.0',
}


setup(**setup_kwargs)
