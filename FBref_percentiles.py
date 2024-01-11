# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 21:57:13 2023

@author: Graduate
"""


def percentiles(df, player_name):

    npg_sorted = df.sort_values(by='G-PK', ascending=False).reset_index()
    npxG_sorted = df.sort_values(by='npxG', ascending=False).reset_index()
    sh_sorted = df.sort_values(by='Sh/90', ascending=False).reset_index()
    ast_sorted = df.sort_values(by='Ast', ascending=False).reset_index()
    xAG_sorted = df.sort_values(by='xAG', ascending=False).reset_index()
    npxG_plus_xAG_sorted = df.sort_values(by='npxG+xAG', ascending=False).reset_index()
    SCA_sorted = df.sort_values(by='SCA90', ascending=False).reset_index()
    pass_att_sorted = df.sort_values(by='Att', ascending=False).reset_index()
    pass_cmp_sorted = df.sort_values(by='Cmp%', ascending=False).reset_index()
    prgP_sorted = df.sort_values(by='PrgP', ascending=False).reset_index()
    prgC_sorted = df.sort_values(by='PrgC', ascending=False).reset_index()
    succ_sorted = df.sort_values(by='Succ', ascending=False).reset_index()
    att_pen_sorted = df.sort_values(by='Att Pen', ascending=False).reset_index()
    prgR_sorted = df.sort_values(by='PrgR.1', ascending=False).reset_index()
    tkl_sorted = df.sort_values(by='Tkl', ascending=False).reset_index()
    int_sorted = df.sort_values(by='Int', ascending=False).reset_index()
    blk_sorted = df.sort_values(by='Blocks.1', ascending=False).reset_index()
    clr_sorted = df.sort_values(by='Clr', ascending=False).reset_index()

    
    npg_index = npg_sorted.index[npg_sorted['Player'] == player_name][0]
    npxG_index = npxG_sorted.index[npxG_sorted['Player'] == player_name][0]
    sh_index = sh_sorted.index[sh_sorted['Player'] == player_name][0]
    ast_index = ast_sorted.index[ast_sorted['Player'] == player_name][0]
    xAG_index = xAG_sorted.index[xAG_sorted['Player'] == player_name][0]
    npxG_plus_xAG_index = npxG_plus_xAG_sorted.index[npxG_plus_xAG_sorted['Player'] == player_name][0]
    SCA_index = SCA_sorted.index[SCA_sorted['Player'] == player_name][0]
    pass_att_index = pass_att_sorted.index[pass_att_sorted['Player'] == player_name][0]
    pass_cmp_index = pass_cmp_sorted.index[pass_cmp_sorted['Player'] == player_name][0]
    prgP_index = prgP_sorted.index[prgP_sorted['Player'] == player_name][0]
    prgC_index = prgC_sorted.index[prgC_sorted['Player'] == player_name][0]
    succ_index = succ_sorted.index[succ_sorted['Player'] == player_name][0]
    att_pen_index = att_pen_sorted.index[att_pen_sorted['Player'] == player_name][0]
    prgR_index = prgR_sorted.index[prgR_sorted['Player'] == player_name][0]
    tkl_index = tkl_sorted.index[tkl_sorted['Player'] == player_name][0]
    int_index = int_sorted.index[int_sorted['Player'] == player_name][0]
    blk_index = blk_sorted.index[blk_sorted['Player'] == player_name][0]
    clr_index = clr_sorted.index[clr_sorted['Player'] == player_name][0]

    
    rows = df.shape[0]
    
    pts_percentile = int(((rows - npg_index) / rows) * 100)
    fg_percentile = int(((rows - npxG_index) / rows) * 100)
    fga_percentile = int(((rows - sh_index) / rows) * 100)
    fgp_percentile = int(((rows - ast_index) / rows) * 100)
    threep_percentile = int(((rows - xAG_index) / rows) * 100)
    threepa_percentile = int(((rows - npxG_plus_xAG_index) / rows) * 100)
    threepp_percentile = int(((rows - SCA_index) / rows) * 100)
    twop_percentile = int(((rows - pass_att_index) / rows) * 100)
    twopa_percentile = int(((rows - pass_cmp_index) / rows) * 100)
    twopp_percentile = int(((rows - prgP_index) / rows) * 100)
    ft_percentile = int(((rows - prgC_index) / rows) * 100)
    fta_percentile = int(((rows - succ_index) / rows) * 100)
    ftp_percentile = int(((rows - att_pen_index) / rows) * 100)
    orb_percentile = int(((rows - prgR_index) / rows) * 100)
    drb_percentile = int(((rows - tkl_index) / rows) * 100)
    trb_percentile = int(((rows - int_index) / rows) * 100)
    ast_percentile = int(((rows - blk_index) / rows) * 100)
    stl_percentile = int(((rows - clr_index) / rows) * 100)

    
    percentiles = [pts_percentile, fg_percentile, fga_percentile, fgp_percentile, threep_percentile, threepa_percentile, threepp_percentile, twop_percentile, twopa_percentile, twopp_percentile, ft_percentile, fta_percentile, ftp_percentile, orb_percentile, drb_percentile, trb_percentile, ast_percentile, stl_percentile]
    return percentiles