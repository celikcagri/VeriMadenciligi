
#############################################
# PROJE ADIMLARI
#############################################

#############################################
# ADIM 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
#############################################

import pandas as pd
import numpy as np

df = pd.read_csv('datasets/persona.csv')

df.info()
df.head()
df.tail()
df.describe().T
df.columns
df.index
df.isnull().values.any()

# Soru 1: Kaç unique SOURCE vardır?

df['SOURCE'].unique()
df['SOURCE'].value_counts()

# Soru 2: Kaç unique PRICE vardır?

df.PRICE.nunique()

# Soru 3: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?

df.PRICE.value_counts()

# Soru 4: Hangi ülkeden kaçar tane satış olmuş?

df.COUNTRY.value_counts()

# Soru 5: Ülkelere göre satışlardan toplam ne kadar kazanılmış?

df.groupby('COUNTRY').agg({'PRICE': 'sum'})
# df.groupby('COUNTRY')['PRICE'].sum()

# Soru 6: SOURCE türlerine göre göre satış sayıları nedir?

df.SOURCE.value_counts()


# Soru 7: Ülkelere göre PRICE ortalamaları nedir?

df.groupby('COUNTRY').agg({'PRICE': 'mean'})

# Soru 8: SOURCE'lara göre PRICE ortalamaları nedir?

df.groupby(['SOURCE']).agg({'PRICE': 'mean'})

# Soru 9: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?

df.groupby(['SOURCE', 'COUNTRY']).agg({'PRICE': 'mean'})


#############################################
# ADIM 2: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazanç hesaplanması
#############################################
# Çıktıyı agg_df olarak kaydettik.

agg_df = df.groupby(['COUNTRY', 'SOURCE', 'SEX', 'AGE']).agg({'PRICE': 'mean'})


#############################################
# ADIM 3: Çıktıyı PRICE'a göre sıralama
#############################################


agg_df.sort_values('PRICE', ascending=False)

len(agg_df.columns)

#############################################
# ADIM 4: Indekste yer alan isimleri değişken ismine çevirme
#############################################
# Üçüncü sorunun çıktısında yer alan PRICE dışındaki tüm değişkenler index isimleridir.
# Bu isimleri değişken isimlerine çeviriyoruz.

agg_df = agg_df.reset_index()
agg_df.columns

#############################################
# ADIM 5: AGE değişkenini kategorik değişkene çevirme ve agg_df'e ekleme
#############################################

# AGE değişkeninin nerelerden bölüneceğini belirtelim:
my_bins = [0, 18, 23, 30, 40, agg_df['AGE'].max()]

# Bölünen noktalara karşılık isimlendirmelerin ne olacağını ifade edelim
mylabels = ['0_18', '19_23', '24_30', '31_40', '41_' + str(agg_df['AGE'].max())]

# age'i bölelim:
pd.cut(agg_df['AGE'], bins=my_bins, labels=mylabels)

agg_df['AGE_CAT'] = pd.cut(agg_df['AGE'], bins=my_bins, labels=mylabels)
agg_df.head()

#############################################
# ADIM 6: Yeni seviye tabanlı müşterileri tanımlama
#############################################

# CUSTOMERS_LEVEL_BASED adında bir değişken tanımladık ve veri setine bu değişkeni ekledik.

agg_df.drop(['AGE', 'PRICE'], axis=1).values

agg_df["CUSTOMERS_LEVEL_BASED"] = ["_".join(i).upper() for i in agg_df.drop(['AGE', 'PRICE'], axis=1).values]
agg_df


# Gereksiz değişkenleri çıkaralım:

agg_df.head()
agg_df = agg_df[['CUSTOMERS_LEVEL_BASED', 'PRICE']]

agg_df = agg_df.groupby('CUSTOMERS_LEVEL_BASED')['PRICE'].mean().reset_index()


#############################################
# ADIM 7: Yeni müşterileri segmentlere ayırma.
#############################################
# PRICE'a göre segmentlere ayırıyoruz
# segmentleri "SEGMENT" isimlendirmesi ile agg_df'e ekledik,

agg_df['SEGMENT'] = pd.qcut(agg_df.PRICE, q=4, labels=['D', 'C', 'B','A'])
agg_df.head()

agg_df.groupby('SEGMENT').agg({'PRICE': 'mean'}).reset_index()

#############################################
# ADIM 8: Yeni gelen müşterileri sınıflandırınız ne kadar gelir getirebileceğini tahmin ediniz.
#############################################
# 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?

new_user = 'TUR_ANDROID_FEMALE_31_40'
agg_df[agg_df['CUSTOMERS_LEVEL_BASED'] == new_user]

# 35 yaşında IOS kullanan bir Fransız kadını hangi segmente ve ortalama ne kadar gelir kazandırması beklenir?

new_user = 'FRA_IOS_FEMALE_31_40'
agg_df[agg_df['CUSTOMERS_LEVEL_BASED'] == new_user]

agg_df[agg_df['CUSTOMERS_LEVEL_BASED'] == 'BRA_ANDROID_FEMALE_0_18']


