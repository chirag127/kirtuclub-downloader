from utils import download_jpg
import os


def main():
    for s in ["savita-bhabhi"]:
        for i in range(200):
            episode_dir = os.path.join("content", "savita-bhabhi", "images", "episode-" + str(i).zfill(3))
            os.makedirs(episode_dir, exist_ok=True)
            print("episode", i)
            for j in range(1, 100):
                print("page", j)
                url = "https://kirtuclub.com/wp-content/uploads/2023/05/savita-bhabhi-episode-{}-{}.jpg".format(i, j)
                filepath = os.path.join(episode_dir, str(j) + ".jpg")
                if not os.path.exists(filepath):
                    if not download_jpg(url, filepath):
                        break


if __name__ == "__main__":
    main()