import pandas as pd
#import openpyxl #intended to be used to retrieve row number when we should startreading DF

COLUMN_NAME: str = "Kwota"

def Load_data(link_to_source_file = 'C:/Users/njvtwk/Downloads/lista_operacji_txt.csv'):

    df =  pd.read_csv(link_to_source_file, index_col= False, skiprows=25, decimal=',' , sep = ';' , encoding='utf-8', on_bad_lines='warn')#, names = ['Data operacji','Opis operacji','Rachunek','Kategoria','Kwota'])
    #index_col = False inform that we don't want to use one of collumns as index list (this one mostly on left 0,1.....)

    df.reset_index()# indexing field again

    #COLUMN'S ORDERING string's in content
    df.columns = [x.replace('#','') for x in df.columns] #This code removing from column name '#'
    df[COLUMN_NAME] = df[COLUMN_NAME].str.replace("PLN", '')#Removing PLN
    df[COLUMN_NAME].replace(to_replace=' ', value='', inplace = True)#Removing Whitespace (we could use strip to remove whitespace)
    df[COLUMN_NAME].replace(to_replace=',', value='.', inplace = True)#Changing From USA system to Europenin (it os posisble to do as well  in settings of readCSV)



    print("New DF will be printed")
    print(df.head())
    print(df["Kwota"])
    #new_df = df.applymap(lambda x: str(x.replace(',','.'))) #special function what map
    df['Kwota'] = df[COLUMN_NAME].str.replace(',', '.')
    df[COLUMN_NAME] = df[COLUMN_NAME].str.replace(' ', '')
    print(df[COLUMN_NAME])
    print(df.replace(to_replace=',',value='.', inplace=True))

    print(df[COLUMN_NAME])



    print(type(df.loc[1,COLUMN_NAME]))
    #df[column_name] = df[column_name].astype(float)
    df[COLUMN_NAME] = pd.to_numeric(df[COLUMN_NAME])
    print(type(df.loc[1,COLUMN_NAME]))
    df[COLUMN_NAME] = df[COLUMN_NAME] * -1



    #Quering across teh data
    print("QUERING DATA in Pandas")
    print(df[(df['Kwota'] > 1000) & (df['Kwota'] < 2000)])

    print(df.head())
    print(int(df.shape[0]))
    print(int(df.shape[1]))
    #for i in range(df.shape[0]):
    #   for j in range(df.shape[1]):
    print(df.iloc[0][5])
    return df

#Load_data()