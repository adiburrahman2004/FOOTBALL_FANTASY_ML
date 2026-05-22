import time
import random
import pandas as pd
import undetected_chromedriver as uc

options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = uc.Chrome(
   options=options,
   version_main=148,
   browser_executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
   suppress_welcome=True,
)

def flatten_columns(df):
   if isinstance(df.columns, pd.MultiIndex):
      df.columns = [
         f"{b}" if a.startswith("Unnamed") else f"{a}_{b}"
         for a, b in df.columns
      ]
   return df

def getcsv(link, filename):
   name = filename.lower()
   if "shooting" in name:
      table_id = "stats_shooting"
   elif "keeper" in name:
      table_id = "stats_keeper"
   elif "playing" in name:
      table_id = "stats_playing_time"
   elif "misc" in name:
      table_id = "stats_misc"
   else:
      table_id = "stats_standard"

   try:
      driver.get(link)
      time.sleep(random.uniform(4, 7))

      dfs = pd.read_html(driver.page_source, attrs={"id": table_id})
      if not dfs:
         print(f"[WARN] No table found for {filename}")
         return

      df = dfs[0]
      df = flatten_columns(df)

      player_col = df.columns[0]
      df = df[df[player_col] != player_col]
      df = df[df[player_col].notna()]

      print(f"[OK] {filename} — shape: {df.shape}")
      df.to_csv(filename, index=False)

   except Exception as e:
      print(f"[ERROR] {filename}: {e}")

   time.sleep(random.uniform(5, 10))


def build_fbref_links(season):
   # Current season links are different, so we need to handle them separately
   if season == "2025-2026":
      return [
         "https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats",
         "https://fbref.com/en/comps/Big5/shooting/players/Big-5-European-Leagues-Stats",
         "https://fbref.com/en/comps/Big5/keepers/players/Big-5-European-Leagues-Stats",
         "https://fbref.com/en/comps/Big5/playingtime/players/Big-5-European-Leagues-Stats",
         "https://fbref.com/en/comps/Big5/misc/players/Big-5-European-Leagues-Stats",
      ]
   return [
      f"https://fbref.com/en/comps/Big5/{season}/stats/players/{season}-Big-5-European-Leagues-Stats",
      f"https://fbref.com/en/comps/Big5/{season}/shooting/players/{season}-Big-5-European-Leagues-Stats",
      f"https://fbref.com/en/comps/Big5/{season}/keepers/players/{season}-Big-5-European-Leagues-Stats",
      f"https://fbref.com/en/comps/Big5/{season}/playingtime/players/{season}-Big-5-European-Leagues-Stats",
      f"https://fbref.com/en/comps/Big5/{season}/misc/players/{season}-Big-5-European-Leagues-Stats",
   ]

def build_fbref_filenames(season):
   return [
      f"{season}-Big-5-European-Leagues-Stats.csv",
      f"{season}-Big-5-European-Leagues-Stats-Shooting.csv",
      f"{season}-Big-5-European-Leagues-Stats-Keeper.csv",
      f"{season}-Big-5-European-Leagues-Stats-Playing-Time.csv",
      f"{season}-Big-5-European-Leagues-Stats-Misc.csv",
   ]

def scrape_all_seasons(seasons):
   for season in seasons:
      print(f"\n===== Season: {season} =====")
      links = build_fbref_links(season)
      filenames = build_fbref_filenames(season)
      for link, filename in zip(links, filenames):
         print(f"Scraping: {link}")
         getcsv(link, filename)
      time.sleep(random.uniform(10, 15))

scrape_all_seasons(["2020-2021", "2021-2022", "2022-2023", "2023-2024", "2024-2025", "2025-2026"])

driver.quit()