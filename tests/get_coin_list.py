
import cryptocompare
import requests, json

# Available Coin List
data = cryptocompare.get_coin_list(format=False)
df = pd.DataFrame.from_dict(data, orient='index')

df['WeissRating'] = df.Rating.apply(lambda x: x['Weiss']['Rating'])
df['TechnologyAdoptionRating'] = df.Rating.apply(lambda x: x['Weiss']['TechnologyAdoptionRating'])
df['MarketPerformanceRating'] = df.Rating.apply(lambda x: x['Weiss']['MarketPerformanceRating'])
df['Access'] = df.Taxonomy.apply(lambda x: x['Access'])
df['FCA'] = df.Taxonomy.apply(lambda x: x['FCA'])
df['FINMA'] = df.Taxonomy.apply(lambda x: x['FINMA'])
df['Industry'] = df.Taxonomy.apply(lambda x: x['Industry'])
df['CollateralizedAsset'] = df.Taxonomy.apply(lambda x: x['CollateralizedAsset'])
df['CollateralizedAssetType'] = df.Taxonomy.apply(lambda x: x['CollateralizedAssetType'])
df['CollateralType'] = df.Taxonomy.apply(lambda x: x['CollateralType'])
df['CollateralInfo'] = df.Taxonomy.apply(lambda x: x['CollateralInfo'])

del df['Rating']
del df['Taxonomy']

if not os.path.exists('../data/cryptocompare_metadata.csv'):
    df.to_csv(f'../data/cryptocompare_metadata.csv', index=True)
