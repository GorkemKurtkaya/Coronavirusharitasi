import pandas
import folium

veri=pandas.read_excel("world_coronavirus_cases.xlsx")

enlemler=list(veri["Enlem"])
boylamlar=list(veri["Boylam"])
toplamvaka=list(veri["Toplam Vaka"])
vefatlar=list(veri["Vefat Edenler"])
aktifler=list(veri["Aktif Vakalar"])
nufus=list(veri["Nüfus"])
toplamtest=list(veri["Toplam Test"])



vaka_sayisi_haritasi = folium.FeatureGroup(name="Toplam Vaka Sayısı Haritası")
olum_orani_haritasi= folium.FeatureGroup(name="Ölüm Oranı Haritası")
aktif_vaka_haritasi= folium.FeatureGroup(name="Aktif Vaka Haritası")
test_orani_haritasi=folium.FeatureGroup(name="Toplam Test Oranı Haritası")
nufus_dagılım_haritasi=folium.FeatureGroup(name="Nüfus Dağılım Haritası")


def vaka_sayisi_renk(vaka):
    if vaka<100000:
        return "green"
    elif vaka<300000:
        return "white"
    elif vaka<750000:
        return "orange"
    else:
        return "red"


def vaka_sayisi_radius(vaka):
    if vaka < 100000:
        return 20000
    elif vaka < 300000:
        return 50000
    elif vaka < 750000:
        return 100000
    else:
        return 200000

def olum_orani_radius(vaka,vefat):
    if (vefat/vaka)*100 <2.5:
        return 20000
    elif (vefat/vaka)*100 <5:
        return 50000
    elif (vefat/vaka)*100 <7.5:
        return 100000
    else:
        return 200000


def olum_orani_renk(vaka,vefat):
    if (vefat/vaka)*100 <2.5:
        return "green"
    elif (vefat/vaka)*100 <5:
        return "white"
    elif (vefat/vaka)*100 <7.5:
        return "orange"
    else:
        return "red"

def aktif_vaka_renk(aktif):
    if aktif < 100000:
        return "green"
    elif aktif < 300000:
        return "white"
    elif aktif < 750000:
        return "orange"
    else:
        return "red"

def aktif_vaka_radius(aktif):
    if aktif < 100000:
        return 20000
    elif aktif < 300000:
        return 150000
    elif aktif < 750000:
        return 250000
    else:
        return 400000

def test_orani_radius(nufus,test):
    if (test/nufus)*100 <2.5:
        return 20000
    elif (test/nufus)*100 <5:
        return 50000
    elif (test/nufus)*100 <7.5:
        return 250000
    else:
        return 400000

def test_orani_renk(nufus,test):
    if (test / nufus) * 100 < 2.5:
        return "red"
    elif (test / nufus) * 100 < 5:
        return "orange"
    elif (test / nufus) * 100 < 7.5:
        return "white"
    else:
        return "green"

world_map=folium.Map(tiles="Cartodb dark_matter")


for enlem,boylam,vaka in zip(enlemler,boylamlar,toplamvaka):
    vaka_sayisi_haritasi.add_child(folium.Circle(location=(enlem,boylam), radius=vaka_sayisi_radius(vaka),
                                      color=vaka_sayisi_renk(vaka),
                                      fill_color=vaka_sayisi_renk(vaka),
                                      fill_opacity=0.3))

for enlem,boylam,vaka,vefat in zip(enlemler,boylamlar,toplamvaka,vefatlar):
    olum_orani_haritasi.add_child(folium.Circle(location=(enlem,boylam),radius=olum_orani_radius(vaka, vefat),
                                      color=olum_orani_renk(vaka,vefat),
                                      fill_color=olum_orani_renk(vaka,vefat),
                                      fill_opacity=0.3))

for enlem,boylam,aktif in zip(enlemler,boylamlar,aktifler):
    aktif_vaka_haritasi.add_child(folium.Circle(location=(enlem,boylam),
                                      radius=aktif_vaka_radius(aktif),
                                      color=aktif_vaka_renk(aktif),
                                      fill_color=aktif_vaka_renk(aktif),
                                      fill_opacity=0.3))


for enlem,boylam,ulke_nufus,test in zip(enlemler,boylamlar,nufus,toplamtest):
    test_orani_haritasi.add_child(folium.Circle(location=(enlem,boylam),
                                      radius=test_orani_radius(ulke_nufus,test),
                                      color=test_orani_renk(ulke_nufus,test),
                                      fill_color=test_orani_renk(ulke_nufus,test),
                                      fill_opacity=0.3))

nufus_dagılım_haritasi.add_child(folium.GeoJson(data=(open("world.json", "r",
                                        encoding="utf-8-sig").read()),
                                        style_function=lambda x:{'fillColor':'green'
                                        if x["properties"]["POP2005"] <20000000 else
                                        'white' if 20000000 <=x["properties"]["POP2005"] <=50000000
                                        else 'orange' if 50000000 <=x["properties"]["POP2005"]<=100000000
                                        else 'red'}))


world_map.add_child(vaka_sayisi_haritasi)
world_map.add_child(olum_orani_haritasi)
world_map.add_child(aktif_vaka_haritasi)
world_map.add_child(test_orani_haritasi)
world_map.add_child(nufus_dagılım_haritasi)


world_map.add_child(folium.LayerControl())


world_map.save("world_map.html")