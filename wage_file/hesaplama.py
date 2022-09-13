from distutils.core import run_setup
from encodings import utf_8
import unicodedata

kullanici = input("Kullanıcı adı: ")
brut = float(input("Brut maasinizi giriniz: "))
kontrolluk = 2.5  # float(input("Odenecek olan kontrolluk ucreti(kac brut tutarinda)?: "))
zam = float(input("Temmuz zammini yuzde olarak giriniz: "))
ozel_sigorta = float(input("varsa özel sağlık sigortası primini giriniz(yoksa 0 giriniz): "))
sendika = input("Sendika durumu (e/h): ")
# aile = input ("esi calismayan(e), esi calismayan ve tek cocuk icin (e1), esi calismayan ve 2 cocuk icin (e2),esi calismayan ve 3+ cocuk icin (e3), bekarlar icin(b) giriniz:")
# k_taksit = int(input("kontrolluk taksit sayisi: "))
# k_donem= input("kontrolluk donemlerini bosluk birakarak sayi olarak giriniz: ")
# k_list=k_donem.split(' ')
# donem1, donem2 = k_list

odemeler = {}
liste = []


# class Aile():
#     def __init___(self,aile):
#         self.aile = aile


class Sgk():
    def __init__(self, brut, ozel_sigorta=0):
        self.brut = brut
        self.prim_orani = 0.14
        self.iprim_orani = 0.01
        self.ozel_sigorta = ozel_sigorta
        self.matrah = self.Matrah()

    def Prim(self):
        sgk_primi = self.brut * self.prim_orani
        sgk_primi = round(sgk_primi, 2)
        return sgk_primi

    def Iprim(self):
        i_primi = self.brut * self.iprim_orani
        i_primi = round(i_primi, 2)
        return i_primi

    def Matrah(self):
        matrah = self.brut - (self.Iprim() + self.Prim() + self.ozel_sigorta)
        matrah = round(matrah, 2)
        return matrah


class Vergi():
    kumulatif_matrah = 0
    toplam_vergi = 0

    def __init__(self, burut, matrah, sendika_katsayi, m, sendika, ozel_sigorta=0):
        self.burut = round(burut, 2)
        self.sendika = sendika
        self.sendika_katsayi = sendika_katsayi
        self.sendika_aidati = self.sendika_aidati()
        self.matrah = (round(matrah, 2) - self.sendika_aidati)
        self.m = m
        self.ozel_sigorta = ozel_sigorta
        self.kum_matrah()
        self.damga = self.damga_hesapla()
        self.gelir_vergisi = self.vergi_hesapla()
        self.odenecek_vergi = self.gelir_vergisi - self.vergi_iadesi()
        self.vergi_sonrasi_ucret = self.vergi_sonrasi()

    def kum_matrah(self):
        Vergi.kumulatif_matrah += self.matrah

    def sendika_aidati(self):
        if self.sendika == "e":
            aidat = self.burut / 200
        else:
            aidat = 0
        return aidat

    def damga_hesapla(self):
        if self.m == 1:
            damga = (self.burut - 5004) * 0.00759
        else:
            damga = self.burut * 0.00759
        damga = round(damga, 2)
        return damga

    def vergi_hesapla(self):
        if Vergi.kumulatif_matrah < 32000:
            vergi = self.matrah * 0.15
        elif Vergi.kumulatif_matrah < 70000:
            if (Vergi.kumulatif_matrah - self.matrah) > 32000:
                vergi = self.matrah * 0.20
            else:
                miktar = (Vergi.kumulatif_matrah - 32000)
                vergi = miktar * 0.20 + (self.matrah - miktar) * 0.15
        elif Vergi.kumulatif_matrah < 250000:
            if (Vergi.kumulatif_matrah - self.matrah) > 70000:
                vergi = self.matrah * 0.27
            else:
                miktar = (Vergi.kumulatif_matrah - 70000)
                vergi = miktar * 0.27 + (self.matrah - miktar) * 0.20
        elif Vergi.kumulatif_matrah < 880000:
            if (Vergi.kumulatif_matrah - self.matrah) > 250000:
                vergi = self.matrah * 0.35
            else:
                miktar = (Vergi.kumulatif_matrah - 250000)
                vergi = miktar * 0.35 + (self.matrah - miktar) * 0.27
        else:
            if (Vergi.kumulatif_matrah - self.matrah) > 880000:
                vergi = self.matrah * 0.40
            else:
                miktar = (Vergi.kumulatif_matrah - 880000)
                vergi = miktar * 0.40 + (self.matrah - miktar) * 0.35
        return vergi

    def vergi_iadesi(self):
        if self.m == 1:
            vergi_iade = 638.01
        else:
            vergi_iade = 0
        return vergi_iade

    def vergi_sonrasi(self):
        if self.sendika_katsayi == 1 and self.sendika == "e":
            toplu_soz = 487.33
        else:
            toplu_soz = 0
        vsucret = self.matrah - self.odenecek_vergi - self.damga + self.ozel_sigorta + self.sendika_aidati + toplu_soz
        # Vergi.toplam_vergi += self.odenecek_vergi + self.damga
        vsucret = round(vsucret, 2)
        return vsucret


def detay_goster(brut, odeme, vergi):
    detay = {"net ucret": vergi.vergi_sonrasi_ucret, "Brut ucret": brut, "Sgk primi": odeme.Prim(),
             "issizlik primi": odeme.Iprim(), "Ozel sigorta GVI": odeme.ozel_sigorta,
             "Gelir vergisi matrahi": vergi.tax_base,
             "Gelir vergisi": vergi.gelir_vergisi, "auvi": vergi.vergi_iadesi(), "odenecek vergi": vergi.odenecek_vergi,
             "damga vergisi": vergi.damga, "Vergi sonrasi ucret": vergi.vergi_sonrasi_ucret,
             "kumulatif vergi matrahi": vergi.cumulative_tax_base
             }
    return detay


fark_brut = (brut - (brut / 1.305)) * (14 / 30)

for i in range(1, 13):
    if i % 3 == 1:
        sendika_katsayi = 1
    else:
        sendika_katsayi = 0
    if i == 7:
        brut += brut * zam / 100
        brut = round(brut, 2)
    if i == 2 or i == 3:
        k_burut = brut * kontrolluk / 2
        odeme_ismi = "KONTROLLUK" + str((i - 1))
        kont = Sgk(k_burut)
        vergi_matrahi = kont.matrah
        k_vergi = Vergi(k_burut, vergi_matrahi, 0, 0, sendika="h")
        liste += [k_vergi.vergi_sonrasi()]
        odemeler[odeme_ismi] = detay_goster(k_burut, kont, k_vergi)
    if i % 3 == 1:
        odeme_ismi = "IKRAMIYE" + str(int((i + 2) / 3))
        ikramiye = Sgk(brut)
        vergi_matrahi = ikramiye.matrah
        i_vergi = Vergi(brut, vergi_matrahi, 0, 0, sendika="h")
        liste += [i_vergi.vergi_sonrasi()]
        odemeler[odeme_ismi] = detay_goster(brut, ikramiye, i_vergi)
    if i == 1:
        odeme_ismi = "Maas Farki Ocak"
        fark = Sgk(fark_brut)
        vergi_matrahi = fark.matrah
        f_vergi = Vergi(fark_brut, vergi_matrahi, 0, 0, sendika="h")
        liste += [f_vergi.vergi_sonrasi()]
        odemeler[odeme_ismi] = detay_goster(fark_brut, fark, f_vergi)
    if i == 7:
        fark_brut = (brut - (brut / 1.305)) * (44 / 30)
        odeme_ismi = "Maas Farki Temmuz"
        fark = Sgk(fark_brut)
        vergi_matrahi = fark.matrah
        f_vergi = Vergi(fark_brut, vergi_matrahi, 0, 0, sendika="h")
        liste += [f_vergi.vergi_sonrasi()]
        odemeler[odeme_ismi] = detay_goster(fark_brut, fark, f_vergi)
    odeme_ismi = "MAAS" + str(i)
    maas = Sgk(brut, ozel_sigorta)
    vergi_matrahi = maas.matrah
    m_vergi = Vergi(brut, vergi_matrahi, sendika_katsayi, 1, sendika, ozel_sigorta)
    liste += [m_vergi.vergi_sonrasi()]
    odemeler[odeme_ismi] = detay_goster(brut, maas, m_vergi)

import json

dosya = kullanici + ".txt"
with open(dosya, "w") as file:
    yil_sonu_net_toplam = 0
    toplam_vergi = 0
    for i in odemeler:
        satir = odemeler[i]
        file.write(i + ":\n")
        file.write('(kumulatif vergi matrahi= ' + str(odemeler[i]["kumulatif vergi matrahi"]) + ")\n")
        # for yari in satir:
        #     if yari == "Gelir vergisi matrahi" or yari == "Vergi sonrasi ucret":
        #          file.write("\n")
        #     file.write(json.dumps(yari))
        #     file.write(":")
        #     file.write(json.dumps(satir[yari]))
        #     file.write("\t\t")
        file.write(json.dumps(satir))
        file.write("\n\n")
        yil_sonu_net_toplam += odemeler[i]["net ucret"]
        toplam_vergi += odemeler[i]["odenecek vergi"]
    file.write("\n\nYil Sonu Toplam Net Ucret = " + str(yil_sonu_net_toplam))
    file.write("\nYil Sonu Toplam Vergi = " + str(Vergi.toplam_vergi))


