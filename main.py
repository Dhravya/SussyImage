"""
Converts an image into funny, smaller amongus characters
"""

import os
from typing import List
from rich import print
from rich.progress import track

import numpy as np
from cv2 import imread, imwrite, imshow, resize, waitKey, destroyAllWindows, INTER_AREA


class SussyImage:
    """
    Makes the input image into smaller amongus characters (or any other emoji/pictures you want)

    Attributes
    ----------
        i_image (np.ndarray): The input image
        emoji_size (int): The size of the emoji
        width (int): The width of the output image
        emoji_path (str): The path to the emoji images
        emojis (List[np.ndarray]): The emojis

    Methods
    -------
        run(): Runs the program
        __check_if_close_and_replace(): Checks if the image color is similar to the average color of the input image. if yes, replaces it.
        initialise_picture(): Resizes image to a width. Defaults to 3000, Returns the resized image
        initialise_emojis(): Returns a list of cv2.imread()'ed emojis
    """

    def __init__(
        self,
        /,
        input_img_path: os.PathLike,
        images_path: os.PathLike = "amongus_images/",
        width: int = 3000,
        emoji_size=30,
    ) -> None:
        # Check if the input image exists
        if not os.path.exists(input_img_path):
            print(f"[bold red]Input image does not exist:[/bold red] {input_img_path}")
            exit()

        # Check if the images folder exists
        if not os.path.exists(images_path):
            print(f"[bold red]Images folder does not exist:[/bold red] {images_path}")
            exit()

        self.i_path = input_img_path
        self.emoji_path = images_path

        self.emoji_size = emoji_size
        self.width = width

        # Initialises the image and "emojis"
        self.input_image = self.initialise_picture()
        self.emojis = self.initialise_emojis()

    def initialise_emojis(self) -> List[np.ndarray]:
        """Returns a list of cv2.imread()'ed emojis"""
        images = [self.emoji_path + image for image in os.listdir(self.emoji_path)]
        size = self.emoji_size, self.emoji_size
        for image in images:
            if not os.path.exists(image):
                print("Image does not exist: {}".format(image))
                exit()
        images = [
            resize(imread(image), size, interpolation=INTER_AREA) for image in images
        ]

        return images

    def initialise_picture(self) -> np.ndarray:
        """Resizes image to a width provided"""
        input_image = imread(self.i_path)

        input_image = resize(
            input_image,
            (
                int((self.width / input_image.shape[0]) * input_image.shape[1]),
                self.width,
            ),
        )

        return input_image

    def _check_if_close_and_replace(
        self,
        image: np.ndarray,
        /,
        average_col: float,
        output_img: np.ndarray,
        dim: tuple,
        avgs: dict,
        atol: float = 50,
    ) -> None:
        """Checks if the image color is similar to the average color of the input image. if yes, replaces it.

        Args:
        ----------
            image (np.ndarray): The input image
            average_col (float): Average color of the input image
            output_img (np.ndarray): The image on which the image/emoji will be placed
            dim (tuple): The dimensions of the image/emoji
            avgs (dict): The average colors of the emojis, so we don't have to calculate them every time
            atol (float, optional): The tolerance level. Defaults to 50.
        """
        i, j = dim

        average_col_image = avgs[str(image)]

        if np.allclose(average_col, average_col_image, atol=atol):
            try:
                output_img[i : i + self.emoji_size, j : j + self.emoji_size] = image
            except Exception:
                pass

    def run(
        self,
        atol: float = 50,
        /,
        show: bool = False,
        save: bool = True,
        save_path="output.png",
        compare: bool = False
    ) -> np.ndarray:
        """Runs the entire program

        Args:
        ----------
            atol (float, optional): Average tolerance. Defaults to 50.
            show (bool, optional): Whether or not to show the image after completion. Defaults to False.
            save (bool, optional): Whether of not to save the image. Saves to the provided save_path. Defaults to False.
            save_path (str, optional): Where to save the output. Defaults to "output.png".
            compare (bool, optional): Stacks the input image and the output image side by side. Defaults to False.

        Returns:
        ----------
            (np.ndarray, None): Either returns the array of the output image, or None if save is True
        """
        input_image = self.input_image
        images = self.emojis

        get_average_color = lambda image: np.average(np.mean(image, axis=0), axis=0)

        output_img = np.zeros(input_image.shape, dtype=np.uint8)
        avgs = {str(image): get_average_color(image) for image in images}

        # Loops through 50 * 50 pixels of the input image
        for i in track(range(0, input_image.shape[0], self.emoji_size)):
            for j in range(0, input_image.shape[1], self.emoji_size):
                # Gets the average color of the input image
                average_col = get_average_color(
                    input_image[i : i + self.emoji_size, j : j + self.emoji_size]
                )

                for image in images:
                    self._check_if_close_and_replace(
                        image,
                        average_col=average_col,
                        output_img=output_img,
                        dim=(i, j),
                        avgs=avgs,
                        atol=atol,
                    )

        if compare:
            output_img = np.hstack((input_image, output_img))

        if show:
            imshow("Output", output_img)
            waitKey(0)
            destroyAllWindows()

        if save:
            imwrite(save_path, output_img)
            print(
                f"[green] Saved the image to [underlined]{save_path}[/underlined][/green]"
            )
            return None

        return output_img


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.app:app", host="0.0.0.0", port=8000)