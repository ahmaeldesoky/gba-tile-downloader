# GBA Tile Downloader

This script automates downloading the [GlobalBuildingAtlas LoD1](https://github.com/zhu-xlab/GlobalBuildingAtlas) building tiles version hosted on [Source Cooperative](https://source.coop/tge-labs/globalbuildingatlas-lod1) for a designated polygon (`.gpkg`), clips them to that polygon, and saves the result.

> ⚠️ Check the [Terms of Use](https://tubvsig-so2sat-vm1.srv.mwn.de/terms_of_use.html) and the [License Notice](https://github.com/zhu-xlab/GlobalBuildingAtlas?tab=readme-ov-file#license-notice) before reusing or publishing the downloaded data, and make sure to cite both the [original dataset](https://doi.org/10.14459/2025mp1782307) and the [Parquet version](https://source.coop/tge-labs/globalbuildingatlas-lod1).

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python download_tiles.py
```
