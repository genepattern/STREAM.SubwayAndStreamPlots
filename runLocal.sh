rm -rf job_1/*

docker run  -v ${PWD}:$PWD -w $PWD/job_1 genepattern/stream_visualization python /stream/visualization_command_line.py  -m $PWD/test/data/stream_epg_result.pkl -of vz_  -fig_width 10 -fig_height 7 -fig_legend_ncol 3 -root S3 -subway_factor 2.0 -color_by label -factor_num_win 10 -factor_min_win 2.0 -factor_width 2.5 -factor_zoomin 100 -flag_cells -preference S4,S1 -genes 'Car2,Gata1,Epx'
