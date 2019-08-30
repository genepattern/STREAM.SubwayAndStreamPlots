#!/usr/bin/env python
# -*- coding: utf-8 -*-

import warnings

warnings.filterwarnings('ignore')

__tool_name__='STREAM'
print('''
   _____ _______ _____  ______          __  __ 
  / ____|__   __|  __ \|  ____|   /\   |  \/  |
 | (___    | |  | |__) | |__     /  \  | \  / |
  \___ \   | |  |  _  /|  __|   / /\ \ | |\/| |
  ____) |  | |  | | \ \| |____ / ____ \| |  | |
 |_____/   |_|  |_|  \_\______/_/    \_\_|  |_|
... cell and gene visualizations                                             
''',flush=True)

import stream as st
import argparse
import multiprocessing
import os
from slugify import slugify
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import sys

mpl.use('Agg')
mpl.rc('pdf', fonttype=42)

os.environ['KMP_DUPLICATE_LIB_OK']='True'


print('- STREAM Single-cell Trajectory Reconstruction And Mapping -',flush=True)
print('Version %s\n' % st.__version__,flush=True)
    

def main():
    sns.set_style('white')
    sns.set_context('poster')
    parser = argparse.ArgumentParser(description='%s Parameters' % __tool_name__ ,formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-m", "--data-file", dest="input_filename",default = None, help="input file name, pkl format from Stream preprocessing module", metavar="FILE")
    parser.add_argument("-of","--of",dest="output_filename_prefix", default="StreamiFSOutput",  help="output file name prefix")
    parser.add_argument("-fig_width",dest="fig_width", type=int, default=8, help="")
    parser.add_argument("-fig_height",dest="fig_height", type=int, default=8, help="")
    parser.add_argument("-fig_legend_ncol",dest="fig_legend_ncol", type=int, default=None, help="")

    parser.add_argument("-root",dest="root", default=None, help="")
    parser.add_argument("-preference",dest="preference", help="")
    parser.add_argument("-subway_factor",dest="subway_factor",  type=float, default=2.0, help="")
    parser.add_argument("-color_by",dest="color_by", default='label', help="")
    parser.add_argument("-factor_num_win",dest="factor_num_win", type=int, default=10, help="")
    parser.add_argument("-factor_min_win",dest="factor_min_win", type=float, default=2.0, help="")
    parser.add_argument("-factor_width",dest="factor_width", type=float, default=2.5, help="")
    parser.add_argument("-flag_log_view",dest="flag_log_view", action="store_true", help="")
    parser.add_argument("-factor_zoomin",dest="factor_zoomin", type=float, default=100.0, help="")
    parser.add_argument("-flag_cells",dest="flag_cells", action="store_true", help="")
    parser.add_argument("-flag_genes",dest="flag_genes", action="store_true", help="")
         

    parser.add_argument("-genes",dest="genes",  default=None, help="")
    parser.add_argument("-percentile_dist",dest="percentile_dist", type=float, default=100, help="")

    args = parser.parse_args()
    
    workdir = "./"

    adata = st.read(file_name=args.input_filename, file_format='pkl', experiment='rna-seq', workdir=workdir)
    preference = args.preference.split(',')
    if (args.flag_cells != None):
        st.plot_flat_tree(adata,save_fig=True, fig_path="./", fig_name=(args.output_filename_prefix + '_flat_tree.png'), fig_size=(args.fig_width, args.fig_height),fig_legend_ncol=args.fig_legend_ncol)

        st.subwaymap_plot(adata,root=args.root,percentile_dist=args.percentile_dist, 
                  preference=preference, factor=args.subway_factor, color_by=args.color_by,
                  save_fig=True,fig_path="./",fig_name=(args.output_filename_prefix + '_cell_subway_map.png'), fig_size=(args.fig_width, args.fig_height),fig_legend_ncol=args.fig_legend_ncol) 

        st.stream_plot(adata,root=args.root,
               preference=preference, factor_num_win=args.factor_num_win,factor_min_win=args.factor_min_win,factor_width=args.factor_width,
               flag_log_view=args.flag_log_view,factor_zoomin=args.factor_zoomin,
               save_fig=True,fig_path="./",fig_name=(args.output_filename_prefix + '_cell_stream_plot.png'),fig_size=(args.fig_width, args.fig_height),fig_legend=True,
               fig_legend_ncol=args.fig_legend_ncol,tick_fontsize=20,label_fontsize=25)

    if (args.flag_genes != None):
        genes = args.genes.split(',')
        st.subwaymap_plot_gene(adata,root=args.root,genes=genes,
                       preference=preference,percentile_dist=args.percentile_dist,factor=args.subway_factor,
                       save_fig=True,fig_path="./",fig_format='png',fig_size=(args.fig_width, args.fig_height))
        #              , fig_name=(args.output_filename_prefix + '_gene_subway_plot.png')) 

        st.stream_plot_gene(adata,root=args.root,genes=genes,
                    preference=preference,factor_min_win=args.factor_min_win,factor_num_win=args.factor_num_win,factor_width=args.factor_width,
                    save_fig=True,fig_path="./",fig_format='png',fig_size=(args.fig_width, args.fig_height),tick_fontsize=20,label_fontsize=25)
        #           , fig_name=(args.output_filename_prefix + '_gene_stream_plot.png'))




    st.write(adata,file_name=(args.output_filename_prefix + '_stream_result.pkl'),file_path='./',file_format='pkl') 

    print('Finished computation.')

if __name__ == "__main__":
    main()
