# https://kirtuclub.com/wp-content/uploads/2023/05/savita-bhabhi-episode-153-140.jpg

from utils import download_jpg
import os

for s in ["savita-bhabhi"]:

    for i in range(200):
        if not os.path.exists("images/" + s + "/" + str(i)):
            os.makedirs("images/" + s + "/" + str(i))

        print("episode", i)

        for j in range(1, 100):

            print("page", j)

            url = f"https://kirtuclub.com/wp-content/uploads/2023/05/savita-bhabhi-episode-{i}-{j}.jpg"

            filepath = "images/" + s + "/" + str(i) + "/" + str(j) + ".jpg"

            if not os.path.exists(filepath):

                # make directory

                if not download_jpg(url, filepath):
                    break
