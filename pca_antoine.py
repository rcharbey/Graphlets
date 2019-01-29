# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 13:34:03 2016

@author: antoine
"""

import json
import gzip
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.patches import Circle
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import numpy as np
from scipy import cluster
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import pdist
from scipy.stats import chi2_contingency, pearsonr
from itertools import combinations
import sys
sys.path.append("lib")
import csv


def circleOfCorrelations(pc_infos, ebouli, dimensions):
    maxi = 0
    dim1, dim2 = dimensions[0], dimensions[1]
    for idx in range(len(pc_infos["PC-1"])):
        x = pc_infos["PC-%s" % dim1][idx]
        y = pc_infos["PC-%s" % dim2][idx]
        if max(abs(x),abs(y)) > maxi:
            maxi = max(abs(x),abs(y))
        plt.plot([0.0,x],[0.0,y],'k-')
        plt.plot(x, y, 'rx')
        plt.annotate(pc_infos.index[idx], xy=(x,y))
    rad = 1.4*maxi
    circle1=plt.Circle((0,0),radius=rad, color='g', fill=False)
    fig = plt.gcf()
    fig.gca().add_artist(circle1)
    plt.xlabel("PC-%s (%s%%)" % (dim1, str(ebouli[dim1-1])[:4].lstrip("0.")))
    plt.ylabel("PC-%s (%s%%)" % (dim2, str(ebouli[dim2-1])[:4].lstrip("0.")))
    plt.xlim((-1.5*maxi,1.5*maxi))
    plt.ylim((-1.5*maxi,1.5*maxi))
    plt.title("Circle of Correlations")
    plt.savefig('../corr_%s/%s_circle_dim_%s_%s.svg' % (file_name, vrange, dim1, dim2), format = 'svg')
    plt.close()

def myPCA(df, vrange, file_name):
    # Normalize data
    print df
    print df.mean()
    print df - df.mean()
    df_norm = (df - df.mean()) / df.std()
    # PCA
    pca = PCA(n_components='mle')
    pca_res = pca.fit_transform(df_norm.values)
    # Ebouli
    variance_ratio = pca.explained_variance_ratio_
    ebouli = pd.Series(variance_ratio)
    ebouli.plot(kind='bar', title="Eboulis des valeurs propres")
    plt.savefig('../corr_%s/%s_variances.svg' % (file_name, vrange), format = 'svg')
    plt.close()
    # Circle of correlations
    # http://stackoverflow.com/a/22996786/1565438
    components = pca.components_
    with open('../corr_%s/%s_axes.csv' % (file_name, vrange), 'w') as file_axes:
        csv_writer = csv.writer(file_axes, delimiter = ';')
        csv_writer.writerow([''] + range(1,31))
        i = 0
        for axe in components:
                csv_writer.writerow([round(100*variance_ratio[i], 1)] + [round(x, 2) for x in axe])
                i += 1
    coef = np.transpose(components)
    cols = ['PC-'+str(x+1) for x in range(len(ebouli))]
    pc_infos = pd.DataFrame(coef, columns=cols, index=[x.split('_')[-1] for x in df_norm.columns])

    dat = pd.DataFrame(pca_res, columns=cols)

    # Print HTML file with motifs on axes
    with open('../corr_%s/%s_axes.html' % (file_name, vrange), 'w') as html_file:
        html_file.write(
'<!DOCTYPE html> \n \
<html> \n \
\n \
<head> \n \
   <style> \
       section.liste { \
           float: left; \
           margin-left: 30px;  \
       } \
       ul {  \
           list-style: none;  \
       } \
       li { \
           margin-top: 10px; \
       } \
       img {  \
           width: 50px;  \
       }  \
 </style>  \
 \
</head> \n \
\n \
<body> \n \
\n \
    <section class="motifs"> \n'
        )
        for dimension in [x+1 for x in range(4)]:
            if dimension == 4 and 'motifs' in file_name:
                continue
            html_file.write('        <section class="liste">\n')
            html_file.write('        <h2>Dimension %s</h2><ul> \n' % dimension)
            info_current_dim = pc_infos['PC-%s' % dimension].copy()
            info_current_dim.sort_values(inplace = True)
            i = 0
            for pattern in info_current_dim.index.values:
                if len(pattern) == 1:
                    html_file.write('        <li><img src="../PATTERNS/pattern0%s.svg" alt="pattern %s"> %s</li>\n' % (pattern, pattern, round(info_current_dim[pattern], 2)))
                else:
                    html_file.write('        <li><img src="../PATTERNS/pattern%s.svg" alt="pattern %s"> %s</li>\n' % (pattern, pattern, round(info_current_dim[pattern], 2)))
                i += 1
            html_file.write('        </section></ul>\n')
        html_file.write('    </section>\n')
        html_file.write('</body>\n')
        html_file.write('</html>')

    for dimensions in [(1,2), (1,3), (1,4)]:

        #Plot correlation circle
        if dimensions == (1,4) and 'motifs' in file_name:
            continue

        circleOfCorrelations(pc_infos, ebouli, dimensions)

        # Plot PCA
        plt.scatter(dat["PC-%s" % str(dimensions[0])] ,dat["PC-%s" % str(dimensions[1])])
        plt.xlabel("PC-%s (%s%%)" % (dimensions[0], str(ebouli[dimensions[0]-1])[:4].lstrip("0.")))
        plt.ylabel("PC-%s (%s%%)" % (dimensions[1], str(ebouli[dimensions[1]-1])[:4].lstrip("0.")))
        plt.title("PCA")
        plt.savefig('../corr_%s/%s_PCA_dim_%s_%s.svg' % (file_name, vrange, dimensions[0], dimensions[1]), format = 'svg')
        plt.close()

    return pc_infos, ebouli, dat


if __name__ == '__main__':
#    for origin in ['motifs', 'representativity']:
    for origin in ['representativity']:
#        for plus in ['', '_plus']:
        for plus in ['_plus']:
            file_name = '%s%s' % (origin, plus)
            df = pd.read_csv('../Data/%s.csv' % file_name, sep = ';')
            df.drop('ego_id', 1, inplace = True)

#            for diff_sizes in [(0,0), (0,50), (50,100), (100,150), (150,300), (300,500), (500,1000), (1000,10000)]:
            for diff_sizes in [(0,0)]:
                minsize, maxsize = diff_sizes
                if not minsize == maxsize:
                    df2 = df[df.nb_edges.isin(range(minsize, maxsize))]
                else:
                    df2 = df.copy()

                vrange = '%s_%s' % (minsize, maxsize) if not minsize == maxsize else 'all'

                # PCA
                pc_infos, eboulis, dat = myPCA(df2, vrange, file_name)
                dat.to_csv(path_or_buf='../corr_%s/PCA_plot_%s.csv' % (file_name, vrange), sep=';')



