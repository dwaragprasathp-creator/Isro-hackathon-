from pathlib import Path
import rasterio


class LandsatLoader:
    def __init__(self, data_folder="data/raw/landsat"):
        self.data_folder = Path(data_folder)
        self.scene = self._find_scene()
        self.bands = self._find_bands()

    def _find_scene(self):
        folders = [f for f in self.data_folder.iterdir() if f.is_dir()]
        if not folders:
            raise FileNotFoundError("No Landsat scene found.")
        return folders[0]

    def _find_bands(self):
        patterns = {
            "blue": "*SR_B2.TIF",
            "green": "*SR_B3.TIF",
            "red": "*SR_B4.TIF",
            "nir": "*SR_B5.TIF",
            "swir1": "*SR_B6.TIF",
            "swir2": "*SR_B7.TIF",
            "thermal": "*ST_B10.TIF",
            "qa": "*QA_PIXEL.TIF",
        }

        bands = {}

        for key, pattern in patterns.items():
            files = list(self.scene.glob(pattern))
            if not files:
                raise FileNotFoundError(f"Missing band: {key}")
            bands[key] = files[0]

        return bands

    def read(self, band):
        with rasterio.open(self.bands[band]) as src:
            return src.read(1).astype("float32"), src.profile

    def info(self):
        print("=" * 60)
        print("LANDSAT LOADER")
        print("=" * 60)
        print("Scene:", self.scene.name)

        for k, v in self.bands.items():
            print(f"{k:10} -> {v.name}")


if __name__ == "__main__":
    loader = LandsatLoader()
    loader.info()