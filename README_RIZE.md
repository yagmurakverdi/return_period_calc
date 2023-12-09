RIZE Adımları
=============

1. 2026-2050 tahmin değerlerinden Rize koordinatına göre veriyi çektik
```shell
cdo remapnn,lon=40.52_lat=41.02 ../data/Turkey_MPI_85_dn_STS.2026-2050_pr_daily.nc ./out/rize-test.nc
```
2. python console'da Rize değerlerini içeri aldık
```python
import xarray as xr
rize_test = xr.open_dataset('./out/rize-test.nc')  # rize ham veri
```
3. ncw rize hesapla
```python
ncw_rize = calculate_ncw(rize_test)
```
4. ncw rize'yi dosya olarak kaydettik
```python
save_nc('NCW_2026-2050-4-wo-year-rize', ncw_rize)
```
5. tüm 25 yıl için max hesaplaması
```python
max_rize = rize_test['pr'].max(dim='time')
```
6. yıllar bazında max hesaplaması için önce yıl koordinatı ekledik
```python
rize_test_year = rize_test.assign_coords(year=rize_test['time'].dt.year)
rize_test_year['time'] = rize_test_year['time'].dt.strftime('%Y-%m-%d')
```
7. yıllar bazında max hesaplaması
```python
max_rize_year = rize_test_year['pr'].groupby('year').max(dim='time')
```
8. gev_max'ı yıllar bazında olanda çalıştırdık 
```python
rize_gev_max_year = calculate_gev_max(max_rize_year)
```
9. !!! ancak tüm yılların max'ında çalışmadı koordinatı değiştirmemize rağmen
```python
rize_gev_max = calculate_gev_max_wo_year(max_rize)
```
10. rize'ye ait csi, psi mu değerleri yıllar bazında hesaplamadan gelen
```python
rize_csi, rize_psi, rize_mu = rize_gev_max_year[0,0,:]
```
11. rize'ye ait n, c, w değerleri
```python
n_rize, c_rize, w_rize = ncw_rize[0,0,:]
```
12. hesaplanan ncw'dan rize için hmew dağılımı return_period = [1, 10, 100]
```python
hmev_rize = calculate_hmev(ncw_rize, return_period)
```
13. chatGPT dağılım fonksiyonu
```python
import numpy as np
def mev_pdf(x, N, C, W):
    # x: Yağış miktarları (numpy array veya liste)
    # N, C, W: MEV dağılım parametreleri (N: ölçek, C: konum, W: şekil)
    z = (x - C) / N  # Gumbel için z değişkeni
    return (1/N) * np.exp(-(z + np.exp(-z)))
```
14. rize yagis değerleri array olarak
```python
rize_yagis = rize_test['pr'][:,0,0].values
```
15. mev_pdf hesaplaması
```python
mev_pdf_values = mev_pdf(rize_yagis, float(n_rize), float(c_rize), float(w_rize))
```
16. mev_pdf'i çizdirme
```python
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.plot(rize_yagis, mev_pdf_values, label='MEV PDF')
plt.title('Rize Yağış Verisi ve MEV Dağılımı')
plt.xlabel('Yağış Miktarı (mm)')
plt.ylabel('Olasılık Yoğunluğu')
plt.legend()
plt.grid(True)
plt.show()
```