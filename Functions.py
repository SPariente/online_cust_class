def factors(n):
    
    '''
    Fonction donnant la décomposition en facteurs premiers d'un entier n.
    '''
    
    result = []
    
    for i in range(2,n+1):
        
        while n/float(i) == int(n/float(i)):
            n = n/float(i)
            result.append(i)
        
        if n == 1:
            return result

        
def get_n_rowcol(fields):
    
    '''
    Fonction définissant un nombre de lignes et colonnes pour un plot, de manière à distribuer les variables contenues dans 'field'.
    '''
    
    n_fields = len(fields)
    
    n_factors = factors(n_fields)
    
    nrow = 1
    ncol = 1

    for i in range (0,len(n_factors)):
        val = n_factors[-(i+1)]

        #Nombre de lignes doit être >= au nombre de colonnes
        if ncol*val > nrow :
            nrow = nrow*val
        else:
            ncol = ncol*val

    return nrow, ncol


def map_indicator(data_lat, data_long, anchor_coords, map_kwargs, circle_kwargs):
    
    import folium
        
    site_map = folium.Map(location=anchor_coords, **map_kwargs)

    for lat, lon in zip(data_lat, data_long):
        folium.Circle(
            [lat, 
             lon],
            **circle_kwargs).add_to(site_map)
        
    return site_map


def cat_imputer(data, na_field, cat_field, imputed_data):
        
    '''
    Fonction d'imputation par catégorie de valeurs manquantes.
    
    Paramètres:
    -----------
    - data : base de données
    - na_field : colonne contenant la variable dont les valeurs manquantes sont à imputer
    - cat_field : colonne contenant la variable catégorielle à utiliser pour l'imputation par catégorie
    - imputed_data : base de données unidimensionnelle contenant les valeurs d'imputation par catégorie, indexées par le nom de la catégorie telle qu'elle apparaît dans la colonne cat_field
    
    Résultat:
    ---------
    Itérable de même dimension que data.shape[0] contenant les données de na_field après imputation des valeurs manquantes
    '''
    import numpy as np
    
    assert np.shape(imputed_data)[1] == 1, "L'élément 'imputed_data' ne doit comporter qu'une colonne et un index."
    
    data = data.copy()
    
    for i in data.index:
        
        try:
            
            if np.isnan(data.at[i,na_field]):
                try: 
                    data.at[i,na_field] = imputed_data.iloc[:,0].at[data.at[i,cat_field]]

                except KeyError:
                    data.at[i,na_field] = None
                    
        except KeyError:
            raise KeyError(f"La variable {na_field} ne se trouve pas dans la base de données.")
                
    return data[na_field]
    

def plot_centroid_coords(data, var_names = None, palette = None):
    
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    #Transformation des données en 3 colonnes : index (classe), variable, et value (coordonnées)
    data = data.reset_index().melt(id_vars = 'index')
    
    fig, ax = plt.subplots(figsize = (15,10))

    sns.lineplot(
        data = data,
        x = 'variable',
        y = 'value',
        hue = 'index',
        palette = palette
    )

    ax.grid(visible = True, axis = 'x', color = 'darkgrey')
    ax.grid(visible = True, axis = 'y', color = 'lightgrey')
    ax.set_axisbelow(True)

    ax.set_xlim(left = data['variable'][0], right = data['variable'][-1:])

    ax.set_xlabel('Variable')
    ax.set_ylabel('Coordonnée du centroïde (standardisée)')
    ax.set_title('Visualisation des coordonnées des centroïdes')
    
    if var_names is not None:
        ax.set_xticks(data['variable'].unique(), var_names)

    ax.legend(title = 'Catégorie')

    return fig