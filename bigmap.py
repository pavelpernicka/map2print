#!python3

import io, datetime, time, re, random, requests, math, os
from PIL import Image, ImageDraw

(zoom, ymin, xmin, ymax, xmax) = (14, 18.039551,49.197634,18.176880,49.268925)
#layers = ["http://{abc}.tile.openstreetmap.fr/osmfr/!z/!x/!y.png"]
layers = ["https://mapserver.mapy.cz/turist-m/!z-!x-!y"]
# formula from https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
def deg2num(lat_deg, lon_deg, zoom):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
  return (xtile, ytile)
  
(xminc, yminc) = deg2num(xmin, ymin, zoom)
(xmaxc, ymaxc) = deg2num(xmax, ymax, zoom)
xsize = xmaxc - xminc + 1
ysize = yminc - ymaxc + 1
print("X: {} - {}".format(xminc, xmaxc))
print("Y: {} - {}".format(ymaxc, yminc))

imglist = []
if(xsize > ysize):
    for x in range(xminc-1, xmaxc+1):
        for y in range(ymaxc-1, yminc+1):
            imglist.append((x, y))
else:
    for y in range(ymaxc-1, yminc+1):
        for x in range(xminc-1, xmaxc+1):
            imglist.append((x, y))
	
print("Must download: {} images".format(len(imglist)))

resultImage = Image.new("RGBA", (xsize * 256, ysize * 256), (0,0,0,0))
counter = 0
for i in imglist:
    (x, y) = i
    for layer in layers:
         url = layer.replace("!x", str(x)).replace("!y", str(y)).replace("!z", str(zoom))
         match = re.search("{([a-z0-9]+)}", url)
         if match:
             url = url.replace(match.group(0), random.choice(match.group(1)))
         print("({}/{}): {}...".format(counter+1, len(imglist), url));
         try:
             resp = requests.get(url)
         except Exception as e:
             print("Error", e)
             continue;
         image = Image.open(io.BytesIO(resp.content))
         resultImage.paste(image, ((x-xminc)*256, (y-ymaxc)*256), image.convert("RGBA"))
         counter += 1

now = datetime.datetime.now()
outputFileName = "map%02d-%02d%02d%02d-%02d%02d" % (zoom, now.year % 100, now.month, now.day, now.hour, now.minute)
outputFileNamePng = "gen/" + outputFileName + ".png"
resultImage.save(outputFileNamePng)
os.system("mkdir gen/{}".format(outputFileName))
os.system("convert {} -crop 5x4+100+100@  +repage  +adjoin  gen/{}/map_%d.png".format(outputFileNamePng, outputFileName))
os.system("convert gen/{}/*.png gen/{}.pdf".format(outputFileName, outputFileName))

os.system("tar -czvf gen/{}.tar.gz gen/{}".format(outputFileName, outputFileName))
os.system("rm -r gen/{}".format(outputFileName))