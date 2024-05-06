import numpy as np
import cv2

img = cv2.imread('./dublin.jpg')
img2 = cv2.imread('./dublin_edited.jpg')

wyskokosc, szerokosc, kolor_rgb = img.shape
roznice = np.zeros((wyskokosc, szerokosc), dtype=np.uint8)

roznica_b =0
roznica_g =0
roznica_r =0
wiz_roznice = np.zeros((wyskokosc,szerokosc,kolor_rgb), dtype=np.uint8)
for i in range(wyskokosc):
    for j in range(szerokosc):
        roznica_b = np.abs(int(img[i, j, 0]) - int(img2[i, j, 0]))
        roznica_g = np.abs(int(img[i, j, 1]) - int(img2[i, j, 1]))
        roznica_r = np.abs(int(img[i, j, 2]) - int(img2[i, j, 2]))

        if roznica_r < 20 and roznica_g < 20 and roznica_b < 20:
            roznice[i, j] = 0
        else:
            roznice[i, j] = 1

for i in range(1, wyskokosc-1):
    for j in range(1, szerokosc-1):
        if roznice[i, j] + roznice[i-1, j-1] +roznice[i-1, j] + roznice[i-1, j+1] + roznice[i, j-1] + roznice[i, j+1] + roznice[i+1, j-1] + roznice[i+1, j] + roznice[i+1, j+1] >= 6:
            roznice[i, j] = 1
            # wiz_roznice[i, j, 0] = 255
            # wiz_roznice[i, j, 1] = 255
            # wiz_roznice[i, j, 2] = 255
            wiz_roznice[i, j, 0] = img2[i, j, 0]
            wiz_roznice[i, j, 1] = img2[i, j, 1]
            wiz_roznice[i, j, 2] = img2[i, j, 2]
        if roznice[i, j] + roznice[i-1, j-1] +roznice[i-1, j] + roznice[i-1, j+1] + roznice[i, j-1] + roznice[i, j+1] + roznice[i+1, j-1] + roznice[i+1, j] + roznice[i+1, j+1] ==1:
            roznice[i, j] = 0

czy_sprawdzone = np.zeros((wyskokosc,szerokosc), dtype=np.uint8)
lewy = szerokosc
prawy = 0
gorny = wyskokosc
dolny = 0
ramka = []
ktory_kwvin = 0
for i in range(wyskokosc):
    for j in range(szerokosc):

        if roznice[i, j] == 1 and czy_sprawdzone[i, j] == 0 and roznice[i, j] + roznice[i-1, j-1] +roznice[i-1, j] + roznice[i-1, j+1] + roznice[i, j-1] + roznice[i, j+1] + roznice[i+1, j-1] + roznice[i+1, j] + roznice[i+1, j+1] >= 6:
            lewy = szerokosc
            prawy = 0
            gorny = wyskokosc
            dolny = 0
            ramka.append([gorny,dolny,lewy,prawy])
            for k in range(i, i+100):
                for l in range(j-50, j + 50):
                    if roznice[k, l] == 1:
                        if roznice[k-1, l] == 0 and k < gorny:
                            gorny = k
                        if roznice[k+1, l] == 0 and k > dolny:
                            dolny = k
                        if roznice[k, l+1] == 0 and l > prawy:
                            prawy = l
                        if roznice[k, l-1] == 0 and l < lewy:
                            lewy = l
                        czy_sprawdzone[k, l] = 1
                        ramka[ktory_kwvin][0] = gorny
                        ramka[ktory_kwvin][1] = dolny
                        ramka[ktory_kwvin][2] = lewy
                        ramka[ktory_kwvin][3] = prawy
            ktory_kwvin = ktory_kwvin+1

# for kewin in range(ktory_kwvin):
#     for i in range(ramka[kewin][0], ramka[kewin][1]+1):
#         for j in range(ramka[kewin][2],ramka[kewin][3]+1):
#             if i==ramka[kewin][0] or i==ramka[kewin][1] or j==ramka[kewin][2] or j==ramka[kewin][3]:
#                 wiz_roznice[i, j, 0] = 0
#                 wiz_roznice[i, j, 1] = 0
#                 wiz_roznice[i, j, 2] = 255
wysokosc_kewinka = ramka[0][1] - ramka[0][0]
szerokosc_kewinka = ramka[0][3] - ramka[0][2]
kewinek = np.zeros((wysokosc_kewinka,szerokosc_kewinka,3), dtype=np.uint8)
kewinek_beztla = np.zeros((wysokosc_kewinka,szerokosc_kewinka,4), dtype=np.uint8)

for kewin in range(ktory_kwvin):
    for i in range(ramka[kewin][0], ramka[kewin][1]+1):
        for j in range(ramka[kewin][2],ramka[kewin][3]+1):
            if i==ramka[kewin][0] or i==ramka[kewin][1] or j==ramka[kewin][2] or j==ramka[kewin][3]:
                img2[i, j, 0] = 0
                img2[i, j, 1] = 0
                img2[i, j, 2] = 255

for i in range(wysokosc_kewinka-1):
    for j in range(szerokosc_kewinka-1):
        kewinek[i, j, 0] = img2[i+ramka[0][0]+1, j + ramka[0][2]+1, 0]
        kewinek[i, j, 1] = img2[i+ramka[0][0]+1, j + ramka[0][2]+1, 1]
        kewinek[i, j, 2] = img2[i+ramka[0][0]+1, j + ramka[0][2]+1, 2]

cv2.imwrite('Kevin_z_tlem.png', kewinek)

for i in range(wysokosc_kewinka-1):
    for j in range(szerokosc_kewinka-1):
        if roznice[i+ramka[0][0]+1, j + ramka[0][2]+1] == 0:
            przezroczystosc = 0
        else:
            przezroczystosc = 255
        kewinek_beztla[i, j, 0] = wiz_roznice[i+ramka[0][0]+1, j + ramka[0][2]+1, 0]
        kewinek_beztla[i, j, 1] = wiz_roznice[i+ramka[0][0]+1, j + ramka[0][2]+1, 1]
        kewinek_beztla[i, j, 2] = wiz_roznice[i+ramka[0][0]+1, j + ramka[0][2]+1, 2]
        kewinek_beztla[i, j, 3] = przezroczystosc

print(ramka)

cv2.imwrite('Kevin_bez_tla.png', kewinek_beztla)
cv2.imwrite('Dublin_zaznaczone_Keviny.png', img2)

cv2.waitKey(0)
cv2.destroyAllWindows()



