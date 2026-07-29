import argparse
import os
from utils import download_jpg


KIRTUCLUB_BASE = "https://kirtuclub.com/wp-content/uploads/2023/05"


def download_episode(series, episode, base_dir, base_url):
    episode_dir = os.path.join(base_dir, series, "images", f"episode-{episode:03d}")
    os.makedirs(episode_dir, exist_ok=True)
    for page in range(1, 100):
        url = f"{base_url}/{series}-episode-{episode}-{page}.jpg"
        filepath = os.path.join(episode_dir, f"{page}.jpg")
        if os.path.exists(filepath):
            continue
        if not download_jpg(url, filepath):
            break


def main():
    parser = argparse.ArgumentParser(description="Download comic pages from KirtuClub")
    parser.add_argument("--series", default="savita-bhabhi", help="Series slug")
    parser.add_argument("--episodes", type=int, nargs=2, default=[1, 200], metavar=("START", "END"), help="Episode range")
    parser.add_argument("--base-dir", default="content", help="Base output directory")
    parser.add_argument("--base-url", default=KIRTUCLUB_BASE, help="Base URL for images")
    args = parser.parse_args()

    for ep in range(args.episodes[0], args.episodes[1] + 1):
        download_episode(args.series, ep, args.base_dir, args.base_url)


if __name__ == "__main__":
    main()
