import argparse
from fine_grained_segmentation.main import detect


def main():
    '''
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Detect and segment fashion items in images.')
    parser.add_argument('--image', required=True,
                        metavar="path to image",
                        help='Image to detect fashion items on')

    args = parser.parse_args()
    detect(args.image)
    '''
    detect("https://cdn.cliqueinc.com/cache/posts/281219/cool-outfits-for-women-in-20s-281219-1562964559214-main.600x0c.jpg")

'''
if __name__ == "__main__":
    main()
'''