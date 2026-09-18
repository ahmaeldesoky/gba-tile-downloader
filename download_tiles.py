import os, math, requests
import pandas as pd
import geopandas as gpd

# config
gpkg_path = "boundary.gpkg"              # replace with the path to the .gpkg file
layer = None                             # name of the layer to read, or None to use the default one
output_path = "clipped_buildings.gpkg"   # name of the output gpkg
base_url = "https://data.source.coop/tge-labs/globalbuildingatlas-lod1"
temp = "temp"                            # path to folder where downloaded tiles are temporarily saved
os.makedirs(temp, exist_ok=True)

# load boundary
print(f"Loading boundary from {gpkg_path}...")
boundary = gpd.read_file(gpkg_path, layer=layer).to_crs(epsg=4326)  # reproject to lat/lon
boundary_geom = boundary.union_all()            # merge all shapes into one, if there are multiple polygons
xmin, ymin, xmax, ymax = boundary.total_bounds  # bounding box of the boundary

# identify the 5 degree tiles that cover the boundary's bounding box
tiles = []
for west in range(math.floor(xmin / 5) * 5, math.ceil(xmax / 5) * 5, 5):
    for south in range(math.floor(ymin / 5) * 5, math.ceil(ymax / 5) * 5, 5):
        # build the tile name the server expects, e.g. "e010_n55_e015_n50"
        tiles.append(f"e{west:03d}_n{south+5:02d}_e{west+5:03d}_n{south:02d}")

print(f"Found {len(tiles)} potential tile(s): {tiles}")

# download + read + clip each tile
gdfs = []
for tile in tiles:
    url = f"{base_url}/{tile}.parquet"
    path = os.path.join(temp, f"{tile}.parquet")

    print(f"Downloading {tile}...")
    r = requests.get(url, stream=True)
    if r.status_code != 200:
        print(f"  This tile doesn't exist (status {r.status_code}) — skipping")
        continue

    # write the file to disk in small chunks (don't load it all into memory)
    with open(path, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)
    print(f"  Saved to {path}")

    gdf = gpd.read_parquet(path)
    gdfs.append(gdf)
    print(f"  Loaded {len(gdf)} buildings from {tile}")
    # os.remove(path)  # uncomment to automatically delete the raw tile after reading

if not gdfs:
    raise RuntimeError("No tiles were downloaded")

# combine + clip to roi
print("Combining tiles and clipping to boundary...")
buildings = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True))
buildings = buildings[buildings.intersects(boundary_geom)].copy()
print(f"{len(buildings)} buildings remain after clipping")

# save output
buildings.to_file(output_path, driver="GPKG")
print(f"Saved {output_path}")
