#!/usr/bin/env python
# coding: utf-8

"""
Load a trained speaker and images/data to create (sample) captions for them.

The MIT License (MIT)
Originally created at 10/3/20, for Python 3.x
Copyright (c) 2021 Panos Achlioptas (ai.stanford.edu/~optas) & Stanford Geometric Computing Lab
"""

import argparse
import os.path as osp
import pathlib
import pprint

import numpy as np
import pandas as pd
import torch
from artemis.captioning.sample_captions import versatile_caption_sampler
from artemis.in_out.basics import read_saved_args
from artemis.in_out.datasets import AffectiveCaptionDataset
from artemis.in_out.neural_net_oriented import (image_transformation,
                                                load_state_dicts,
                                                torch_load_model)
from artemis.neural_models.show_attend_tell import \
    describe_model as describe_sat
from artemis.utils.vocabulary import Vocabulary


def custom_data_loader(img, img_transforms):
    image_files = pd.Series([img])
    dummy = pd.Series(np.ones(len(image_files), dtype=int) * -1)
    emotions = dummy

    custom_dataset = AffectiveCaptionDataset(image_files, dummy, emotions=emotions,
                                             n_emotions=5,
                                             img_transform=img_transforms)

    custom_data_loader = torch.utils.data.DataLoader(dataset=custom_dataset,batch_size=len(custom_dataset),num_workers=1)
    return custom_data_loader

def load_speaker(args_file, model_ckp, with_data=False, override_args=None, verbose=False):
    """
    :param args_file: saved argparse arguments with model's description (and location of used data)
    :param model_ckp: saved checkpoint with model's parameters.
    :param with_data:
    :param override_args:
    :return:
    Note, the model is loaded and returned in cpu.
    """
    if verbose:
        print('Loading saved speaker trained with parameters:')
    args = read_saved_args(args_file, override_args=override_args, verbose=verbose)

    # Prepare empty model
    vocab = Vocabulary.load('./server/preprocessed/vocabulary.pkl')
    
    print('Using a vocabulary of size', len(vocab))
    model = describe_sat(vocab, args)

    # Load save weights
    epoch = load_state_dicts(model_ckp, model=model, map_location='cpu')
    print('Loading speaker model at epoch {}.'.format(epoch))

    # Load transform
    img_transforms = image_transformation(args.img_dim, lanczos=args.lanczos)["train"]
    
    return model, epoch, img_transforms

def str2bool(v):
    """ boolean values for argparse
    """
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def parse_speaker_arguments(notebook_options=None):
    """ Parameters for testing (sampling) a neural-speaker.
    :param notebook_options: list, if you are using this via a jupyter notebook
    :return: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(description='testing-a-neural-speaker')

    ## Basic required arguments
    parser.add_argument('-speaker-saved-args', type=str, required=True, help='config.json.txt file for saved speaker model (output of train_speaker.py)')
    parser.add_argument('-speaker-checkpoint', type=str, required=True, help='saved model checkpoint ("best_model.pt" (output of train_speaker.py)')
    parser.add_argument('-img-dir', type=str, help='path to top image dir (typically that\'s the WikiArt top-dir)')
    parser.add_argument('-out-file', type=str, help='file to save the sampled utterances, their attention etc. as a pkl')

    ## Basic optional arguments
    parser.add_argument('--split', type=str, default='test', choices=['train', 'test', 'val', 'rest'], help='set the split of the dataset you want to annotate '
                                                                                                            'the code will load the dataset based on the dir-location marked '
                                                                                                            'in the input config.json.txt file. ' 
                                                                                                            'this param has no effect if a custom-data-csv is passed.')

    parser.add_argument('--custom-data-csv', type=str, help='if you want to annotate your own set of images. Please '
                                                            'see the code for what this csv should look like. ')

    parser.add_argument('--subsample-data', type=int, default=-1, help='if not -1, will subsample the underlying dataset'
                                                                        'and will annotated only this many images.')


    ## Optional arguments controlling the generation/sampling process
    parser.add_argument('--max-utterance-len', type=int, help='maximum allowed lenght for any sampled utterances. If not given '
                                                              'the maximum found in the underlying dataset split will be used.'
                                                              'Fot the official ArtEmis split for deep-nets that is 30 tokens.')

    parser.add_argument('--drop-unk', type=str2bool, default=True, help='if True, do not create samples that contain the '
                                                                        'unknown token')

    parser.add_argument('--drop-bigrams', type=str2bool, default=True, help='if True, prevent the same bigram to occur '
                                                                            'twice in a sampled utterance')


    ## To enable the pass of multiple configurations for the sampler at once! i.e., so you can try many
    ## sampling temperatures, methods to sample (beam-search vs. topk), beam-size (or more)
    ## You can provide a simple .json that specifies these values you want to try.
    ## See  >> data/speaker_sampling_configs << for examples
    ## Note. if you pass nothing the >> data/speaker_sampling_configs/selected_hyper_params.json.txt << will be used
    ##       these are parameters used in the the paper.
    parser.add_argument('--sampling-config-file', type=str, help='Note. if max-len, drop-unk '
                                                                 'and drop-bigrams are not specified in the json'
                                                                 'the directly provided values of these parameters '
                                                                 'will be used.')


    parser.add_argument('--random-seed', type=int, default=2021, help='if -1 it won\'t have an effect; else the sampler '
                                                                      'becomes deterministic')

    parser.add_argument('--img2emo-checkpoint', type=str, help='checkpoint file of image-2-emotion classifier that will '
                                                               'be used to sample the grounding emotion that will be used '
                                                               'by the speaker, if you pass an emotionally-grouned speaker. '
                                                               'Note. if you pass/use an emo-grounded speaker - this argument '
                                                               'becomes required, except if you are using your own custom-data-csv '
                                                               'where you can specify the grounding emotion manually.' )

    parser.add_argument('--gpu', type=str, default='0')
    parser.add_argument('--n-workers', type=int)

    parser.add_argument('--compute-nll', type=str2bool, default=False, help='Compute the negative-log-likelihood of '
                                                                            'the dataset under the the saved speaker model.')

    # Parse arguments
    if notebook_options is not None:  # Pass options directly
        args = parser.parse_args(notebook_options)
    else:
        args = parser.parse_args() # Read from command line.

    # load "default"
    if args.sampling_config_file is None:
        up_dir = osp.split(pathlib.Path(__file__).parent.absolute())[0]
        args.sampling_config_file = osp.join(up_dir, 'data/speaker_sampling_configs/selected_hyper_params.json.txt')

    # pprint them
    print('\nParameters Specified:')
    args_string = pprint.pformat(vars(args))
    print(args_string)
    print('\n')

    return args

def image2caption(img_file):
    annotate_loader = custom_data_loader(img_file, img_transforms)
    captions_predicted, attn_weights = versatile_caption_sampler(speaker, annotate_loader, device, 50, "argmax")
    # print(captions_predicted)
    # print('Done.')
    return next(iter(captions_predicted))

# Load pretrained speaker & its corresponding train-val-test data. 
speaker, epoch, img_transforms = load_speaker("./server/config.json.txt", "./server/checkpoints/best_model.pt", with_data=False, verbose=True)
device = torch.device("cpu")
speaker = speaker.to(device)
