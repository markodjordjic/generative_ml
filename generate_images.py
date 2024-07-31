from operations.operation import ImageCaller


if __name__ == '__main__':

    image_caller = ImageCaller(
        prompt='People working in the forest'
    )
    image_caller.generate_image()
    image_caller.display_image()