import argparse

from fine_grained_segmentation import main
    
# Parse command line arguments
parser = argparse.ArgumentParser(
    description='Detect and segment fashion items in images.')
parser.add_argument('--image', required=True,
                    metavar="path to image",
                    help='Image to detect fashion items on')

args = parser.parse_args()

main.detect(args.image)
