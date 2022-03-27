import pandas


def printAreaCountries(df):
    countries = df[['name', 'area']].sort_values('area', ascending=False)
    print(countries[:10])
    print()
    print(countries[-10:])


def printPopulationCountries(df):
    countries = df[['name', 'population']].sort_values('population', ascending=False)
    print(countries[:10])
    print()
    print(countries[-10:])


def printFrenchCountries(df):
    countries = df.loc[df['languages'] == 'French'][['name', 'languages']]
    print(countries)


def printIslandCountries(df):
    countries = df.loc[df['name'].str.contains("island", case=False)]['name']
    print(countries)


def printSouthCountries(df):
    countries = df.loc[df['subregion'].notna()]
    countries = countries.loc[countries['subregion'].str.contains("south", case=False)][['name', 'subregion']]
    print(countries)


def groupFirstCharacter(df):
    return df.groupby('name').size().reset_index()['name']


def groupPopulation(df):
    return df.groupby('population').size().reset_index()['population']


def groupArea(df):
    return df.groupby('area').size().reset_index()['area']


df = pandas.read_csv('countries.csv')
# print(groupFirstCharacter(df))

dfRes = df[['name', 'capital', 'area', 'currencies', 'latlng']]
dfRes.to_excel('countries.xlsx')
