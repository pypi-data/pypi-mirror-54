#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

import imageio
import moviepy

from moviepy.editor import ImageSequenceClip

#fonction pour voir les dechets en France selon les annees voulues

def plot_geo_time_value(x, y, df, lim_metropole = [-5, 10, 41, 52], years=[2003,2005,2007,2009], filename = None):
    
    fig, axs = plt.subplots(2, 2, figsize=(20,15), subplot_kw={'projection': ccrs.PlateCarree()})
        
    i = 0
    j = 0
    
    for k in years :
        colonne = 'Quantite' + str(k)
        axs[i,j].plot()
        axs[i,j].set_extent(lim_metropole)
        axs[i,j].add_feature(cfeature.OCEAN.with_scale('50m'))
        axs[i,j].add_feature(cfeature.COASTLINE.with_scale('50m'))
        axs[i,j].add_feature(cfeature.RIVERS.with_scale('50m'))
        axs[i,j].add_feature(cfeature.BORDERS.with_scale('50m'), linestyle=':')
        axs[i,j].scatter(x, y,
                   s=df[colonne] ** 0.5 / 5, alpha=0.5)
        axs[i,j].set_title('France ' + str(k) + '\nproduction de produits dangereux');
        if i == 0:
            i += 1
        elif i == 1 and j == 0 :
            (i,j) = (j,i)
        else : 
            i = 1
            j = 1
            
    fig.savefig(filename)
    return(i,j)

#Fonction pour creer les images (a enregistrer sous le nom de l'annee (par exemple 2003)) une par une pour creer le gif

def plot_geo_time_value_une_image(x, y, df, lim_metropole = [-5, 10, 41, 52], years=[2004], filename = None):
    
    fig, axs = plt.subplots(1,1, figsize=(20,15), subplot_kw={'projection': ccrs.PlateCarree()})
    
    for k in years :
        colonne = 'Quantite' + str(k)
        axs.plot()
        axs.set_extent(lim_metropole)
        axs.add_feature(cfeature.OCEAN.with_scale('50m'))
        axs.add_feature(cfeature.COASTLINE.with_scale('50m'))
        axs.add_feature(cfeature.RIVERS.with_scale('50m'))
        axs.add_feature(cfeature.BORDERS.with_scale('50m'), linestyle=':')
        axs.scatter(x, y,
                   s=df[colonne] ** 0.5 / 5, alpha=0.5)
        axs.set_title('France ' + str(k) + '\nproduction de produits dangereux');

    fig.savefig(filename)
    
#fonction pour creer le gif, path pour dire ou sont les images, annnee deb et annee fin pour debut et fin des annees () et giffile pour le nom du fichier
    
def gif(path = 'C:/Users/Philmedion/Desktop/projet python dataviz 2A/images/', annee_deb = 2003, annee_fin = 2006, giffile = 'demo.gif'):
    
    images_data = []
    #load les images
    for i in range(int(annee_deb),int(annee_fin)):
        data = imageio.imread(path+str(i)+'.png')
        images_data.append(data)

    imageio.mimwrite(giffile, images_data, format= '.gif', fps = 1)

