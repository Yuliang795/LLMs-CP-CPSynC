import argparse
import pickle
import os, sys

def load_inputs(ovar_transformer):
    parser = argparse.ArgumentParser()
    parser.add_argument('-check', choices=['sat', 'opt'], required=True)
    parser.add_argument('-ovar', required=True)
    parser.add_argument('-param', required=True)
    args = parser.parse_args()

    param_dict = {}
    if os.path.isfile(args.param):
        with open(args.param, 'rb') as f:
            param_dict = pickle.load(f)

    with open(args.ovar, 'rb') as f:
        dvar_dict = ovar_transformer(pickle.load(f), param_dict)

    return args, param_dict, dvar_dict


# def load_params_pkl(pkl_params_path):
#     data_dict=None
#     if pkl_params_path!=None and Path(pkl_params_path).is_file():
#         with open(pkl_params_path, 'rb') as file:
#             data_dict = pickle.load(file)
#     return data_dict