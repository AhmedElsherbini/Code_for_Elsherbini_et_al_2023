#import lib
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from utils import *


def PCA_model(f_name):
    data, x, y1, y2, _, t1, t2, _ = load_train_data(f_name)
    x = StandardScaler().fit_transform(x)
    pca = PCA(n_components=2)
    colors = ['r','g','y','b','c','k','#f48ec5','#f48ec5','#c670c0','#a71db2','#f40efa','#4b34ca','#fa7d66','#37b0a4','#beda3f','#c52553','#ac6895','#7ca77b','#66d0ee','#06c405','#2b97c2','#292927','#1d9375','#e3ec51','#7dfe45','#f48f84','#6df17a','#2470d0','#a0f4a0','#7380b9','#c31bd0','#9be737','#445397','#12c693','#9a853f','#070740','#a65530','#e637a5','#b23399','#a29316','#a0ebe0','#ef955c','#f7b512','#a062a4','#ce6a1c','#e2e7fa','#8a26d5','#e3fe76','#adf8e6','#12dfde','#ae653b','#82a36c','#416d7e','#a5d12e','#e4815c','#d95602','#9a6616','#3029d2','#532c7f','#528525','#51eff3','#fb234f','#d13750','#cd0135','#e24c95','#c507b6','#e20241','#2f90df','#36f5d0','#cfb087','#970826','#fa5265','#4241f1','#346331','#b79c2e','#d56f1d','#fad7f5','#6d2f1b','#e0e8b1','#261d62','#00e899','#4e6cfb','#77bdc4','#aa1c5c','#ccd9a0','#fad2bc','#cd746b','#71bca7','#45c442','#68aa78','#046d99','#d0fd75','#0ca4d9','#73db67','#14401c','#17c915','#17bad5','#c3b9fb','#c7a7a5','#fd3ae7','#b17f7b','#174b9e','#a8a3fd','#f3a354','#587d92','#4d752b']    
    p_Components = pca.fit_transform(x)
    pc_df = pd.DataFrame(p_Components, columns = ['pc1', 'pc2'])
    y = pd.DataFrame(np.asarray(y1), columns= ['class'])
    finalDf = pd.concat([pc_df, y[['class']]], axis = 1)
    plot_2d_pca(pca, finalDf, t1, f_name= 'Clade' ,c= colors)

    y = pd.DataFrame(np.asarray(y2), columns= ['class'])
    finalDf = pd.concat([pc_df, y[['class']]], axis = 1)
    plot_2d_pca(pca, finalDf, t2, f_name='Cont')
